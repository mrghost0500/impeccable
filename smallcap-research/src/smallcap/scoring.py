"""Stage 2 scoring: six investor lenses (each 0-10) and red-flag deductions.

Every lens is a weighted average of sub-scores on a 0-10 scale. Inputs that the
data source cannot provide (promoter change, pledge, debtor days, margin and ROCE
history, product checks) default to a neutral 5 and can be filled in later
through per-company overrides from the Stage 3 and Stage 4 research.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

import pandas as pd

NEUTRAL = 5.0


def isnum(x) -> bool:
    return x is not None and not (isinstance(x, float) and math.isnan(x))


def lin(x: float, zero_at: float, ten_at: float) -> float:
    """Map x linearly so that `zero_at` -> 0 and `ten_at` -> 10, clipped to [0, 10].

    Works in both directions (ten_at may be below zero_at for "lower is better").
    """
    if zero_at == ten_at:
        raise ValueError("zero_at and ten_at must differ")
    t = (x - zero_at) / (ten_at - zero_at)
    return max(0.0, min(10.0, 10.0 * t))


def wavg(parts: dict[str, tuple[float, float]]) -> float:
    total_w = sum(w for _, w in parts.values())
    return sum(s * w for s, w in parts.values()) / total_w


# ---------------------------------------------------------------- helpers

def peg(pe, growth_pct):
    """PEG = P/E / 3Y profit CAGR (in percent). None when either is non-positive."""
    if not (isnum(pe) and isnum(growth_pct)) or pe <= 0 or growth_pct <= 0:
        return None
    return pe / growth_pct


def cfo_to_pat(cfo, pat):
    if not (isnum(cfo) and isnum(pat)) or pat <= 0:
        return None
    return cfo / pat


@dataclass
class Context:
    industry_pe: dict = field(default_factory=dict)
    industry_opm: dict = field(default_factory=dict)
    sector_pe: dict = field(default_factory=dict)
    sector_opm: dict = field(default_factory=dict)
    overall_pe: float = 25.0
    overall_opm: float = 12.0

    @classmethod
    def from_frame(cls, df: pd.DataFrame, min_peers: int = 5) -> "Context":
        pos = df[(df["pe"] > 0) & (df["pe"] < 200)]
        def medians(frame, key, col):
            g = frame.groupby(key)[col]
            m = g.median()[g.count() >= min_peers]
            return {k: float(v) for k, v in m.items() if k}
        return cls(
            industry_pe=medians(pos, "industry", "pe"),
            sector_pe=medians(pos, "sector", "pe"),
            industry_opm=medians(df, "industry", "opm"),
            sector_opm=medians(df, "sector", "opm"),
            overall_pe=float(pos["pe"].median()) if len(pos) else 25.0,
            overall_opm=float(df["opm"].median()) if df["opm"].notna().any() else 12.0,
        )

    def pe_for(self, industry, sector) -> float:
        return self.industry_pe.get(industry) or self.sector_pe.get(sector) or self.overall_pe

    def opm_for(self, industry, sector) -> float:
        return self.industry_opm.get(industry) or self.sector_opm.get(sector) or self.overall_opm


# ---------------------------------------------------------------- lenses

def lynch_score(r: dict, cfg: dict, ctx: Context) -> tuple[float, dict]:
    c = cfg["lynch"]
    sw = c["sub_weights"]
    detail = {}

    p = peg(r.get("pe"), r.get("pat_g3y"))
    detail["peg"] = p
    if p is None:
        s_peg = 0.0 if not isnum(r.get("pe")) or (r.get("pe") or 0) <= 0 else 1.0
    else:
        s_peg = lin(p, c["peg_worst"], c["peg_best"])

    ind_pe = ctx.pe_for(r.get("industry"), r.get("sector"))
    detail["industry_pe"] = ind_pe
    if isnum(r.get("pe")) and r["pe"] > 0:
        s_pe_ind = lin(r["pe"] / ind_pe, 1.5, 0.5)
    else:
        s_pe_ind = 0.0

    inst = r.get("inst_pct")
    s_inst = 7.0 if not isnum(inst) else lin(inst, 30, c["max_institutional_pct"])

    de = r.get("de")
    s_de = NEUTRAL if not isnum(de) else lin(de, 1.0, c["max_de"])

    mcap = r.get("mcap_cr")
    s_mcap = NEUTRAL if not isnum(mcap) else (10.0 if mcap <= c["max_mcap_cr"] else lin(mcap, 2 * c["max_mcap_cr"], c["max_mcap_cr"]))

    chg = r.get("promoter_chg_3y")
    s_prom = NEUTRAL if not isnum(chg) else lin(chg, -5.0, 0.0)

    ind = str(r.get("industry", ""))
    boring = any(pat.lower() in ind.lower() for pat in c["boring_industry_patterns"])
    detail["boring"] = boring
    s_boring = 10.0 if boring else 3.0

    score = wavg({
        "peg": (s_peg, sw["peg"]), "pe_ind": (s_pe_ind, sw["pe_vs_industry"]),
        "inst": (s_inst, sw["institutional"]), "de": (s_de, sw["de"]),
        "mcap": (s_mcap, sw["mcap"]), "prom": (s_prom, sw["promoter_not_selling"]),
        "boring": (s_boring, sw["boring"]),
    })
    return score, detail


def reinvestment_score(capex, cfo) -> float:
    if not (isnum(capex) and isnum(cfo)):
        return NEUTRAL
    if cfo <= 0:
        return 2.0
    ratio = abs(capex) / cfo
    if 0.3 <= ratio <= 1.0:
        return 10.0
    if ratio < 0.3:
        return 4.0 + 20.0 * ratio
    return max(2.0, 10.0 - 8.0 * (ratio - 1.0))


def mayer_score(r: dict, cfg: dict, ctx: Context) -> tuple[float, dict]:
    c = cfg["mayer"]
    mcap = r.get("mcap_cr")
    s_mcap = NEUTRAL if not isnum(mcap) else (10.0 if mcap <= c["max_mcap_cr"] else lin(mcap, 5000, c["max_mcap_cr"]))
    roe = r.get("roe")
    s_roe = NEUTRAL if not isnum(roe) else lin(roe, 10, c["min_roe"] + 5)
    g = r.get("sales_g3y")
    s_g = NEUTRAL if not isnum(g) else lin(g, 5, c["min_sales_growth_3y"] + 5)
    prom = r.get("promoter_pct")
    s_prom = NEUTRAL if not isnum(prom) else lin(prom, 30, c["min_promoter_pct"] + 10)
    s_reinv = reinvestment_score(r.get("capex_cr"), r.get("cfo_cr"))
    score = (s_mcap + s_roe + s_g + s_prom + s_reinv) / 5.0
    return score, {"reinvestment": s_reinv}


def buffett_fisher_score(r: dict, cfg: dict, ctx: Context) -> tuple[float, dict]:
    c = cfg["buffett_fisher"]
    roce = r.get("roce")
    s_roce = NEUTRAL if not isnum(roce) else lin(roce, c["roce_floor"], c["roce_target"])
    ind_opm = ctx.opm_for(r.get("industry"), r.get("sector"))
    opm = r.get("opm")
    if isnum(opm) and ind_opm and ind_opm > 0:
        s_price = lin(opm / ind_opm, 0.5, 1.5)
    else:
        s_price = NEUTRAL
    s_roce_stab = r.get("roce_stability") if isnum(r.get("roce_stability")) else NEUTRAL
    s_margin_stab = r.get("margin_stability") if isnum(r.get("margin_stability")) else NEUTRAL
    score = wavg({
        "roce": (s_roce, 0.40), "pricing": (s_price, 0.30),
        "roce_stab": (s_roce_stab, 0.15), "margin_stab": (s_margin_stab, 0.15),
    })
    return score, {"industry_opm": ind_opm}


def kirby_score(r: dict, cfg: dict, ctx: Context) -> tuple[float, dict]:
    c = cfg["kirby_mukherjea"]
    checks = []
    for key in ("sales_g3y", "sales_g_yoy"):
        v = r.get(key)
        checks.append(0.5 if not isnum(v) else lin(v, 0, c["min_sales_growth"]) / 10)
    roce = r.get("roce")
    checks.append(0.5 if not isnum(roce) else lin(roce, 5, c["min_roce"]) / 10)
    conv = cfo_to_pat(r.get("cfo_cr"), r.get("pat_cr"))
    checks.append(0.5 if conv is None else lin(conv, 0.3, c["min_cfo_to_pat"]) / 10)
    dd = r.get("debtor_days")
    checks.append(0.5 if not isnum(dd) else lin(dd, 180, c["max_debtor_days"]) / 10)
    return 10.0 * sum(checks) / len(checks), {"cfo_to_pat": conv}


def pe_vc_score(r: dict, cfg: dict, ctx: Context) -> tuple[float, dict]:
    c = cfg["pe_vc"]
    inc = r.get("inc_roce") if isnum(r.get("inc_roce")) else r.get("roce")
    s_inc = NEUTRAL if not isnum(inc) else lin(inc, 10, 40)

    capex, sales, cfo = r.get("capex_cr"), r.get("sales_cr"), r.get("cfo_cr")
    if isnum(capex) and isnum(sales) and sales > 0:
        s_light = lin(abs(capex) / sales, c["capex_to_sales_heavy"], c["capex_to_sales_light"])
    else:
        s_light = NEUTRAL
    if isnum(capex) and isnum(cfo):
        s_payback = 10.0 if abs(capex) < 1e-9 and cfo > 0 else (2.0 if cfo <= 0 else lin(cfo / abs(capex), 0.5, 3.0))
    else:
        s_payback = NEUTRAL
    s_head = r.get("headroom") if isnum(r.get("headroom")) else NEUTRAL

    mcap = r.get("mcap_cr")
    cutoff = c["smallcap250_cutoff_cr"]
    if not isnum(mcap):
        s_exit = NEUTRAL
    else:
        ratio = mcap / cutoff
        s_exit = 10.0 if 0.5 <= ratio <= 1.0 else (6.0 if ratio > 1.0 else lin(ratio, 0.1, 0.5))
    if r.get("sme") is True:
        # SME -> main-board migration is a re-rating / liquidity event in its own right
        s_exit = max(s_exit, 8.0)
    score = wavg({
        "inc": (s_inc, 0.30), "light": (s_light, 0.20), "payback": (s_payback, 0.15),
        "head": (s_head, 0.20), "exit": (s_exit, 0.15),
    })
    return score, {}


def product_score(r: dict, cfg: dict, ctx: Context) -> tuple[float, dict]:
    v = r.get("product_score")
    return (float(v) if isnum(v) else NEUTRAL), {}


LENSES = {
    "lynch": lynch_score,
    "mayer": mayer_score,
    "buffett_fisher": buffett_fisher_score,
    "kirby_mukherjea": kirby_score,
    "pe_vc": pe_vc_score,
    "lynch_product": product_score,
}


# ---------------------------------------------------------------- red flags

def red_flags(r: dict, cfg: dict) -> list[tuple[str, float]]:
    d = cfg["red_flags"]
    flags: list[tuple[str, float]] = []
    if isnum(r.get("pledge_pct")) and r["pledge_pct"] > 0:
        # 0.2 for a token pledge, rising to 1.0 once half the promoter stake is pledged
        size = 0.2 + 0.8 * min(r["pledge_pct"] / 50.0, 1.0)
        flags.append((f"promoter pledge {r['pledge_pct']:.1f}% of holding", round(max(size, 0.2), 2)))
    if isnum(r.get("promoter_chg_3y")) and r["promoter_chg_3y"] < -5:
        flags.append((f"promoter stake down {abs(r['promoter_chg_3y']):.1f}pp in 3Y", d["promoter_stake_down_5pp"]))
    writeoff = bool(r.get("writeoff_exceptional")) or (
        isnum(r.get("pat_cr")) and isnum(r.get("ebit_cr")) and r["pat_cr"] < 0 < r["ebit_cr"]
    )
    if writeoff:
        flags.append(("exceptional write-off / net loss despite operating profit", d["exceptional_writeoff"]))
    conv = cfo_to_pat(r.get("cfo_cr"), r.get("pat_cr"))
    if conv is not None and conv < 0.5:
        flags.append((f"CFO/PAT {conv:.2f} < 0.5", d["cfo_to_pat_below_0_5"]))
    if isnum(r.get("debtor_days")) and r["debtor_days"] > 150:
        flags.append((f"debtor days {r['debtor_days']:.0f} > 150", d["debtor_days_above_150"]))
    if isnum(r.get("rpt_pct")) and r["rpt_pct"] > 10:
        flags.append((f"related-party sales {r['rpt_pct']:.0f}% > 10%", d["related_party_sales_above_10pct"]))
    if r.get("auditor_change") is True:
        flags.append(("auditor change or resignation", d["auditor_change"]))
    if r.get("regulatory_incident") is True:
        flags.append(("regulatory / safety incident", d["regulatory_incident"]))
    if isnum(r.get("shares_yoy")) and r["shares_yoy"] > 10:
        flags.append((f"share count +{r['shares_yoy']:.0f}% YoY (dilution)", d["dilution_above_10pct"]))
    return flags


# ---------------------------------------------------------------- composite

def normalise_weights(weights: dict) -> dict:
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("weights must sum to a positive number")
    return {k: v / total for k, v in weights.items()}


def score_row(r: dict, cfg: dict, ctx: Context) -> dict:
    weights = normalise_weights(cfg["weights"])
    out = {}
    detail = {}
    for lens, fn in LENSES.items():
        s, d = fn(r, cfg, ctx)
        out[f"s_{lens}"] = round(s, 3)
        detail.update(d)
    base = sum(out[f"s_{k}"] * w for k, w in weights.items())
    flags = red_flags(r, cfg)
    deduction = sum(x for _, x in flags)
    out["base_score"] = round(base, 3)
    out["red_flag_deduction"] = round(deduction, 2)
    out["red_flags"] = "; ".join(f for f, _ in flags)
    out["n_red_flags"] = len(flags)
    out["score"] = round(max(0.0, min(10.0, base - deduction)), 3)
    out["peg"] = None if detail.get("peg") is None else round(detail["peg"], 2)
    out["industry_pe"] = round(detail.get("industry_pe", float("nan")), 1)
    cp = detail.get("cfo_to_pat")
    out["cfo_to_pat"] = None if cp is None else round(cp, 2)
    out["boring"] = detail.get("boring", False)
    return out


def score_frame(df: pd.DataFrame, cfg: dict, ctx: Context | None = None) -> pd.DataFrame:
    ctx = ctx or Context.from_frame(df)
    scored = df.apply(lambda r: pd.Series(score_row(r.to_dict(), cfg, ctx)), axis=1)
    res = pd.concat([df.reset_index(drop=True), scored.reset_index(drop=True)], axis=1)
    res = res.sort_values("score", ascending=False).reset_index(drop=True)
    res["rank"] = range(1, len(res) + 1)
    return res


def mcap_band(mcap) -> str:
    if not isnum(mcap):
        return "n/a"
    if mcap < 1000:
        return "<1k Cr"
    if mcap < 2000:
        return "1k-2k Cr"
    if mcap < 5000:
        return "2k-5k Cr"
    return ">5k Cr"

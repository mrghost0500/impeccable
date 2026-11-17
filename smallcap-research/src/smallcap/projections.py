"""Final list: scenario probabilities, expected FY28 profit and PE-style outcomes.

Probabilities: start from a prior (25/50/25 bear/base/bull). Each negative evidence
flag moves `shift_per_flag` from bull to bear; each positive flag moves it back.
Bear and bull are clamped to configured ranges and base takes the remainder.

Outcomes (illustrative, research only): value at the end of the horizon =
FY28 PAT x exit P/E. Exit P/E: bear = derate x min(FY26 P/E, peer P/E);
base = midpoint of FY26 P/E and peer P/E; bull = max of the two; all capped.
MOIC = value / today's market cap (ignores dividends, dilution and net cash).
"""
from __future__ import annotations

import json
import os

import pandas as pd

from .final_content import FINAL
from .memo_content import MEMOS
from .pipeline import load_cfg

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "outputs")
LABELS = ("Bear", "Base", "Bull")


def scenario_probs(flags: dict, pcfg: dict) -> tuple[tuple[float, float, float], list[str]]:
    bear, _, bull = pcfg["prior"]
    step = pcfg["shift_per_flag"]
    reasons = []
    for f in pcfg["negative_flags"]:
        if flags.get(f):
            bear += step
            bull -= step
            reasons.append(f"-{f}")
    for f in pcfg["positive_flags"]:
        if flags.get(f):
            bear -= step
            bull += step
            reasons.append(f"+{f}")
    bear = min(max(bear, pcfg["bear_range"][0]), pcfg["bear_range"][1])
    bull = min(max(bull, pcfg["bull_range"][0]), pcfg["bull_range"][1])
    base = 1.0 - bear - bull
    return (round(bear, 2), round(base, 2), round(bull, 2)), reasons


def exit_multiples(pe_now: float, peer_pe: float | None, pcfg: dict) -> tuple[float, float, float]:
    peer = peer_pe if peer_pe else pe_now
    cap = pcfg["exit_pe_cap"]
    bear = min(pcfg["bear_derate"] * min(pe_now, peer), cap)
    base = min((pe_now + peer) / 2, cap)
    bull = min(max(pe_now, peer), cap)
    return bear, base, bull


def outcomes(mcap: float, fy26_pat: float, scen, probs, peer_pe, pcfg: dict) -> dict:
    pe_now = mcap / fy26_pat
    exits = exit_multiples(pe_now, peer_pe, pcfg)
    h = pcfg["horizon_years"]
    rows = []
    for lab, pat, p, xpe in zip(LABELS, scen, probs, exits):
        value = pat * xpe
        moic = value / mcap
        irr = moic ** (1 / h) - 1 if moic > 0 else -1.0
        rows.append(dict(scenario=lab, prob=p, fy28_pat=pat, pat_cagr=(pat / fy26_pat) ** 0.5 - 1,
                         exit_pe=xpe, value_cr=value, moic=moic, irr=irr))
    e_pat = sum(r["prob"] * r["fy28_pat"] for r in rows)
    e_moic = sum(r["prob"] * r["moic"] for r in rows)
    return dict(rows=rows, pe_now=pe_now, peer_pe=peer_pe, e_pat=e_pat, e_moic=e_moic,
                e_irr=e_moic ** (1 / h) - 1 if e_moic > 0 else -1.0,
                p_loss=sum(r["prob"] for r in rows if r["moic"] < 1.0),
                p_15x=sum(r["prob"] for r in rows if r["moic"] >= 1.5))


def build() -> pd.DataFrame:
    cfg = load_cfg()
    pcfg = cfg["projections"]
    fin = pd.read_csv(os.path.join(OUT, "finalists.csv"), dtype={"ticker": str})
    top = pd.read_csv(os.path.join(OUT, "rescored_top60.csv"), dtype={"ticker": str})
    gap = pd.read_csv(os.path.join(OUT, "valuation_gap.csv"), dtype={"ticker": str})
    council = json.load(open(os.path.join(OUT, "council.json")))
    out, detail = [], {}
    for t, spec in FINAL.items():
        if spec["tier"] == "A":
            row = fin[fin["ticker"] == t].iloc[0]
            memo = MEMOS[row["symbol"]]
            name, mcap, fy26_pat, scen = row["name"], row["mcap_cr"], memo["fy26_pat"], memo["scen"]
            g = gap[gap["ticker"] == t].iloc[0]
            peer_pe = g["peer_median_pe"] if pd.notna(g["peer_median_pe"]) else g["model_pe"]
            screen, csc = row["score"], council[t]["chairman_score"]
            symbol, industry = row["symbol"], row["industry"]
        else:
            row = top[top["ticker"] == t].iloc[0]
            name, mcap, fy26_pat, scen = spec["name"], row["mcap_cr"], spec["fy26_pat"], spec["scen"]
            peer_pe = spec.get("peer_pe") or row["industry_pe"]
            screen, csc = row["score"], None
            symbol, industry = row["symbol"], row["industry"]
        probs, reasons = scenario_probs(spec["flags"], pcfg)
        oc = outcomes(mcap, fy26_pat, scen, probs, peer_pe, pcfg)
        detail[t] = dict(oc=oc, reasons=reasons, probs=probs)
        out.append(dict(
            tier=spec["tier"], ticker=t, symbol=symbol, name=name, industry=industry, lynch=spec["lynch"],
            mcap_cr=round(mcap), fy26_pat=fy26_pat, pe_fy26=round(oc["pe_now"], 1),
            peer_pe=None if peer_pe is None else round(float(peer_pe), 1),
            screen_score=round(screen, 2), council_score=csc,
            pat_bear=scen[0], pat_base=scen[1], pat_bull=scen[2],
            p_bear=probs[0], p_base=probs[1], p_bull=probs[2], prob_drivers=", ".join(reasons) or "none",
            exp_fy28_pat=round(oc["e_pat"], 1), exp_pat_cagr=round(((oc["e_pat"] / fy26_pat) ** 0.5 - 1) * 100, 1),
            moic_bear=round(oc["rows"][0]["moic"], 2), moic_base=round(oc["rows"][1]["moic"], 2),
            moic_bull=round(oc["rows"][2]["moic"], 2), exp_moic=round(oc["e_moic"], 2),
            exp_irr_pct=round(oc["e_irr"] * 100, 1), p_loss=round(oc["p_loss"], 2), p_moic_1_5x=round(oc["p_15x"], 2),
            story=spec["story"], pe_case=spec["pe_case"],
        ))
    df = pd.DataFrame(out)
    df["_order"] = df.apply(lambda r: (0 if r["tier"] == "A" else 1,
                                       -(r["council_score"] if r["tier"] == "A" else r["screen_score"])), axis=1)
    df = df.sort_values("_order").drop(columns="_order").reset_index(drop=True)
    df.insert(0, "final_rank", range(1, len(df) + 1))
    df.to_csv(os.path.join(OUT, "final_list.csv"), index=False)
    with open(os.path.join(OUT, "final_detail.json"), "w") as fh:
        json.dump({k: dict(probs=v["probs"], reasons=v["reasons"], rows=v["oc"]["rows"]) for k, v in detail.items()},
                  fh, indent=1, default=float)
    return df


if __name__ == "__main__":
    d = build()
    pd.set_option("display.width", 250)
    print(d[["final_rank", "tier", "name", "lynch", "pe_fy26", "peer_pe", "pat_base", "p_bear", "p_base", "p_bull",
             "exp_fy28_pat", "exp_moic", "exp_irr_pct", "p_loss", "prob_drivers"]].to_string(max_colwidth=24))

"""Comparables: peer tables, peer-relative valuation and a fundamentals-implied P/E.

Two yardsticks per finalist:
  1. Peer median P/E from a hand-picked peer set (universe peers on the same data
     date + larger listed leaders from web research, dated).
  2. A screen-wide regression of log(P/E) on ROCE, 3Y sales and profit growth,
     size, leverage and sector. It explains only ~17% of P/E variation in these
     small caps, so it is a weak cross-check, reported alongside the peer view.
"""
from __future__ import annotations

import json
import math
import os

import numpy as np
import pandas as pd

from .comparables_content import COMPS

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "outputs")
PE_LO, PE_HI = 3.0, 100.0  # >100x P/E means earnings too thin for a meaningful multiple
METRICS = ["mcap_cr", "pe", "roce", "opm", "sales_g3y", "pat_g3y", "de"]


def _valid_pe(x) -> bool:
    return x is not None and not (isinstance(x, float) and math.isnan(x)) and PE_LO < x < PE_HI


def _median(vals):
    vals = [v for v in vals if v is not None and not (isinstance(v, float) and math.isnan(v))]
    return float(np.median(vals)) if vals else None


# ------------------------------------------------------------- peer tables

def peer_rows(ticker: str, universe: pd.DataFrame) -> list[dict]:
    spec = COMPS.get(ticker, {})
    uni = universe.assign(ticker=universe["ticker"].astype(str))
    rows = []
    for t in spec.get("universe_peers", []):
        hit = uni[uni["ticker"] == str(t)]
        if hit.empty:
            continue
        r = hit.iloc[0]
        rows.append(dict(peer=r["name"], ticker=t, source="screener universe (17-Nov-2026)",
                         url=r.get("stockanalysis_url"), **{m: r.get(m) for m in METRICS}))
    for e in spec.get("external_peers", []):
        rows.append(dict(peer=e["name"], ticker="", source=f"web search snapshot ({e['asof']})", url=e["url"],
                         mcap_cr=e.get("mcap_cr"), pe=e.get("pe"), roce=e.get("roce"), opm=None,
                         sales_g3y=None, pat_g3y=None, de=None, note=e.get("growth")))
    return rows


def peer_pe(ticker: str, universe: pd.DataFrame):
    return _median([r["pe"] for r in peer_rows(ticker, universe) if _valid_pe(r["pe"])])


def peer_pe_map(universe: pd.DataFrame) -> dict:
    """symbol -> peer median P/E, for the scoring overrides."""
    uni = universe.assign(ticker=universe["ticker"].astype(str))
    out = {}
    for t in COMPS:
        sym = uni.loc[uni["ticker"] == t, "symbol"]
        p = peer_pe(t, universe)
        if len(sym) and p is not None:
            out[sym.iloc[0]] = round(p, 1)
    return out


# ------------------------------------------------------------- P/E model

def fit_pe_model(scores: pd.DataFrame) -> dict:
    d = scores[(scores["pe"] > PE_LO) & (scores["pe"] < PE_HI)].dropna(
        subset=["roce", "sales_g3y", "pat_g3y", "de", "mcap_cr"]).copy()
    d["sector"] = d["sector"].fillna("").replace("", "Unclassified")
    sectors = sorted(d["sector"].unique())
    base_sector = sectors[0]

    def design(df):
        cols = [np.ones(len(df)), df["roce"].clip(-10, 60), df["sales_g3y"].clip(-30, 80),
                df["pat_g3y"].clip(-50, 150), np.log(df["mcap_cr"]), df["de"].clip(0, 3)]
        for s in sectors[1:]:
            cols.append((df["sector"] == s).astype(float))
        return np.column_stack(cols)

    X, y = design(d), np.log(d["pe"].values)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ b
    r2 = 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return dict(coef=b.tolist(), sectors=sectors, base_sector=base_sector, r2=float(r2), n=int(len(d)),
                names=["const", "roce", "sales_g3y", "pat_g3y", "log_mcap", "de"] + [f"sector:{s}" for s in sectors[1:]])


def model_pe(model: dict, row: dict):
    need = ["roce", "sales_g3y", "pat_g3y", "de", "mcap_cr"]
    vals = {k: row.get(k) for k in need}
    # missing growth -> sector-neutral 0 contribution is wrong; use clipped medians instead
    defaults = {"roce": 15.0, "sales_g3y": 12.0, "pat_g3y": 12.0, "de": 0.3}
    for k, v in vals.items():
        if v is None or (isinstance(v, float) and math.isnan(v)):
            if k == "mcap_cr":
                return None
            vals[k] = defaults[k]
    sector = row.get("sector") or "Unclassified"
    if isinstance(sector, float):
        sector = "Unclassified"
    x = [1.0, min(max(vals["roce"], -10), 60), min(max(vals["sales_g3y"], -30), 80),
         min(max(vals["pat_g3y"], -50), 150), math.log(vals["mcap_cr"]), min(max(vals["de"], 0), 3)]
    x += [1.0 if sector == s else 0.0 for s in model["sectors"][1:]]
    return float(math.exp(np.dot(model["coef"], x)))


# ------------------------------------------------------------- outputs

def build(finalists: pd.DataFrame | None = None) -> dict:
    uni = pd.read_csv(os.path.join(OUT, "universe.csv"))
    scores = pd.read_csv(os.path.join(OUT, "scores.csv"))
    fin = finalists if finalists is not None else pd.read_csv(os.path.join(OUT, "finalists.csv"))
    model = fit_pe_model(scores)
    from .memo_content import MEMOS

    long_rows, gap_rows = [], []
    for _, f in fin.iterrows():
        t = str(f["ticker"])
        spec = COMPS.get(t)
        if spec is None:
            continue
        peers = peer_rows(t, uni)
        memo = MEMOS.get(f["symbol"], {})
        pe_fy26 = f["mcap_cr"] / memo["fy26_pat"] if memo.get("fy26_pat") else None
        long_rows.append(dict(finalist=f["name"], finalist_ticker=t, role="FINALIST", peer=f["name"], ticker=t,
                              source="screener + Stage 3/4 overrides", url=f.get("stockanalysis_url"),
                              **{m: f.get(m) for m in METRICS}))
        for p in peers:
            long_rows.append(dict(finalist=f["name"], finalist_ticker=t, role="peer", **p))

        upe = [p["pe"] for p in peers if _valid_pe(p["pe"])]
        med_pe = _median(upe)
        uni_peers = [p for p in peers if p["ticker"]]
        med = {m: _median([p[m] for p in uni_peers]) for m in ("roce", "opm", "sales_g3y", "pat_g3y")}
        pe_used = f.get("pe")
        mpe = model_pe(model, f.to_dict())
        gap_rows.append(dict(
            finalist=f["name"], ticker=t, mcap_cr=f["mcap_cr"],
            pe_used=pe_used, pe_fy26=None if pe_fy26 is None else round(pe_fy26, 1),
            peer_median_pe=None if med_pe is None else round(med_pe, 1), n_peers_pe=len(upe),
            prem_disc_vs_peers_pct=None if (med_pe is None or not _valid_pe(pe_used)) else round((pe_used / med_pe - 1) * 100, 0),
            model_pe=None if mpe is None else round(mpe, 1),
            prem_disc_vs_model_pct=None if (mpe is None or not _valid_pe(pe_used)) else round((pe_used / mpe - 1) * 100, 0),
            roce=f.get("roce"), peer_median_roce=med["roce"],
            opm=f.get("opm"), peer_median_opm=med["opm"],
            sales_g3y=f.get("sales_g3y"), peer_median_sales_g3y=med["sales_g3y"],
            pat_g3y=f.get("pat_g3y"), peer_median_pat_g3y=med["pat_g3y"],
            competitors=spec["competitors"], positioning=spec["positioning"], valuation_gap=spec["gap"],
        ))

    long_df = pd.DataFrame(long_rows)
    gap_df = pd.DataFrame(gap_rows)
    long_df.to_csv(os.path.join(OUT, "comparables_peers.csv"), index=False)
    gap_df.to_csv(os.path.join(OUT, "valuation_gap.csv"), index=False)
    meta = {k: model[k] for k in ("r2", "n", "names", "coef")}
    meta["note"] = ("log(P/E) ~ ROCE + 3Y sales CAGR + 3Y profit CAGR + log(mcap) + D/E + sector dummies, "
                    "fitted on scored universe names with 3 < P/E < 100. Low R^2: use as a weak cross-check.")
    with open(os.path.join(OUT, "pe_model.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    return {"peers": len(long_df), "finalists": len(gap_df), "model_r2": round(model["r2"], 3)}


if __name__ == "__main__":
    print(build())

"""Run Stages 1-3 end to end from the cache.

    python -m smallcap.pipeline            (run from smallcap-research/ with PYTHONPATH=src)

Outputs land in outputs/: universe.csv, excluded.csv, scores.csv, top60.csv,
rescored_top60.csv (when cache/stage3_overrides.json exists), finalists.csv.
"""
from __future__ import annotations

import json
import os

import pandas as pd
import yaml

from .filters import apply_filters
from .load import load_universe, missing_field_log
from .scoring import Context, mcap_band, score_frame

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_cfg(path: str | None = None) -> dict:
    with open(path or os.path.join(ROOT, "config.yaml")) as fh:
        return yaml.safe_load(fh)


def apply_overrides(df: pd.DataFrame, overrides: dict) -> pd.DataFrame:
    """Overlay researched fields (Stage 3/4) onto the score inputs, keyed by symbol."""
    df = df.copy()
    for sym, fields in overrides.items():
        idx = df.index[df["symbol"] == sym]
        if not len(idx):
            continue
        for k, v in fields.items():
            if k.startswith("_") or k in ("sources", "notes", "s4", "s4_sources") or isinstance(v, (list, dict)):
                continue
            if k not in df.columns:
                df[k] = None
            df[k] = df[k].astype(object)
            df.loc[idx, k] = v
    return df


def run(top_n: int = 60, n_final: int = 15) -> dict:
    cfg = load_cfg()
    out = os.path.join(ROOT, "outputs")
    os.makedirs(out, exist_ok=True)

    uni = load_universe(os.path.join(ROOT, "cache"))
    uni["mcap_band"] = uni["mcap_cr"].map(mcap_band)
    kept, excluded = apply_filters(uni, cfg)
    ctx = Context.from_frame(kept)
    scored = score_frame(kept, cfg, ctx)

    uni.to_csv(os.path.join(out, "universe.csv"), index=False)
    excluded.to_csv(os.path.join(out, "excluded.csv"), index=False)
    scored.to_csv(os.path.join(out, "scores.csv"), index=False)
    top = scored.head(top_n).copy()
    top.to_csv(os.path.join(out, "top60.csv"), index=False)
    pd.DataFrame(missing_field_log()).to_csv(os.path.join(out, "field_map.csv"), index=False)

    result = {"universe": len(uni), "excluded": len(excluded), "scored": len(scored)}

    ov_path = os.path.join(ROOT, "cache", "stage3_overrides.json")
    if os.path.exists(ov_path):
        with open(ov_path) as fh:
            overrides = json.load(fh)
        base_cols = [c for c in top.columns if not c.startswith("s_") and c not in (
            "base_score", "red_flag_deduction", "red_flags", "n_red_flags", "score", "peg",
            "industry_pe", "cfo_to_pat", "boring", "rank")]
        top_in = apply_overrides(top[base_cols], overrides)
        # Stage 3 drops: anything research marked as excluded
        drop = top_in.get("stage3_exclude")
        if drop is not None:
            dropped = top_in[drop.fillna(False).astype(bool)]
            top_in = top_in[~drop.fillna(False).astype(bool)]
            result["stage3_dropped"] = len(dropped)
            dropped.to_csv(os.path.join(out, "stage3_dropped.csv"), index=False)
        rescored = score_frame(top_in, cfg, ctx)
        rescored.to_csv(os.path.join(out, "rescored_top60.csv"), index=False)
        finalists = rescored.head(n_final).copy()
        result["finalists"] = len(finalists)

        # Stage 4: deep-research overrides refine the finalists' inputs and re-rank them
        s4_path = os.path.join(ROOT, "cache", "stage4_overrides.json")
        if os.path.exists(s4_path):
            with open(s4_path) as fh:
                s4 = json.load(fh)
            from .memo_content import MEMOS
            for sym, memo in MEMOS.items():
                s4.setdefault(sym, {}).update(
                    product_score=memo["product_score"], headroom=memo["headroom"])
            score_outputs = {"base_score", "red_flag_deduction", "red_flags", "n_red_flags", "score",
                             "peg", "industry_pe", "cfo_to_pat", "boring", "rank"}
            keep = [c for c in finalists.columns if not c.startswith("s_") and c not in score_outputs]
            fin_in = apply_overrides(finalists[keep], s4)
            for extra in ("sales_g_yoy", "pat_g_yoy"):
                if extra in fin_in.columns:
                    fin_in[extra] = pd.to_numeric(fin_in[extra], errors="coerce")
            finalists = score_frame(fin_in, cfg, ctx)
        finalists.to_csv(os.path.join(out, "finalists.csv"), index=False)
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

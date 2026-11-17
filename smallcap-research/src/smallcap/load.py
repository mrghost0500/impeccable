"""Load cached screener pages into one de-duplicated universe table.

Each cache file under cache/screener_pages/ is a pipe-separated projection of a
stockanalysis.com India screener page (fetched through the Firecrawl Alexandria
connector). Money is in Rs crore, ratios in percent, D/E as a multiple.
"""
from __future__ import annotations

import glob
import os
import re

import pandas as pd

BASE_COLUMNS = [
    "symbol", "name", "industry", "sector", "mcap_cr", "price", "pe", "roe", "roce",
    "opm", "sales_cr", "sales_g3y", "pat_cr", "pat_g3y", "de", "promoter_pct",
    "inst_pct", "ebit_cr", "bse_code",
]

SUPPLEMENT_COLUMNS = [
    "symbol", "cfo_cr", "pbt_cr", "capex_cr", "ebitda_cr", "ret_1y", "pat_g_yoy",
    "sales_g_yoy", "shares_yoy", "roic",
]

NUMERIC = [
    "mcap_cr", "price", "pe", "roe", "roce", "opm", "sales_cr", "sales_g3y", "pat_cr",
    "pat_g3y", "de", "promoter_pct", "inst_pct", "ebit_cr",
]

# Fields the Screener.in export would carry that this source does not provide.
EXPECTED_FIELDS = {
    "Name": "name",
    "NSE/BSE code": "symbol",
    "Market Cap": "mcap_cr",
    "P/E": "pe",
    "PEG": "peg (computed: P/E / 3Y profit CAGR)",
    "ROCE": "roce",
    "ROE": "roe",
    "OPM": "opm",
    "Sales growth 3Y": "sales_g3y",
    "Profit growth 3Y": "pat_g3y",
    "Debt/Equity": "de",
    "Promoter holding": "promoter_pct (insider holding proxy)",
    "Change in promoter holding 3Y": None,
    "Pledged %": None,
    "FII %": "inst_pct (FII + DII combined only)",
    "DII %": "inst_pct (FII + DII combined only)",
    "No. of shareholders": None,
    "CFO last year": "cfo_cr (supplement)",
    "Net profit": "pat_cr",
    "1Y return": "ret_1y (supplement, often missing)",
}


def _norm_name(name: str) -> str:
    n = name.lower()
    n = re.sub(r"\b(limited|ltd\.?)\b", "", n)
    n = re.sub(r"[^a-z0-9]+", " ", n)
    return n.strip()


def parse_symbol(sym: str) -> dict:
    exch, code = sym.split(":", 1)
    if exch == "N":
        return {
            "exchange": "NSE", "ticker": code, "yahoo": f"{code}.NS",
            "stockanalysis_url": f"https://stockanalysis.com/quote/nse/{code}/",
            "screener_url": f"https://www.screener.in/company/{code}/",
        }
    return {
        "exchange": "BSE", "ticker": code, "yahoo": f"{code}.BO",
        "stockanalysis_url": f"https://stockanalysis.com/quote/bom/{code}/",
        "screener_url": f"https://www.screener.in/company/{code}/",
    }


def read_pages(pattern: str) -> pd.DataFrame:
    rows = []
    for path in sorted(glob.glob(pattern)):
        page = os.path.basename(path)
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if not line:
                    continue
                parts = line.split("|")
                parts += [""] * (len(BASE_COLUMNS) - len(parts))
                rec = dict(zip(BASE_COLUMNS, parts[: len(BASE_COLUMNS)]))
                rec["source_page"] = page
                rows.append(rec)
    df = pd.DataFrame(rows)
    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col].replace("", None), errors="coerce")
    for col in ("industry", "sector", "bse_code"):
        df[col] = df[col].fillna("").astype(str)
    return df


def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    """Keep one row per company, preferring the NSE listing."""
    df = df.copy()
    df["_key"] = df["name"].map(_norm_name)
    df["_nse"] = df["symbol"].str.startswith("N:")
    df = df.sort_values(["_key", "_nse", "mcap_cr"], ascending=[True, False, False])
    keep = df.drop_duplicates("_key", keep="first").copy()
    # carry a BSE code over from the dropped duplicate when the NSE row lacks one
    bse_map = (
        df[~df["_nse"]].assign(code=lambda d: d["symbol"].str.split(":").str[1])
        .groupby("_key")["code"].first()
    )
    missing = keep["bse_code"].eq("") & keep["_nse"]
    keep.loc[missing, "bse_code"] = keep.loc[missing, "_key"].map(bse_map).fillna("")
    return keep.drop(columns=["_key", "_nse"]).reset_index(drop=True)


def attach_links(df: pd.DataFrame) -> pd.DataFrame:
    meta = df["symbol"].map(parse_symbol).apply(pd.Series)
    return pd.concat([df.reset_index(drop=True), meta.reset_index(drop=True)], axis=1)


def read_supplement(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame(columns=SUPPLEMENT_COLUMNS)
    sup = pd.read_csv(path, sep="|", names=SUPPLEMENT_COLUMNS, dtype={"symbol": str})
    for col in SUPPLEMENT_COLUMNS[1:]:
        sup[col] = pd.to_numeric(sup[col], errors="coerce")
    return sup.drop_duplicates("symbol")


def load_universe(cache_dir: str) -> pd.DataFrame:
    raw = read_pages(os.path.join(cache_dir, "screener_pages", "*.psv"))
    uni = attach_links(dedupe(raw))
    sup = read_supplement(os.path.join(cache_dir, "supplement.psv"))
    if len(sup):
        uni = uni.merge(sup, on="symbol", how="left")
    else:
        for col in SUPPLEMENT_COLUMNS[1:]:
            uni[col] = float("nan")
    return uni


def missing_field_log() -> list[dict]:
    return [
        {"expected": k, "mapped_to": v or "NOT AVAILABLE", "status": "ok" if v else "missing"}
        for k, v in EXPECTED_FIELDS.items()
    ]

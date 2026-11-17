"""Stage 1 noise filter. Every exclusion carries a reason string."""
from __future__ import annotations

import math
import re

import pandas as pd


def _isnum(x) -> bool:
    return x is not None and not (isinstance(x, float) and math.isnan(x))


def other_income_share(pbt, ebit):
    """Lower bound on other income as a share of PBT.

    PBT = EBIT - interest + other income, so other income >= PBT - EBIT.
    Returns None when the inputs are missing or PBT <= 0.
    """
    if not (_isnum(pbt) and _isnum(ebit)) or pbt <= 0:
        return None
    return max(0.0, (pbt - ebit) / pbt)


def exclusion_reasons(row: dict, cfg: dict) -> list[str]:
    f = cfg["filters"]
    reasons: list[str] = []
    name = str(row.get("name", ""))
    industry = str(row.get("industry", ""))

    opm = row.get("opm")
    if _isnum(opm) and abs(opm) > f["max_abs_opm_pct"]:
        reasons.append(f"data anomaly: OPM {opm:.0f}% (verify by hand)")

    for pat in f["financial_industry_patterns"]:
        if pat.lower() in industry.lower():
            reasons.append(f"financial/holding company ({industry}): lenses not applicable")
            break
    for pat in f["holding_name_patterns"]:
        if re.search(pat, name, flags=re.I):
            reasons.append("holding company / trust by name")
            break

    sales = row.get("sales_cr")
    if not _isnum(sales):
        reasons.append("no sales data")
    elif sales < f["min_sales_cr"]:
        reasons.append(f"sales Rs {sales:.0f} Cr < {f['min_sales_cr']} Cr")

    price = row.get("price")
    if _isnum(price) and price < f["min_price"]:
        reasons.append(f"price Rs {price:.1f} < Rs {f['min_price']}")

    pat, ebit = row.get("pat_cr"), row.get("ebit_cr")
    if _isnum(pat) and _isnum(ebit) and pat < 0 and ebit < 0:
        reasons.append("operating loss and net loss (TTM)")

    # one-off profit spike. Prefer YoY growth; fall back to 3Y CAGR.
    g_yoy, s_yoy = row.get("pat_g_yoy"), row.get("sales_g_yoy")
    g3, s3 = row.get("pat_g3y"), row.get("sales_g3y")
    if _isnum(g_yoy) and g_yoy > f["one_off_profit_growth_pct"] and (
        not _isnum(s_yoy) or s_yoy < f["one_off_max_sales_growth_pct"]
    ):
        reasons.append(f"one-off: profit +{g_yoy:.0f}% YoY on sales {s_yoy if _isnum(s_yoy) else 'n/a'}%")
    elif _isnum(g3) and g3 > f["one_off_3y_cagr_pct"] and (
        not _isnum(s3) or s3 < f["one_off_max_sales_growth_pct"]
    ):
        reasons.append(f"one-off: profit 3Y CAGR {g3:.0f}% on sales CAGR {s3 if _isnum(s3) else 'n/a'}%")

    share = other_income_share(row.get("pbt_cr"), ebit)
    if share is not None and share > f["max_other_income_share_of_pbt"]:
        reasons.append(f"other income >= {share:.0%} of PBT")
    elif not _isnum(row.get("pbt_cr")) and _isnum(pat) and _isnum(ebit) and ebit > 0 and pat > 1.3 * ebit:
        # no PBT available: net profit well above operating profit implies non-operating income
        reasons.append("net profit > 1.3x operating profit (other income / one-off)")

    return reasons


def apply_filters(df: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    reasons = df.apply(lambda r: exclusion_reasons(r.to_dict(), cfg), axis=1)
    mask = reasons.map(len) == 0
    kept = df[mask].copy()
    excluded = df[~mask].copy()
    excluded["exclusion_reasons"] = reasons[~mask].map("; ".join)
    return kept, excluded

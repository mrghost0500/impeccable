"""Render one Markdown memo per finalist into memos/."""
from __future__ import annotations

import json
import math
import os

import pandas as pd

from .memo_content import MEMOS

_cpath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "outputs", "council.json")
COUNCIL = {k: v for k, v in json.load(open(_cpath)).items() if not k.startswith("_")} if os.path.exists(_cpath) else {}

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXIT_PE = 20.0
YEARS = 5


def _num(x, fmt="{:,.1f}", na="n/a"):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return na
    return fmt.format(x)


def earnings_table(mcap: float, fy26_pat: float, scen: tuple) -> dict:
    out = {"scenarios": {}, "required": {}}
    for label, pat in zip(("Bear", "Base", "Bull"), scen):
        out["scenarios"][label] = {"fy28_pat": pat, "implied_pe": mcap / pat if pat > 0 else None,
                                   "cagr_vs_fy26": (pat / fy26_pat) ** 0.5 - 1 if fy26_pat > 0 else None}
    cur_pe = mcap / fy26_pat if fy26_pat > 0 else None
    for m in (3, 5, 10):
        need_exit20 = m * mcap / EXIT_PE
        out["required"][m] = {
            "pat_needed_exit20": need_exit20,
            "cagr_exit20": (need_exit20 / fy26_pat) ** (1 / YEARS) - 1 if fy26_pat > 0 else None,
            "cagr_const_pe": m ** (1 / YEARS) - 1,
        }
    out["current_pe_fy26"] = cur_pe
    return out


def render(row: pd.Series, s3: dict, s4: dict, memo: dict) -> str:
    sym, name = row["symbol"], row["name"]
    et = earnings_table(row["mcap_cr"], memo["fy26_pat"], memo["scen"])
    srcs = list(dict.fromkeys((s3.get("sources") or []) + (s4.get("s4_sources") or []) + [row["stockanalysis_url"], row["screener_url"]]))
    L = []
    L.append(f"# {name} ({row['exchange']}: {row['ticker']})\n")
    L.append("> Research memo, not investment advice. Figures are from secondary aggregators and company releases found by web search in Nov 2026; anything marked *unverified* has not been checked against filings.\n")
    L.append(f"**Composite score {row['score']:.2f}/10** (rank {int(row['rank'])} of the finalists) · market cap Rs {row['mcap_cr']:,.0f} Cr · {row['industry']}\n")
    L.append("## 1. Two-minute drill\n")
    L.append(memo["drill"] + "\n")
    L.append("## 2. Numbers\n")
    L.append("| Metric | Value | Basis |\n|---|---|---|")
    L.append(f"| Revenue FY26 | Rs {memo['fy26_rev']:,.0f} Cr | company release (see sources) |")
    L.append(f"| PAT FY26 | Rs {memo['fy26_pat']:,.1f} Cr | company release |")
    L.append(f"| Revenue TTM / PAT TTM | Rs {_num(row['sales_cr'], '{:,.0f}')} Cr / Rs {_num(row['pat_cr'])} Cr | stockanalysis.com screener |")
    L.append(f"| P/E (as scored) / P/E on FY26 PAT | {_num(row['pe'])} / {_num(et['current_pe_fy26'])} | |")
    L.append(f"| PEG (P/E / 3Y profit CAGR) | {_num(row['peg'], '{:.2f}')} | 3Y profit CAGR {_num(row['pat_g3y'])}% |")
    L.append(f"| Sales CAGR 3Y / YoY | {_num(row['sales_g3y'])}% / {_num(row.get('sales_g_yoy'))}% | |")
    L.append(f"| ROCE / ROE / OPM | {_num(row['roce'])}% / {_num(row['roe'])}% / {_num(row['opm'])}% | TTM |")
    L.append(f"| Debt/Equity | {_num(row['de'], '{:.2f}')} | |")
    L.append(f"| CFO used / CFO-to-PAT | {_num(row.get('cfo_cr'))} Cr / {_num(row.get('cfo_to_pat'), '{:.2f}')} | Stage 3 research; period noted in sources |")
    L.append(f"| Promoter / FII+DII | {_num(row['promoter_pct'])}% / {_num(row['inst_pct'])}% | exchange-filing aggregators |")
    L.append("\n**10-year history: not verified.** Screener.in and the exchanges were not reachable from this environment, so the 10-year sales, profit and ROCE series is still missing. Pull it from the Screener page in the sources before relying on this memo.\n")
    if s3.get("notes"):
        L.append(f"*Stage 3 notes:* {s3['notes']}\n")
    if s4.get("s4"):
        L.append(f"*Stage 4 notes:* {s4['s4']}\n")
    L.append("## 3. Thinking ladder\n")
    for i, step in enumerate(memo["ladder"], 1):
        L.append(f"{i}. {step}")
    L.append("\n## 4. Customer and product angle\n")
    L.append(memo["customer"] + f"\n\n*Provisional product score (desk-based, product not tried): {memo['product_score']}/10.*\n")
    L.append("## 5. PE/VC view\n")
    L.append(memo["pevc"] + f"\n\n*Headroom score: {memo['headroom']}/10.*\n")
    L.append("## 6. Red flags\n")
    for f in memo["flags"]:
        L.append(f"- {f}")
    if isinstance(row.get("red_flags"), str) and row["red_flags"]:
        L.append(f"- Scoring deductions applied: {row['red_flags']}")
    L.append("\n## 7. Earnings potential (FY28 = FY+2)\n")
    L.append("| Scenario | FY28 PAT (Rs Cr) | Implied P/E at today's price | PAT CAGR vs FY26 |\n|---|---|---|---|")
    for lab, v in et["scenarios"].items():
        L.append(f"| {lab} | {v['fy28_pat']:,.0f} | {_num(v['implied_pe'])} | {_num(v['cagr_vs_fy26'] * 100 if v['cagr_vs_fy26'] is not None else None)}% |")
    L.append(f"\n*Basis:* {memo['scenario_basis']}\n")
    L.append(f"**Growth needed over {YEARS} years** (from FY26 PAT of Rs {memo['fy26_pat']:,.1f} Cr):\n")
    L.append("| Outcome | PAT needed at exit P/E 20 | PAT CAGR needed (exit P/E 20) | CAGR needed if P/E stays constant |\n|---|---|---|---|")
    for m, v in et["required"].items():
        L.append(f"| {m}x | Rs {v['pat_needed_exit20']:,.0f} Cr | {v['cagr_exit20'] * 100:.1f}% | {v['cagr_const_pe'] * 100:.1f}% |")
    L.append("\n## 8. Who has caught on\n")
    L.append(f"Institutional (FII+DII) holding is {_num(row['inst_pct'])}%; promoter {_num(row['promoter_pct'])}%. "
             "Shareholder-count trend and 1-year price trend were **not retrieved**: the 1Y-return supplement was not fetched because the data-connector credits ran out. Check the latest shareholding pattern (number of shareholders) on BSE/NSE.\n")
    council = COUNCIL.get(row["ticker"])
    if council:
        L.append("## Council verdict (Stage 5)\n")
        L.append(f"**Chairman score {council['chairman_score']:.2f}/10.** {council['verdict']}\n")
        L.append("| Member | Score | Reason |\n|---|---|---|")
        for mem, sc in council["member_scores"].items():
            L.append(f"| {mem} | {sc} | {council['member_reasons'][mem]} |")
        L.append(f"\n*Main disagreement:* {council['main_disagreement']}\n")
    L.append("## Sources\n")
    for u in srcs:
        L.append(f"- <{u}>")
    return "\n".join(L) + "\n"


def write_all() -> list[str]:
    fin = pd.read_csv(os.path.join(ROOT, "outputs", "finalists.csv"))
    s3 = json.load(open(os.path.join(ROOT, "cache", "stage3_overrides.json")))
    s4 = json.load(open(os.path.join(ROOT, "cache", "stage4_overrides.json")))
    os.makedirs(os.path.join(ROOT, "memos"), exist_ok=True)
    paths = []
    for _, row in fin.iterrows():
        memo = MEMOS.get(row["symbol"])
        if memo is None:
            continue
        fn = f"{int(row['rank']):02d}_{row['ticker']}.md"
        path = os.path.join(ROOT, "memos", fn)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(row, s3.get(row["symbol"], {}), s4.get(row["symbol"], {}), memo))
        paths.append(path)
    return paths


if __name__ == "__main__":
    for p in write_all():
        print(p)

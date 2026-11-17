"""Render FINAL_LIST.md from outputs/final_list.csv and final_detail.json."""
from __future__ import annotations

import json
import os

import pandas as pd

from .final_content import FINAL
from .memo_content import MEMOS
from .pipeline import load_cfg

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "outputs")

FLAG_TEXT = {
    "cfo_gap": "operating cash flow not verified",
    "weak_cash": "weak or negative cash conversion",
    "policy": "earnings tied to a policy-set price, subsidy scheme or commodity",
    "concentration": "one customer, country or programme dominates",
    "governance": "governance or listing risk (SME, related parties, pledge, promoter selling, audit)",
    "stalling": "growth slowing in the latest data",
    "order_cover": "order book of 1.5x+ revenue",
    "cash_verified": "verified cash conversion of 0.8x+",
    "momentum": "latest quarter profit up 25%+",
}


def _pct(x):
    return f"{x * 100:.0f}%"


def render() -> str:
    cfg = load_cfg()["projections"]
    df = pd.read_csv(os.path.join(OUT, "final_list.csv"), dtype={"ticker": str})
    det = json.load(open(os.path.join(OUT, "final_detail.json")))
    L = ["# Final list: 25 Indian small caps\n",
         "> Research, not investment advice. Nothing here is a buy or sell call. Projections are scenario estimates built from secondary sources and stated assumptions; the probabilities are rule-based judgements, not statistical forecasts.\n",
         "## How to read this\n",
         "- **Tier A (1-15)** went through the full process: screen, web research, memo, comparables and the four-member council. They are ordered by council score.",
         "- **Tier B (16-25)** are the next ten on the Stage 3 list. They have web research and FY26 results, but no memo or council review. They are ordered by screen score.",
         "- **Lynch category** follows *One Up on Wall Street*: slow grower, stalwart, fast grower, cyclical, turnaround or asset play.",
         "- **Projections** are FY28 (two years out) net profit in three scenarios.",
         "- **Probabilities** start at 25% bear / 50% base / 25% bull. Each piece of evidence then moves 5 points between bear and bull:",
         "  - Against: unverified cash flow, weak cash conversion, dependence on a policy-set price or commodity, one dominant customer or country, governance or listing risk, slowing growth.",
         "  - For: an order book of 1.5x revenue or more, verified cash conversion, and latest-quarter profit up more than 25%.",
         f"- **PE-style outcome:** value in about {cfg['horizon_years']} years is FY28 profit times an exit P/E. The exit P/E is {cfg['bear_derate']}x the lower of today's and the peers' P/E (bear), their midpoint (base) or the higher of the two (bull), capped at {cfg['exit_pe_cap']}x.",
         "- **MOIC** is that value divided by today's market cap, ignoring dividends, dilution and cash. **IRR** is the annualised return on the probability-weighted MOIC.\n",
         "## The list\n",
         "| # | Tier | Company | Lynch category | Mcap (Rs Cr) | P/E FY26 | Peer P/E | FY28 PAT bear / base / bull | Probabilities | Expected FY28 PAT | Expected MOIC (IRR) | P(loss) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in df.itertuples():
        L.append(f"| {r.final_rank} | {r.tier} | {r.name} | {r.lynch} | {r.mcap_cr:,} | {r.pe_fy26:.1f}x | {r.peer_pe:.1f}x | "
                 f"{r.pat_bear:,.0f} / {r.pat_base:,.0f} / {r.pat_bull:,.0f} | {_pct(r.p_bear)} / {_pct(r.p_base)} / {_pct(r.p_bull)} | "
                 f"{r.exp_fy28_pat:,.0f} ({r.exp_pat_cagr:+.0f}%/yr) | {r.exp_moic:.2f}x ({r.exp_irr_pct:+.0f}%) | {_pct(r.p_loss)} |")
    L.append("\n*FY28 PAT in Rs crore. Expected PAT growth is the annualised change from FY26 audited PAT.*\n")

    for r in df.itertuples():
        spec = FINAL[r.ticker]
        d = det[r.ticker]
        L.append(f"## {r.final_rank}. {r.name} ({r.ticker})\n")
        sub = f"Tier {r.tier} · {r.industry} · market cap Rs {r.mcap_cr:,} Cr · screen score {r.screen_score:.2f}"
        if r.tier == "A":
            sub += f" · council score {r.council_score:.2f}"
        L.append(sub + "\n")
        L.append(f"### The story (Lynch: {r.lynch})\n")
        L.append(spec["story"] + "\n")
        L.append("### The case to a PE/VC firm\n")
        L.append(spec["pe_case"] + "\n")
        L.append("### Projections and probabilities\n")
        L.append("| Scenario | Probability | FY28 PAT (Rs Cr) | PAT growth/yr vs FY26 | Exit P/E | Implied value (Rs Cr) | MOIC | IRR |\n|---|---|---|---|---|---|---|---|")
        for row in d["rows"]:
            L.append(f"| {row['scenario']} | {_pct(row['prob'])} | {row['fy28_pat']:,.0f} | {round(row['pat_cagr'] * 100) + 0:+d}% | {row['exit_pe']:.1f}x | "
                     f"{row['value_cr']:,.0f} | {row['moic']:.2f}x | {row['irr'] * 100:+.0f}% |")
        L.append(f"| **Expected** | | **{r.exp_fy28_pat:,.0f}** | {r.exp_pat_cagr:+.0f}% | | | **{r.exp_moic:.2f}x** | **{r.exp_irr_pct:+.0f}%** |")
        basis = MEMOS[r.symbol]["scenario_basis"] if r.tier == "A" else None
        if basis:
            L.append(f"\n*Scenario basis:* {basis}")
        moves = []
        for code in d["reasons"]:
            sign, flag = code[0], code[1:]
            moves.append(("towards bear: " if sign == "-" else "towards bull: ") + FLAG_TEXT[flag])
        L.append("\n*Why these probabilities:* start at 25/50/25; " + ("; ".join(moves) if moves else "no evidence flags, prior kept") +
                 f". Result {_pct(r.p_bear)} / {_pct(r.p_base)} / {_pct(r.p_bull)}. "
                 f"P(MOIC < 1x) = {_pct(r.p_loss)}; P(MOIC >= 1.5x) = {_pct(r.p_moic_1_5x)}.\n")
        if r.tier == "A":
            idx = int(pd.read_csv(os.path.join(OUT, 'finalists.csv'), dtype={'ticker': str}).set_index('ticker').loc[r.ticker, 'rank'])
            L.append(f"*Full memo:* `memos/{idx:02d}_{r.ticker}.md` (numbers, thinking ladder, comparables, council verdict, sources).\n")
        else:
            L.append("*Sources:* " + " · ".join(f"<{u}>" for u in spec.get("sources", [])) + "\n")
    L.append("## Caveats\n")
    L.append("- **Scenario inputs:** FY28 profits are analyst scenarios, not company guidance. Where a company gives guidance, the base case references it.")
    L.append("- **Probabilities:** a transparent scoring rule (prior plus evidence flags), not a fitted statistical model. Change `projections` in `config.yaml` to test other assumptions.")
    L.append("- **Exit multiples:** the result is sensitive to them. Peer P/E is the curated peer median for Tier A and the screen's industry median for Tier B, which is rougher.")
    L.append("- **Missing data:** cash flow is unverified for many names, and no 10-year histories were checked.")
    L.append("- **Supreme Power's FY26 profit:** estimated from TTM and half-year data, because audited FY26 figures were not found.")
    return "\n".join(L) + "\n"


def write() -> str:
    path = os.path.join(ROOT, "FINAL_LIST.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(render())
    return path


if __name__ == "__main__":
    print(write())

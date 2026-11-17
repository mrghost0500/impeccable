"""Stage 6A: write outputs/research.xlsx."""
from __future__ import annotations

import json
import os

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "outputs")
HEAD_FILL = PatternFill("solid", fgColor="1F3A5F")
HEAD_FONT = Font(bold=True, color="FFFFFF")

UNIVERSE_COLS = ["symbol", "name", "exchange", "ticker", "bse_code", "industry", "sector", "mcap_cr", "mcap_band",
                 "price", "pe", "roe", "roce", "opm", "sales_cr", "sales_g3y", "pat_cr", "pat_g3y", "de",
                 "promoter_pct", "inst_pct", "ebit_cr", "yahoo", "stockanalysis_url", "screener_url", "source_page"]
SCORE_COLS = ["rank", "symbol", "name", "industry", "mcap_cr", "pe", "peg", "industry_pe", "roce", "roe", "opm",
              "sales_g3y", "pat_g3y", "de", "promoter_pct", "inst_pct", "cfo_to_pat", "boring",
              "s_lynch", "s_mayer", "s_buffett_fisher", "s_kirby_mukherjea", "s_pe_vc", "s_lynch_product",
              "base_score", "red_flag_deduction", "n_red_flags", "red_flags", "score"]
NUMFMT = {"mcap_cr": "#,##0", "sales_cr": "#,##0", "pat_cr": "#,##0.0", "ebit_cr": "#,##0.0", "price": "#,##0.0",
          "pe": "0.0", "peg": "0.00", "de": "0.00", "cfo_to_pat": "0.00", "score": "0.00", "base_score": "0.00",
          "chairman_score": "0.00"}


def _sheet(wb, title, df, widths=None, link_cols=()):
    ws = wb.create_sheet(title)
    cols = list(df.columns)
    ws.append(cols)
    for c in ws[1]:
        c.fill, c.font = HEAD_FILL, HEAD_FONT
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for row in df.itertuples(index=False):
        ws.append([None if (isinstance(v, float) and pd.isna(v)) else (v.item() if hasattr(v, "item") else v) for v in row])
    for j, col in enumerate(cols, 1):
        letter = get_column_letter(j)
        ws.column_dimensions[letter].width = (widths or {}).get(col, max(10, min(40, len(col) + 4)))
        fmt = NUMFMT.get(col) or ("0.0" if col.startswith("s_") else None)
        if fmt:
            for cell in ws[letter][1:]:
                cell.number_format = fmt
        if col in link_cols:
            for cell in ws[letter][1:]:
                if isinstance(cell.value, str) and cell.value.startswith("http"):
                    cell.hyperlink = cell.value
                    cell.font = Font(color="0563C1", underline="single")
    ws.freeze_panes = "C2" if len(cols) > 3 else "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def build() -> str:
    uni = pd.read_csv(os.path.join(OUT, "universe.csv"))
    exc = pd.read_csv(os.path.join(OUT, "excluded.csv"))
    scores = pd.read_csv(os.path.join(OUT, "scores.csv"))
    top = pd.read_csv(os.path.join(OUT, "rescored_top60.csv"))
    fin = pd.read_csv(os.path.join(OUT, "finalists.csv"))
    council = json.load(open(os.path.join(OUT, "council.json")))
    s3 = json.load(open(os.path.join(ROOT, "cache", "stage3_overrides.json")))
    s4 = json.load(open(os.path.join(ROOT, "cache", "stage4_overrides.json")))

    wb = Workbook()
    wb.remove(wb.active)

    _sheet(wb, "Universe", uni[[c for c in UNIVERSE_COLS if c in uni.columns]],
           {"name": 34, "industry": 30}, link_cols=("stockanalysis_url", "screener_url"))

    exc_out = exc[["symbol", "name", "industry", "mcap_cr", "sales_cr", "price", "pat_cr", "ebit_cr", "exclusion_reasons"]].copy()
    exc_out.insert(0, "stage", "Stage 1 noise filter")
    d3 = os.path.join(OUT, "stage3_dropped.csv")
    if os.path.exists(d3):
        dd = pd.read_csv(d3)
        dd = dd.assign(stage="Stage 3 research", exclusion_reasons=dd["symbol"].map(lambda s: s3.get(s, {}).get("notes", "")))
        exc_out = pd.concat([exc_out, dd[exc_out.columns]], ignore_index=True)
    _sheet(wb, "Excluded", exc_out, {"name": 34, "industry": 28, "exclusion_reasons": 90})

    _sheet(wb, "Scores", scores[[c for c in SCORE_COLS if c in scores.columns]], {"name": 34, "industry": 28, "red_flags": 50})

    top_out = top[[c for c in SCORE_COLS if c in top.columns]].copy()
    top_out["stage3_notes"] = top["symbol"].map(lambda s: s3.get(s, {}).get("notes", ""))
    _sheet(wb, "Top60", top_out, {"name": 34, "industry": 28, "red_flags": 45, "stage3_notes": 100})

    fin_out = fin[[c for c in SCORE_COLS if c in fin.columns] + [c for c in ("sales_g_yoy", "pat_g_yoy", "cfo_cr") if c in fin.columns]].copy()
    fin_out["council_score"] = fin["ticker"].map(lambda t: council.get(str(t), {}).get("chairman_score"))
    fin_out["council_verdict"] = fin["ticker"].map(lambda t: council.get(str(t), {}).get("verdict"))
    fin_out["stage4_notes"] = fin["symbol"].map(lambda s: s4.get(s, {}).get("s4", ""))
    fin_out["memo"] = fin.apply(lambda r: f"memos/{int(r['rank']):02d}_{r['ticker']}.md", axis=1)
    fin_out = fin_out.sort_values("council_score", ascending=False)
    _sheet(wb, "Finalists", fin_out, {"name": 30, "industry": 26, "red_flags": 40, "council_verdict": 80, "stage4_notes": 100, "memo": 28})

    rows = []
    for t, v in council.items():
        if t.startswith("_"):
            continue
        r = {"ticker": t, "chairman_score": v["chairman_score"]}
        for m, sc in v["member_scores"].items():
            r[f"{m}_score"] = sc
        r["spread"] = v["spread"]
        r["verdict"] = v["verdict"]
        r["main_disagreement"] = v["main_disagreement"]
        for m, rs in v["member_reasons"].items():
            r[f"{m}_reason"] = rs
        rows.append(r)
    cdf = pd.DataFrame(rows).sort_values("chairman_score", ascending=False)
    ws = _sheet(wb, "Council", cdf, {"verdict": 70, "main_disagreement": 70, "rigorous_reason": 60,
                                     "pragmatist_reason": 60, "contrarian_reason": 60, "plain_reason": 60})
    meta = council["_meta"]
    base = len(cdf) + 3
    ws.cell(base, 1, "Method").font = Font(bold=True)
    ws.cell(base, 2, meta["method"])
    ws.cell(base + 1, 1, "Peer rank (avg, n)").font = Font(bold=True)
    for i, (m, (avg, n)) in enumerate(sorted(meta["peer_rank"].items(), key=lambda x: x[1][0])):
        ws.cell(base + 2 + i, 1, m)
        ws.cell(base + 2 + i, 2, avg)
        ws.cell(base + 2 + i, 3, n)
    ws.cell(base + 7, 1, "Chairman corrections").font = Font(bold=True)
    for i, c in enumerate(meta["chairman_corrections"]):
        ws.cell(base + 8 + i, 2, c)

    src = [{"symbol": "ALL", "name": "Universe data", "stage": "Stage 0",
            "url": "https://stockanalysis.com/stocks/screener/", "note": "stockanalysis.com India screener via Firecrawl Alexandria connector (Nov 17, 2026)"}]
    names = dict(zip(top["symbol"], top["name"]))
    for sym, f in s3.items():
        for u in f.get("sources", []):
            src.append({"symbol": sym, "name": names.get(sym, ""), "stage": "Stage 3", "url": u, "note": ""})
    for sym, f in s4.items():
        for u in f.get("s4_sources", []):
            src.append({"symbol": sym, "name": names.get(sym, ""), "stage": "Stage 4", "url": u, "note": ""})

    fl = os.path.join(OUT, "final_list.csv")
    if os.path.exists(fl):
        _sheet(wb, "Final25", pd.read_csv(fl, dtype={"ticker": str}),
               {"name": 30, "industry": 26, "lynch": 24, "prob_drivers": 40, "story": 90, "pe_case": 90})

    cp = os.path.join(OUT, "comparables_peers.csv")
    if os.path.exists(cp):
        peers = pd.read_csv(cp, dtype={"finalist_ticker": str, "ticker": str})
        cols = ["finalist", "role", "peer", "ticker", "mcap_cr", "pe", "roce", "opm", "sales_g3y", "pat_g3y", "de", "note", "source", "url"]
        _sheet(wb, "Comparables", peers[[c for c in cols if c in peers.columns]],
               {"finalist": 30, "peer": 32, "note": 50, "source": 30, "url": 55}, link_cols=("url",))
        gap = pd.read_csv(os.path.join(OUT, "valuation_gap.csv"), dtype={"ticker": str})
        _sheet(wb, "ValuationGap", gap, {"finalist": 30, "competitors": 70, "positioning": 70, "valuation_gap": 90})
        for u, n in peers[["url", "peer"]].dropna().drop_duplicates("url").itertuples(index=False):
            if "stockanalysis.com/quote" not in u:
                src.append({"symbol": "", "name": n, "stage": "Comparables", "url": u, "note": "peer valuation snapshot"})

    sp = os.path.join(OUT, "spotcheck.csv")
    if os.path.exists(sp):
        _sheet(wb, "SpotCheck", pd.read_csv(sp), {"name": 26, "our_value (Rs Cr / %)": 50, "source_value": 60,
                                                 "result": 50, "source_url": 60}, link_cols=("source_url",))

    _sheet(wb, "Sources", pd.DataFrame(src), {"name": 32, "url": 90, "note": 60}, link_cols=("url",))

    notes = pd.read_csv(os.path.join(OUT, "field_map.csv"))
    ws = _sheet(wb, "Notes", notes, {"expected": 32, "mapped_to": 45})
    caveats = [
        "Research only, not investment advice. No row is a buy or sell call.",
        "Universe: stockanalysis.com India screener, ranks 1,750-3,750 by market cap (~Rs 4,550 Cr down to ~Rs 570 Cr), NSE listing preferred over BSE duplicates.",
        "Screener.in CSV was not supplied; yfinance, NSE archives and Screener.in were blocked by the session's network policy.",
        "Feed 'insider %' is used as the promoter-holding proxy and 'institutions %' as FII+DII; Stage 3 found both often wrong and replaced them for the top 60.",
        "Supplementary fields (CFO, PBT, capex, 1Y return) could not be fetched for the full universe after Firecrawl credits ran out; Stage 1 other-income check uses a net-profit > 1.3x operating-profit proxy.",
        "CFO/PAT often divides latest-FY CFO by TTM PAT, so it is indicative only.",
        "Comparables: peer medians use P/E between 3x and 100x; larger peers are web-search snapshots (dated) and approximate. The fundamentals-implied P/E model explains ~17% of P/E variation (see outputs/pe_model.json): a weak cross-check.",
    ]
    for i, c in enumerate(caveats):
        ws.cell(len(notes) + 3 + i, 1, c)

    path = os.path.join(OUT, "research.xlsx")
    wb.save(path)
    return path


if __name__ == "__main__":
    print(build())

# Indian small-cap research screen

A repeatable screen of about 1,100 NSE/BSE small caps. It scores each company on six investor lenses, researches the top 60 on the web, writes memos for the finalists and runs an LLM council over them.

**This is research, not investment advice.** Nothing here is a buy or sell call.

## What's here

| Path | What it is |
|---|---|
| `outputs/research.xlsx` | Workbook: Universe, Excluded (with reasons), Scores, Top60, Finalists, Council, Comparables, ValuationGap, SpotCheck, Sources, Notes |
| `memos/NN_TICKER.md` | One memo per finalist (9 sections, incl. comparables and valuation gap, plus the council verdict and sources) |
| `outputs/valuation_gap.csv`, `outputs/comparables_peers.csv`, `outputs/pe_model.json` | Comparables: valuation gap per finalist, peer tables, P/E model |
| `outputs/council.json` | Member scores, chairman score, verdict and main disagreement per finalist |
| `outputs/council/` | Raw council answers, the anonymised responses and peer-review aggregation |
| `outputs/*.csv` | Every stage's table as CSV |
| `config.yaml` | Lens weights, filter thresholds and red-flag deductions |
| `src/smallcap/` | `load` (cache to universe), `filters` (Stage 1), `scoring` (Stage 2), `pipeline` (Stages 1-4), `comparables`, `memos`, `excel` |
| `tests/` | pytest suite for scoring, filters, loader and comparables (29 tests) |
| `cache/screener_pages/*.psv` | Raw screener pages, one file per 250-rank page |
| `cache/stage3_overrides.json`, `cache/stage4_overrides.json` | Researched facts per company, each with source URLs |

## How to re-run

```bash
cd smallcap-research
pip install pandas openpyxl pyyaml pytest
python -m pytest -q tests                       # 29 tests
PYTHONPATH=src python -m smallcap.pipeline      # Stages 1-4: universe, filter, score, top 60, finalists
PYTHONPATH=src python -m smallcap.comparables   # peer tables, valuation gap, P/E model
PYTHONPATH=src python -m smallcap.memos         # memos/ (reads outputs/council.json if present)
PYTHONPATH=src python -m smallcap.excel         # outputs/research.xlsx
```

Change weights or thresholds in `config.yaml` and re-run the pipeline. Weights are normalised to 100%.

To refresh the data:

1. Replace `cache/screener_pages/*.psv` with new pages. Each line is `symbol|name|industry|sector|mcap_cr|price|pe|roe|roce|opm|sales_cr|sales_g3y|pat_cr|pat_g3y|de|insider_pct|inst_pct|ebit_cr|bse_code`.
2. If you get a Screener.in export, map its columns to these names in `src/smallcap/load.py` (`BASE_COLUMNS`). It would fill the missing fields listed below.
3. Optionally add `cache/supplement.psv` (`symbol|cfo_cr|pbt_cr|capex_cr|ebitda_cr|ret_1y|pat_g_yoy|sales_g_yoy|shares_yoy|roic`). The filter and scoring code use these columns when they are present.
4. Stage 3 and 4 research is in the two overrides JSON files, keyed by symbol (`N:TICKER` or `B:BSECODE`). Edit them by hand or with `python -m smallcap.ov < new.json`.

## This run (17 Nov 2026)

There is no earlier run, so this is the baseline.

| Stage | Result |
|---|---|
| Universe | 1,090 unique companies (ranks 1,750-3,750 by market cap, about Rs 4,550 Cr down to Rs 570 Cr; the NSE listing is kept where a company is listed on both exchanges) |
| Stage 1 exclusions | 257 companies. Reasons (a company can have several): financial or holding company 106, net profit above 1.3x operating profit 70, operating and net loss 69, sales under Rs 50 Cr 40, price under Rs 10 21, one-off profit spike 15, data anomaly 13, no sales data 9 |
| Stage 2 | 833 scored |
| Stage 3 | Top 60 researched; 2 dropped (One Global Service Provider: unexplained change of control and conflicting financials; Axis Solutions: promoter holding above the 75% public-float limit, recently relisted) |
| Stage 4 | 15 finalists, one memo each |
| Stage 5 | Four-lens council with anonymised peer review |

### Finalists by council score

| # | Company | Council | Screen | P/E (as scored) | Peer median P/E (gap) | Fundamentals-implied P/E (gap) |
|---|---|---|---|---|---|---|
| 1 | SRM Contractors | 5.94 | 7.86 | 7.7x | 10.3x (-25%) | 18.5x (-58%) |
| 2 | Frontier Springs | 5.92 | 8.17 | 26.4x | 23.5x (+12%) | 16.0x (+65%) |
| 3 | Gandhi Special Tubes | 5.85 | 7.72 | 14.1x | 28.7x (-51%) | 16.2x (-13%) |
| 4 | Dynamic Cables | 5.46 | 7.78 | 18.7x | 27.5x (-32%) | 20.0x (-6%) |
| 5 | Gulshan Polyols | 5.46 | 8.16 | 6.0x | 17.1x (-65%) | 13.2x (-55%) |
| 6 | Crizac | 5.01 | 7.86 | 12.7x | n/a (only peer, IDP, has no meaningful P/E) | 24.2x (-48%) |
| 7 | Jeena Sikho Lifecare | 4.75 | 7.89 | 17.4x | 31.2x (-44%) | 26.9x (-35%) |
| 8 | KP Green Engineering | 4.59 | 7.76 | 10.0x | 21.1x (-53%) | 26.4x (-62%) |
| 9 | Apcotex Industries | 4.56 | 7.31 | 14.7x | 13.3x (+11%) | 17.1x (-14%) |
| 10 | Arrow Greentech | 4.47 | 7.26 | 14.2x | 8.5x (+67%) | 16.3x (-13%) |
| 11 | Savita Oil Technologies | 4.44 | 6.42 | 24.5x (normalised) | 10.1x (+143%) | 18.4x (+33%) |
| 12 | TAC Infosec | 3.83 | 7.59 | 33.6x | 21.3x (+58%) | 15.6x (+116%) |
| 13 | Unified Data-Tech | 3.76 | 7.82 | 17.1x | 19.1x (-11%) | 21.5x (-20%) |
| 14 | Krishna Defence | 3.70 | 7.84 | 35.6x | 34.2x (+4%) | 19.3x (+84%) |
| 15 | Modison | 3.49 | 7.19 | 15.6x (normalised) | 24.0x (-35%) | 18.4x (-15%) |

The council scores sit well below the screen scores. The screen rewards recent acceleration, and the council penalised missing cash-flow data, windfall quarters and policy dependence. Read the two together. The council ran before the comparables were added, so its scores don't use them.

## Comparables and valuation gaps

Each finalist has a named peer set (`src/smallcap/comparables_content.py`):

- **Universe peers:** companies in the same business from the cached screener universe, on the same data date.
- **Sector leaders:** larger listed competitors outside the cached band (Polycab, KEI, Ratnamani, Balrampur, Narayana, KEC, Castrol, GRSE, Tenable, IDP and others). Their figures are web-search snapshots with a date, so treat them as approximate.

For each finalist the research records how the competitors are doing, why this company is positioned differently, and why its valuation doesn't match its peers. Memo section 9 and the Comparables / ValuationGap sheets hold the detail.

**Two yardsticks:**

1. **Peer median P/E.** Only multiples between 3x and 100x count; above 100x the earnings are too thin to mean anything.
2. **Fundamentals-implied P/E.** A screen-wide regression of log(P/E) on ROCE, 3Y sales and profit growth, size, leverage and sector (`outputs/pe_model.json`). It explains only ~17% of the variation, so it is a weak cross-check. Its coefficients still matter: the market pays more for size and *less* for high current ROCE and fast recent profit growth. In other words, it expects recent spikes to revert.

**What the gaps say:**

- **Discounts that look explained by risk:**
  - Gulshan (-65% vs peers): policy-set ethanol spread.
  - KP Green (-53%): SME listing and related-party revenue.
  - Gandhi Tubes (-51%): slow growth in a pipe cycle that rewards growth.
  - Jeena Sikho (-44%): credibility of a 44% margin and weak cash conversion.
  - SRM (-25%): road-EPC sector de-rating and FY25 cash burn.
- **Premiums that are the risk:**
  - Savita (+143% on normalised profit).
  - Arrow (+67% vs commodity film makers).
  - TAC (+58% vs peers, more than double the model).
- **Priced roughly in line:** Krishna Defence (with the defence theme), Apcotex, Unified Data-Tech and Frontier Springs.

**Scoring change:** the Lynch "P/E vs industry" criterion now uses the curated peer median P/E when one exists, instead of the broad industry median.

## Data sources and what was missing

- **Screener.in CSV:** not supplied. Instead, the universe comes from the stockanalysis.com India screener via the Firecrawl Alexandria connector (fetched 17 Nov 2026), paged by market-cap rank.
- **yfinance, NSE archives (EQUITY_L.csv) and Screener.in pages:** blocked by this session's network policy, so they were not used. To use them, add `query1.finance.yahoo.com`, `nsearchives.nseindia.com` and `www.screener.in` to the environment's allowed domains.
- **Supplementary fields (CFO, PBT, capex, 1-year return):** the full-universe fetch failed when the Firecrawl credits ran out. Stage 1's other-income test therefore uses a proxy: net profit above 1.3x operating profit, not other income as a share of PBT.
- **Fields the source does not provide:** change in promoter holding over 3Y, pledged %, FII and DII separately, number of shareholders, debtor days. For the top 60, Stage 3 web research filled promoter, pledge, FII+DII and some CFO and debtor-day figures.
- **Stage 3 and 4 research:** web search over exchange-filing aggregators and company releases, each fact with its URLs in the overrides files and the Sources sheet.

## Caveats

- **Promoter holding:** the feed's "insider %" is a poor proxy for it. Research found it wrong for many top-60 names (R M Drip 62.7% in the feed vs 21.1% actual; Indo Tech 0% vs 72%), and it is wrong for corporate promoters (Nelco 3.5% vs 50.1%, which is Tata Power's stake).
- **Spot-check:** 10 random rows against public pages (SpotCheck sheet). Price and market cap matched within the drift you'd expect between dates for 9 of 10; one was inconclusive because its source was two months old. There were mismatches in promoter % (4 rows), ROCE (2), revenue (2-3, including Popular Vehicles at about 2.6x the reported figure) and P/E basis (2). Treat the feed's ROCE and revenue as approximate outside the top 60.
- **CFO/PAT:** this ratio often divides the latest financial year's CFO by trailing-twelve-month profit, so it is indicative only. CFO is still unknown for 9 of the 15 finalists.
- **Windfall earnings:** Savita Oil and Modison were normalised to FY26 profit. The council noted that Modison's FY26 profit was itself silver-inflated.
- **Identical profit figures:** Gulshan Polyols and Apcotex both show a TTM PAT of Rs 170.7 Cr. Each figure matches its own provider P/E (1,022/6.0 and 2,509/14.7), so this is a coincidence, not a transcription error.
- **10-year histories:** not verified for any finalist. Each memo links the Screener page where they can be pulled.
- **"Try the product" and headroom scores:** desk-based and provisional. Nobody has visited or used the products.

## Not done yet

- **Dashboard** (`dashboard/index.html`): deferred at your request. The CSVs, `council.json` and memos already hold everything it would embed.
- **Data gaps for the finalists:** close same-period CFO, receivables, related-party schedules and 10-year history from the annual reports.

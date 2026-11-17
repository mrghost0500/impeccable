import math
import os
import sys

import pandas as pd
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from smallcap import filters, scoring  # noqa: E402
from smallcap.load import dedupe, parse_symbol  # noqa: E402

with open(os.path.join(ROOT, "config.yaml")) as fh:
    CFG = yaml.safe_load(fh)

CTX = scoring.Context(industry_pe={"Auto Parts": 25.0}, industry_opm={"Auto Parts": 10.0},
                      overall_pe=25.0, overall_opm=12.0)


def base_row(**kw):
    r = dict(
        symbol="N:TEST", name="Test Industries", industry="Auto Parts", sector="Consumer Discretionary",
        mcap_cr=1500, price=200, pe=15, roe=22, roce=25, opm=15, sales_cr=500, sales_g3y=22,
        pat_cr=60, pat_g3y=30, de=0.1, promoter_pct=65, inst_pct=4, ebit_cr=80,
        cfo_cr=70, pbt_cr=82, capex_cr=-30, sales_g_yoy=18, pat_g_yoy=25, shares_yoy=0.0,
    )
    r.update(kw)
    return r


# ---------------------------------------------------------------- helpers

def test_lin_maps_endpoints_and_clips():
    assert scoring.lin(10, 10, 30) == 0
    assert scoring.lin(30, 10, 30) == 10
    assert scoring.lin(20, 10, 30) == pytest.approx(5)
    assert scoring.lin(99, 10, 30) == 10
    assert scoring.lin(-5, 10, 30) == 0


def test_lin_reverse_direction_for_lower_is_better():
    assert scoring.lin(0.5, 1.5, 0.5) == 10
    assert scoring.lin(1.5, 1.5, 0.5) == 0
    assert scoring.lin(1.0, 1.5, 0.5) == pytest.approx(5)


def test_peg_definition_and_invalid_inputs():
    assert scoring.peg(15, 30) == pytest.approx(0.5)
    assert scoring.peg(-10, 30) is None
    assert scoring.peg(15, -5) is None
    assert scoring.peg(float("nan"), 20) is None


def test_cfo_to_pat_requires_positive_profit():
    assert scoring.cfo_to_pat(80, 100) == pytest.approx(0.8)
    assert scoring.cfo_to_pat(80, -10) is None


def test_weights_normalise_to_one():
    w = scoring.normalise_weights({"a": 30, "b": 20, "c": 50})
    assert sum(w.values()) == pytest.approx(1.0)
    assert w["a"] == pytest.approx(0.3)
    with pytest.raises(ValueError):
        scoring.normalise_weights({"a": 0})


# ---------------------------------------------------------------- lenses

def test_lynch_rewards_low_peg():
    cheap, _ = scoring.lynch_score(base_row(pe=10, pat_g3y=30), CFG, CTX)   # PEG 0.33
    dear, _ = scoring.lynch_score(base_row(pe=60, pat_g3y=30), CFG, CTX)    # PEG 2.0
    assert cheap > dear
    assert cheap > 8


def test_lynch_penalises_crowded_institutional_holding():
    low, _ = scoring.lynch_score(base_row(inst_pct=2), CFG, CTX)
    high, _ = scoring.lynch_score(base_row(inst_pct=40), CFG, CTX)
    assert low - high == pytest.approx(10 * CFG["lynch"]["sub_weights"]["institutional"], rel=1e-6)


def test_lynch_loss_maker_gets_zero_peg_credit():
    s, d = scoring.lynch_score(base_row(pe=None), CFG, CTX)
    assert d["peg"] is None
    s_ok, _ = scoring.lynch_score(base_row(), CFG, CTX)
    assert s < s_ok


def test_mayer_prefers_small_high_roe_growers():
    small, _ = scoring.mayer_score(base_row(mcap_cr=900, roe=28, sales_g3y=30, promoter_pct=70), CFG, CTX)
    big, _ = scoring.mayer_score(base_row(mcap_cr=4800, roe=11, sales_g3y=6, promoter_pct=32), CFG, CTX)
    assert small > 9
    assert big < 3


def test_reinvestment_score_shape():
    assert scoring.reinvestment_score(-50, 100) == 10       # reinvests half of CFO
    assert scoring.reinvestment_score(-5, 100) < 6          # barely reinvesting
    assert scoring.reinvestment_score(-300, 100) < 10       # capex far above CFO
    assert scoring.reinvestment_score(-50, -10) == 2        # negative CFO
    assert scoring.reinvestment_score(None, 100) == scoring.NEUTRAL


def test_kirby_full_marks_for_consistent_compounder():
    s, d = scoring.kirby_score(base_row(sales_g3y=15, sales_g_yoy=15, roce=20, cfo_cr=90, pat_cr=100,
                                        debtor_days=60), CFG, CTX)
    assert s == pytest.approx(10)
    assert d["cfo_to_pat"] == pytest.approx(0.9)


def test_buffett_pricing_power_uses_industry_margin():
    strong, _ = scoring.buffett_fisher_score(base_row(opm=15), CFG, CTX)   # 1.5x industry OPM
    weak, _ = scoring.buffett_fisher_score(base_row(opm=5), CFG, CTX)      # 0.5x industry OPM
    assert strong > weak


def test_product_lens_neutral_until_researched():
    s, _ = scoring.product_score(base_row(), CFG, CTX)
    assert s == 5
    s2, _ = scoring.product_score(base_row(product_score=8), CFG, CTX)
    assert s2 == 8


# ---------------------------------------------------------------- red flags & composite

def test_red_flags_deduct_and_are_listed():
    clean = scoring.score_row(base_row(), CFG, CTX)
    flagged = scoring.score_row(base_row(pledge_pct=12, cfo_cr=10, auditor_change=True), CFG, CTX)
    assert clean["n_red_flags"] == 0
    assert flagged["n_red_flags"] == 3
    pledge = round(0.2 + 0.8 * min(12 / 50, 1.0), 2)
    expected = pledge + CFG["red_flags"]["cfo_to_pat_below_0_5"] + CFG["red_flags"]["auditor_change"]
    assert flagged["red_flag_deduction"] == pytest.approx(expected)
    assert flagged["score"] == pytest.approx(max(0, flagged["base_score"] - expected), abs=1e-3)


def test_writeoff_flag_when_net_loss_but_operating_profit():
    flags = scoring.red_flags(base_row(pat_cr=-5, ebit_cr=40), CFG)
    assert any("write-off" in f for f, _ in flags)


def test_composite_is_bounded():
    r = scoring.score_row(base_row(pledge_pct=50, promoter_chg_3y=-20, auditor_change=True,
                                   regulatory_incident=True, debtor_days=300, rpt_pct=40,
                                   cfo_cr=1, shares_yoy=50), CFG, CTX)
    assert 0 <= r["score"] <= 10


def test_score_frame_ranks_descending():
    df = pd.DataFrame([base_row(symbol="N:A", name="A", pe=10), base_row(symbol="N:B", name="B", pe=80)])
    out = scoring.score_frame(df, CFG, CTX)
    assert list(out["symbol"]) == ["N:A", "N:B"]
    assert list(out["rank"]) == [1, 2]


# ---------------------------------------------------------------- filters & loader

def test_filter_small_sales_and_penny_price():
    reasons = filters.exclusion_reasons(base_row(sales_cr=30, price=6), CFG)
    assert any("sales" in r for r in reasons)
    assert any("price" in r for r in reasons)


def test_filter_other_income_lower_bound():
    assert filters.other_income_share(100, 60) == pytest.approx(0.4)
    assert filters.other_income_share(100, 120) == 0
    assert filters.other_income_share(-5, 10) is None
    reasons = filters.exclusion_reasons(base_row(pbt_cr=100, ebit_cr=50), CFG)
    assert any("other income" in r for r in reasons)


def test_filter_keeps_net_loss_with_operating_profit():
    # write-off year: net loss but positive operating profit must not be dropped
    reasons = filters.exclusion_reasons(base_row(pat_cr=-10, ebit_cr=50, pbt_cr=40), CFG)
    assert reasons == []
    reasons = filters.exclusion_reasons(base_row(pat_cr=-10, ebit_cr=-5, pbt_cr=-12), CFG)
    assert any("operating loss" in r for r in reasons)


def test_filter_one_off_profit_spike():
    r = filters.exclusion_reasons(base_row(pat_g_yoy=450, sales_g_yoy=5), CFG)
    assert any("one-off" in x for x in r)
    r = filters.exclusion_reasons(base_row(pat_g_yoy=450, sales_g_yoy=60), CFG)
    assert not any("one-off" in x for x in r)


def test_filter_financials_and_holdcos():
    assert any("financial" in r for r in filters.exclusion_reasons(base_row(industry="Credit Services"), CFG))
    assert any("holding" in r for r in filters.exclusion_reasons(base_row(name="Acme Investments"), CFG))


def test_dedupe_prefers_nse_and_carries_bse_code():
    df = pd.DataFrame([
        dict(symbol="B:500001", name="Foo Limited", mcap_cr=1000, bse_code=""),
        dict(symbol="N:FOO", name="Foo", mcap_cr=990, bse_code=""),
    ])
    out = dedupe(df)
    assert len(out) == 1
    assert out.iloc[0]["symbol"] == "N:FOO"
    assert out.iloc[0]["bse_code"] == "500001"


def test_parse_symbol_builds_tickers():
    assert parse_symbol("N:KPL")["yahoo"] == "KPL.NS"
    assert parse_symbol("B:543669")["yahoo"] == "543669.BO"


def test_sme_listing_lifts_exit_path():
    plain, _ = scoring.pe_vc_score(base_row(mcap_cr=600), CFG, CTX)
    sme, _ = scoring.pe_vc_score(base_row(mcap_cr=600, sme=True), CFG, CTX)
    assert sme > plain


def test_apply_overrides_replaces_feed_values():
    from smallcap.pipeline import apply_overrides
    df = pd.DataFrame([base_row(symbol="N:A", promoter_pct=70)])
    out = apply_overrides(df, {"N:A": {"promoter_pct": 21.1, "notes": "x", "sources": ["u"]}})
    assert out.iloc[0]["promoter_pct"] == 21.1
    assert "notes" not in out.columns


def test_pledge_deduction_scales_with_size():
    small = dict(scoring.red_flags(base_row(pledge_pct=2), CFG))
    large = dict(scoring.red_flags(base_row(pledge_pct=77), CFG))
    assert list(small.values())[0] < list(large.values())[0] == 1.0


def test_peer_pe_overrides_industry_median():
    # same company, cheap vs its curated peers but expensive vs the broad industry median
    vs_peers, d1 = scoring.lynch_score(base_row(pe=20, peer_pe=40), CFG, CTX)
    vs_industry, d2 = scoring.lynch_score(base_row(pe=20), CFG, CTX)   # CTX Auto Parts median = 25
    assert d1["industry_pe"] == 40 and d2["industry_pe"] == 25
    assert vs_peers > vs_industry


def test_model_pe_and_peer_median():
    from smallcap import comparables
    df = pd.DataFrame([dict(pe=10 + i, roce=10 + i, sales_g3y=5 + i, pat_g3y=5 + i, de=0.2,
                            mcap_cr=1000 + 50 * i, sector="Industrials" if i % 2 else "Materials")
                       for i in range(30)])
    m = comparables.fit_pe_model(df)
    assert m["n"] == 30 and 0 <= m["r2"] <= 1
    p = comparables.model_pe(m, dict(roce=20, sales_g3y=15, pat_g3y=15, de=0.2, mcap_cr=1500, sector="Materials"))
    assert 5 < p < 60
    assert comparables._median([10, None, 30, float("nan")]) == 20
    assert not comparables._valid_pe(150) and comparables._valid_pe(12)


def test_scenario_probs_shift_and_sum():
    from smallcap.projections import scenario_probs
    pc = CFG["projections"]
    p0, r0 = scenario_probs({}, pc)
    assert p0 == (0.25, 0.5, 0.25) and r0 == []
    p1, r1 = scenario_probs({"cfo_gap": True, "policy": True, "order_cover": True}, pc)
    assert p1 == (0.30, 0.5, 0.20) and set(r1) == {"-cfo_gap", "-policy", "+order_cover"}
    p2, _ = scenario_probs({f: True for f in pc["negative_flags"]}, pc)
    assert p2[0] == pc["bear_range"][1] and abs(sum(p2) - 1) < 1e-9


def test_outcomes_moic_and_expectation():
    from smallcap.projections import outcomes
    pc = CFG["projections"]
    oc = outcomes(1000, 100, (80, 120, 150), (0.25, 0.5, 0.25), 10, pc)   # P/E 10 today, peers 10
    base = oc["rows"][1]
    assert abs(base["exit_pe"] - 10) < 1e-9 and abs(base["moic"] - 1.2) < 1e-9
    assert abs(oc["e_pat"] - (0.25 * 80 + 0.5 * 120 + 0.25 * 150)) < 1e-9
    assert oc["p_loss"] == 0.25          # bear: 80 x 8 = 640 < 1000

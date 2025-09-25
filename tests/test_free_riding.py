from statistical_cultures.p_ic import PICConfig, sample_p_ic
from free_riding.detector import detect_free_riding
from free_riding.risk import evaluate_risk
from voting_rules.utilitarian import run_seq_utilitarian

def test_detector_and_risk():
    cfg = PICConfig(n_voters=4, candidates_per_issue=[2,2], seed=2)
    elec = sample_p_ic(cfg)
    res = detect_free_riding(elec, run_seq_utilitarian)
    risk = evaluate_risk(elec, run_seq_utilitarian)
    assert "trials" in res
    assert "success_rate" in risk

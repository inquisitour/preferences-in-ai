# File: tests/test_free_riding.py
from statistical_cultures.p_ic import PICConfig, sample_p_ic
from free_riding.detector import detect_free_riding
from free_riding.risk import evaluate_risk
from voting_rules.utilitarian import sequential_utilitarian

def test_detector_and_risk():
    cfg = PICConfig(n_voters=4, candidates_per_issue=[2, 2], seed=2)
    elec = sample_p_ic(cfg)

    res = detect_free_riding(elec, sequential_utilitarian)
    risk = evaluate_risk(elec, sequential_utilitarian)

    assert "trials" in res
    assert "successes" in res
    assert "harms" in res
    assert "success_rate" in risk
    assert "harm_rate" in risk
    assert risk["trials"] == res["trials"]
    assert risk["successes"] == res["successes"]

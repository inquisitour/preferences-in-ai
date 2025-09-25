from statistical_cultures.p_ic import PICConfig, sample_p_ic
from voting_rules.utilitarian import run_seq_utilitarian
from voting_rules.sequential_thiele import run_seq_pav

def test_rules_run():
    cfg = PICConfig(n_voters=5, candidates_per_issue=[2,2], seed=1)
    elec = sample_p_ic(cfg)
    assert run_seq_utilitarian(elec).winners
    assert run_seq_pav(elec).winners

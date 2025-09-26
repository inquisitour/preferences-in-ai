# File: tests/test_rules.py
from statistical_cultures.p_ic import PICConfig, sample_p_ic
from voting_rules.utilitarian import sequential_utilitarian
from voting_rules.sequential_thiele import sequential_thiele
from voting_rules.owa import leximin_owa, mean_owa
from core.types import Outcome

def test_utilitarian_and_thiele_rules():
    cfg = PICConfig(n_voters=5, candidates_per_issue=[2, 2], seed=1)
    elec = sample_p_ic(cfg)

    out1 = sequential_utilitarian(elec)
    out2 = sequential_thiele(elec, rule="pav")

    assert isinstance(out1, Outcome)
    assert isinstance(out2, Outcome)
    assert out1.winners
    assert out2.winners

def test_owa_rules():
    cfg = PICConfig(n_voters=5, candidates_per_issue=[2, 2], seed=2)
    elec = sample_p_ic(cfg)

    out1 = leximin_owa(elec)
    out2 = mean_owa(elec)

    assert isinstance(out1, Outcome)
    assert isinstance(out2, Outcome)
    assert out1.winners
    assert out2.winners
    assert out1.winners != out2.winners
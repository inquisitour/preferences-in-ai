# File: tests/test_rules.py
from statistical_cultures.p_ic import PICConfig, sample_p_ic
from voting_rules.utilitarian import sequential_utilitarian
from voting_rules.sequential_thiele import sequential_thiele
from voting_rules.owa import owa_rule, leximin_owa
from core.types import Outcome


def test_utilitarian_rule():
    cfg = PICConfig(n_voters=5, candidates_per_issue=[2, 2], seed=1)
    elec = sample_p_ic(cfg)

    out = sequential_utilitarian(elec)
    assert isinstance(out, Outcome)
    assert out.winners


def test_thiele_rules_parametric():
    cfg = PICConfig(n_voters=5, candidates_per_issue=[2, 2], seed=2)
    elec = sample_p_ic(cfg)

    out1 = sequential_thiele(elec, x=1)
    out2 = sequential_thiele(elec, x=5)

    assert isinstance(out1, Outcome)
    assert isinstance(out2, Outcome)
    assert out1.winners
    assert out2.winners


def test_owa_rules_parametric_and_leximin():
    cfg = PICConfig(n_voters=5, candidates_per_issue=[2, 2], seed=3)
    elec = sample_p_ic(cfg)

    out1 = owa_rule(elec, x=3)
    out2 = leximin_owa(elec)

    assert isinstance(out1, Outcome)
    assert isinstance(out2, Outcome)
    assert out1.winners
    assert out2.winners

from statistical_cultures.p_ic import PICConfig, sample_p_ic
from statistical_cultures.disjoint import DisjointConfig, sample_disjoint
from statistical_cultures.resampling import ResamplingConfig, sample_resampling

def test_pic():
    cfg = PICConfig(n_voters=5, candidates_per_issue=[3,3], seed=0)
    elec = sample_p_ic(cfg)
    assert elec.approvals.shape == (5,2,3)

def test_disjoint():
    cfg = DisjointConfig(n_voters=6, candidates_per_issue=[2,2], n_groups=2, seed=0)
    elec = sample_disjoint(cfg)
    assert elec.approvals.shape == (6,2,2)

def test_resampling():
    cfg = ResamplingConfig(n_voters=4, candidates_per_issue=[2,2], seed=0)
    elec = sample_resampling(cfg)
    assert elec.approvals.shape == (4,2,2)

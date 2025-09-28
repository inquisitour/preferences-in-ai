# File: tests/test_cultures.py
from statistical_cultures.p_ic import PICConfig, sample_p_ic
from statistical_cultures.resampling import ResamplingConfig, sample_resampling
from statistical_cultures.disjoint import DisjointConfig, sample_disjoint
from statistical_cultures.hamming_noise import HammingConfig, sample_hamming


def test_p_ic_sampling():
    cfg = PICConfig(n_voters=4, candidates_per_issue=[2, 2], p=0.5, seed=1)
    elec = sample_p_ic(cfg)
    assert elec.approvals.shape == (4, 2, 2)


def test_resampling_sampling():
    cfg = ResamplingConfig(n_voters=4, candidates_per_issue=[2, 2], p=0.5, phi=0.3, seed=2)
    elec = sample_resampling(cfg)
    assert elec.approvals.shape == (4, 2, 2)


def test_disjoint_sampling():
    cfg = DisjointConfig(n_voters=4, candidates_per_issue=[2, 2], n_groups=2, p=0.5, seed=3)
    elec = sample_disjoint(cfg)
    assert elec.approvals.shape == (4, 2, 2)


def test_hamming_sampling():
    cfg = HammingConfig(base="p_ic", n_voters=4, candidates_per_issue=[2, 2], p=0.5, noise_prob=0.2, seed=4)
    elec = sample_hamming(cfg)
    assert elec.approvals.shape == (4, 2, 2)

# File: statistical_cultures/hamming_noise.py
from dataclasses import dataclass
from typing import List
import numpy as np
from core.types import MultiIssueElection
from statistical_cultures.p_ic import PICConfig, sample_p_ic
from statistical_cultures.resampling import ResamplingConfig, sample_resampling
from statistical_cultures.disjoint import DisjointConfig, sample_disjoint


@dataclass
class HammingConfig:
    """Configuration for Hamming-noise preferences."""
    base: str                   # base culture: "p_ic", "resampling", or "disjoint"
    n_voters: int
    candidates_per_issue: List[int]
    p: float = 0.5              # approval probability
    phi: float = 0.5            # correlation (resampling model)
    groups: int = 2             # number of groups (disjoint model)
    noise_prob: float = 0.1     # probability of flipping each approval
    seed: int = None            # random seed


def add_hamming_noise(elec: MultiIssueElection, noise_prob: float, seed=None) -> MultiIssueElection:
    """Flip each approval with probability `noise_prob`."""
    rng = np.random.default_rng(seed)
    noisy = elec.approvals.copy()
    flips = rng.binomial(1, noise_prob, size=noisy.shape)
    noisy = np.abs(noisy - flips)
    return MultiIssueElection(noisy)


def sample_hamming(cfg: HammingConfig) -> MultiIssueElection:
    """Sample from a base culture and apply Hamming noise."""
    if cfg.base == "p_ic":
        base_cfg = PICConfig(
            n_voters=cfg.n_voters,
            candidates_per_issue=cfg.candidates_per_issue,
            p=cfg.p,
            seed=cfg.seed
        )
        elec = sample_p_ic(base_cfg)

    elif cfg.base == "resampling":
        base_cfg = ResamplingConfig(
            n_voters=cfg.n_voters,
            candidates_per_issue=cfg.candidates_per_issue,
            p=cfg.p,
            phi=cfg.phi,
            seed=cfg.seed
        )
        elec = sample_resampling(base_cfg)

    elif cfg.base == "disjoint":
        base_cfg = DisjointConfig(
            n_voters=cfg.n_voters,
            candidates_per_issue=cfg.candidates_per_issue,
            n_groups=cfg.groups,
            p=cfg.p,
            seed=cfg.seed
        )
        elec = sample_disjoint(base_cfg)

    else:
        raise ValueError(f"Unknown base culture: {cfg.base}")

    return add_hamming_noise(elec, cfg.noise_prob, seed=cfg.seed)

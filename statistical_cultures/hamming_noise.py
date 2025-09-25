import numpy as np
from core.types import MultiIssueElection

def add_hamming_noise(elec: MultiIssueElection, noise_prob: float, seed=None) -> MultiIssueElection:
    rng = np.random.default_rng(seed)
    noisy = elec.approvals.copy()
    flips = rng.binomial(1, noise_prob, size=noisy.shape)
    noisy = np.abs(noisy - flips)
    return MultiIssueElection(noisy)

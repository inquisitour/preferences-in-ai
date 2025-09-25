import numpy as np
from dataclasses import dataclass
from core.types import MultiIssueElection

@dataclass
class ResamplingConfig:
    n_voters: int
    candidates_per_issue: list
    p: float = 0.5
    phi: float = 0.5
    seed: int = None

def sample_resampling(cfg: ResamplingConfig) -> MultiIssueElection:
    rng = np.random.default_rng(cfg.seed)
    approvals = []
    base_pref = []
    for m in cfg.candidates_per_issue:
        base_pref.append(rng.binomial(1, cfg.p, size=m))
    for _ in range(cfg.n_voters):
        voter = []
        for base in base_pref:
            mask = rng.binomial(1, cfg.phi, size=base.shape)
            issue_pref = np.where(mask == 1, base, rng.binomial(1, cfg.p, size=base.shape))
            voter.append(issue_pref)
        approvals.append(voter)
    approvals = np.array(approvals)
    return MultiIssueElection(approvals)

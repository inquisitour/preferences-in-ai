import numpy as np
from dataclasses import dataclass
from core.types import MultiIssueElection

@dataclass
class DisjointConfig:
    n_voters: int
    candidates_per_issue: list
    n_groups: int
    p: float = 0.5
    seed: int = None

def sample_disjoint(cfg: DisjointConfig) -> MultiIssueElection:
    rng = np.random.default_rng(cfg.seed)
    group_size = cfg.n_voters // cfg.n_groups
    approvals = []
    for m in cfg.candidates_per_issue:
        issue_matrix = np.zeros((cfg.n_voters, m))
        for g in range(cfg.n_groups):
            start, end = g * group_size, (g + 1) * group_size
            fav = rng.integers(0, m)
            issue_matrix[start:end, fav] = rng.binomial(1, cfg.p, size=(group_size,))
        approvals.append(issue_matrix)
    approvals = np.stack(approvals, axis=1)
    return MultiIssueElection(approvals)

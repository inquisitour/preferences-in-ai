import numpy as np
from dataclasses import dataclass
from core.types import MultiIssueElection

@dataclass
class PICConfig:
    n_voters: int
    candidates_per_issue: list
    p: float = 0.5
    seed: int = None

def sample_p_ic(cfg: PICConfig) -> MultiIssueElection:
    rng = np.random.default_rng(cfg.seed)
    approvals = []
    for m in cfg.candidates_per_issue:
        issue_matrix = rng.binomial(1, cfg.p, size=(cfg.n_voters, m))
        approvals.append(issue_matrix)
    approvals = np.stack(approvals, axis=1)
    return MultiIssueElection(approvals)

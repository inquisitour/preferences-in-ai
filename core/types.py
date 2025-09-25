from dataclasses import dataclass
from typing import List, Dict, Callable
import numpy as np

@dataclass
class MultiIssueElection:
    approvals: np.ndarray  # shape (n_voters, n_issues, n_candidates)

    @property
    def n_voters(self):
        return self.approvals.shape[0]

    @property
    def n_issues(self):
        return self.approvals.shape[1]

    @property
    def candidates_per_issue(self):
        return self.approvals.shape[2]

@dataclass
class Outcome:
    winners: List[int]

def utilitarian_welfare(elec: MultiIssueElection, outcome: Outcome) -> float:
    welfare = 0.0
    for issue, cand in enumerate(outcome.winners):
        welfare += elec.approvals[:, issue, cand].sum()
    return welfare

def egalitarian_welfare(elec: MultiIssueElection, outcome: Outcome) -> float:
    scores = np.zeros(elec.n_voters)
    for issue, cand in enumerate(outcome.winners):
        scores += elec.approvals[:, issue, cand]
    return scores.min()

def nash_welfare(elec: MultiIssueElection, outcome: Outcome) -> float:
    scores = np.ones(elec.n_voters)
    for issue, cand in enumerate(outcome.winners):
        scores *= (1 + elec.approvals[:, issue, cand])
    return np.prod(scores) ** (1 / elec.n_voters)

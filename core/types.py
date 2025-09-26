# File: core/types.py
from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class MultiIssueElection:
    """
    Represents a multi-issue approval election.

    Attributes
    ----------
    approvals : np.ndarray
        Binary approval tensor of shape (n_voters, n_issues, n_candidates).
        approvals[v, i, c] = 1 if voter v approves candidate c on issue i.
    """
    approvals: np.ndarray

    @property
    def n_voters(self) -> int:
        return self.approvals.shape[0]

    @property
    def n_issues(self) -> int:
        return self.approvals.shape[1]

    @property
    def candidates_per_issue(self) -> int:
        return self.approvals.shape[2]


@dataclass
class Outcome:
    """
    Stores the outcome of a multi-issue election.

    Attributes
    ----------
    winners : List[int]
        A list of chosen candidate indices, one per issue.
        winners[i] = index of the selected candidate for issue i.
    """
    winners: List[int]


def make_outcome(winners: List[int]) -> Outcome:
    """
    Helper constructor for creating an Outcome from a list of winners.
    """
    return Outcome(winners=winners)


# -------------------------
# Welfare Functions
# -------------------------

def utilitarian_welfare(elec: MultiIssueElection, outcome: Outcome) -> float:
    """
    Sum of approvals (total utility) across all voters and issues.
    """
    welfare = 0.0
    for issue, cand in enumerate(outcome.winners):
        welfare += elec.approvals[:, issue, cand].sum()
    return welfare


def egalitarian_welfare(elec: MultiIssueElection, outcome: Outcome) -> float:
    """
    Minimum utility across voters (focus on worst-off voter).
    """
    scores = np.zeros(elec.n_voters)
    for issue, cand in enumerate(outcome.winners):
        scores += elec.approvals[:, issue, cand]
    return scores.min()


def nash_welfare(elec: MultiIssueElection, outcome: Outcome) -> float:
    """
    Nash social welfare: geometric mean of utilities.
    To avoid zero-product, we add +1 to each voter’s score.
    """
    scores = np.ones(elec.n_voters)
    for issue, cand in enumerate(outcome.winners):
        scores *= (1 + elec.approvals[:, issue, cand])
    return np.prod(scores) ** (1 / elec.n_voters)

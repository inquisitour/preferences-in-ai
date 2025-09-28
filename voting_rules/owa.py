# File: voting_rules/owa.py
import numpy as np
from core.types import MultiIssueElection, Outcome


def owa_aggregate(values, weights):
    """
    Generic OWA aggregation: sort values descending, apply weights.
    """
    values_sorted = sorted(values, reverse=True)
    return sum(w * v for w, v in zip(weights, values_sorted))


def owa_weights(n_voters: int, x: int) -> list:
    """
    Construct OWA weights as in Lackner & al. (2023).
    - x = 0   -> utilitarian (all weights = 1)
    - x = n-1 -> leximin (only worst-off counts)
    - intermediate x interpolates between them
    """
    if x < 0 or x >= n_voters:
        raise ValueError(f"Invalid OWA parameter x={x}, must be in [0, n_voters-1].")

    # Start with all zeros
    weights = [0] * n_voters
    # Assign weight 1 to the last (x+1) positions
    for i in range(n_voters - (x + 1), n_voters):
        weights[i] = 1
    return weights


def owa_rule(elec: MultiIssueElection, x: int) -> Outcome:
    """
    Apply parametric OWA rule for multi-issue decisions.
    :param elec: MultiIssueElection
    :param x: parameter (0=utilitarian, n-1=leximin)
    :return: Outcome
    """
    n_voters, n_issues, n_cands = elec.approvals.shape
    weight_vec = owa_weights(n_voters, x)

    winners = []
    for issue in range(n_issues):
        issue_scores = []
        for cand in range(n_cands):
            approvals = [elec.approvals[voter, issue, cand] for voter in range(n_voters)]
            score = owa_aggregate(approvals, weight_vec)
            issue_scores.append(score)
        winners.append(int(np.argmax(issue_scores)))

    return Outcome(winners=winners)


# Convenience wrappers
def leximin_owa(elec: MultiIssueElection) -> Outcome:
    """Leximin OWA is the special case x = n_voters - 1."""
    return owa_rule(elec, x=elec.n_voters - 1)

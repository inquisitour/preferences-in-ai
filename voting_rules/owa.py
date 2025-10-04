# File: voting_rules/owa.py
# Implements the Section 5 OWA family exactly:
#   α^(x) = (1, ..., 1 [n-x times], 1/(k n), 1/(k^2 n^2), ..., 1/(k^x n^x))
# and the sequential α-OWA rule as defined in the paper.
#
# References:
# - Sec. 2.2 and Sec. 5 (numerical simulations) of the paper
#   arXiv:2310.08194 (Lackner–Maly–Nardi, 2023).

from __future__ import annotations
from typing import List
import numpy as np

from core.types import MultiIssueElection, Outcome

def _alpha_vector(n_voters: int, n_issues: int, x: int) -> np.ndarray:
    """
    Construct α^(x) = (1,...,1 [n-x times], 1/(k n), 1/(k^2 n^2), ..., 1/(k^x n^x))
    as in Section 5. Length is n_voters.

    - x=0 gives utilitarian (all ones).
    - x=n_voters-1 approximates leximin (strictly positive, decreasing tail).
    """
    if x < 0 or x > n_voters - 1:
        raise ValueError(f"x must be in [0, n_voters-1]; got x={x}, n_voters={n_voters}")

    n = n_voters
    k = n_issues

    alpha = np.ones(n, dtype=float)
    tail_len = x  # number of trailing entries to replace by the geometric tail

    if tail_len > 0:
        tail = np.array([1.0 / ((k * n) ** t) for t in range(1, tail_len + 1)], dtype=float)
        alpha[-tail_len:] = tail  # replace the last x entries

    # α must be nonincreasing; with k,n >= 1 this holds automatically.
    return alpha


def _satisfaction_vector(elec: MultiIssueElection, winners: List[int]) -> np.ndarray:
    """
    Satisfaction s(w) per voter = number of issues (among decided ones)
    where the voter approves the chosen candidate.
    """
    n_voters = elec.n_voters
    decided = len(winners)
    s = np.zeros(n_voters, dtype=float)
    for i in range(decided):
        w = winners[i]
        # voters who approved winner on issue i
        s += elec.approvals[:, i, w]
    return s


def _owa_score(s: np.ndarray, alpha: np.ndarray) -> float:
    """
    OWAα(s): sort s ascending and take dot-product with α (nonincreasing).
    (Equivalently, sort descending and reverse α consistently.)
    """
    s_sorted = np.sort(s)  # ascending
    # α^(x) is nonincreasing; dot with ascending s implements OWA
    return float(np.dot(alpha, s_sorted))


def owa_rule(elec: MultiIssueElection, x: int) -> Outcome:
    """
    Sequential α^(x)-OWA rule (Section 2.2), using the family from Section 5.
    At each issue i, choose the candidate c maximizing OWAα^(x)(s(w1..wi-1,c)).

    Parameters
    ----------
    elec : MultiIssueElection
    x    : int in [0, n_voters-1]
           x=0 is utilitarian; x=n_voters-1 corresponds to the leximin limit used in the paper.

    Returns
    -------
    Outcome with one winner per issue.
    """
    n_voters = elec.n_voters
    n_issues = elec.n_issues
    n_cands = elec.candidates_per_issue

    alpha = _alpha_vector(n_voters, n_issues, x)

    winners: List[int] = []
    for i in range(n_issues):
        best_score = -1e100
        best_cand = 0
        # Try each candidate for the current issue i
        for c in range(n_cands):
            tentative = winners + [c]
            s = _satisfaction_vector(elec, tentative)
            score = _owa_score(s, alpha)
            if score > best_score:
                best_score = score
                best_cand = c
        winners.append(best_cand)

    return Outcome(winners=winners)


def leximin_owa(elec: MultiIssueElection) -> Outcome:
    """
    Convenience wrapper for the leximin limit in the Section 5 family:
    x = n_voters - 1.
    (Note: strictly positive α; not the zero-heavy vector I used before.)
    """
    return owa_rule(elec, x=elec.n_voters - 1)

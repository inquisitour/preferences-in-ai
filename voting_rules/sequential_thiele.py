import numpy as np
from core.types import MultiIssueElection, Outcome


def thiele_score_vector(x: int, max_support: int):
    """
    Return the scoring vector for a given Thiele rule with parameter x.
    - x = 0: utilitarian (all weights = 1)
    - x = 1: PAV (harmonic sequence 1, 1/2, 1/3, ...)
    - large x approximates CC (only first approval counts)
    """
    if x == 0:
        return [1.0] * max_support
    else:
        return [1 / ((i + 1) ** x) for i in range(max_support)]


def sequential_thiele(elec: MultiIssueElection, x: int = 1) -> Outcome:
    """
    Generic sequential Thiele method (parameterized by x).
    - x = 1 → seq-PAV
    - x = 0 → utilitarian
    - larger x values interpolate toward CC
    """
    winners = []
    scores = np.zeros((elec.n_voters, elec.candidates_per_issue))

    weight_vector = thiele_score_vector(x, elec.candidates_per_issue)

    for issue in range(elec.n_issues):
        issue_scores = np.zeros(elec.candidates_per_issue)
        for voter in range(elec.n_voters):
            for cand in range(elec.candidates_per_issue):
                if elec.approvals[voter, issue, cand] == 1:
                    support = int(np.sum(scores[voter, :]))
                    issue_scores[cand] += weight_vector[min(support, len(weight_vector) - 1)]
        chosen = int(np.argmax(issue_scores))
        winners.append(chosen)

        # update scores for voters who approved chosen
        for voter in range(elec.n_voters):
            if elec.approvals[voter, issue, chosen] == 1:
                scores[voter, chosen] += 1

    return Outcome(winners=winners)


# Convenience wrappers for common variants
def sequential_pav(elec: MultiIssueElection) -> Outcome:
    return sequential_thiele(elec, x=1)


def sequential_cc(elec: MultiIssueElection) -> Outcome:
    # Approximated by large x (only first approval counts strongly)
    return sequential_thiele(elec, x=1000)

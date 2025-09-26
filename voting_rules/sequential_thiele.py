import numpy as np
from core.types import MultiIssueElection, Outcome

def thiele_score_vector(rule: str, max_support: int):
    """
    Return the scoring vector for a given Thiele rule.
    - pav: harmonic sequence (1, 1/2, 1/3, ...)
    - cc: committee scoring (1, 0, 0, ...)
    """
    if rule == "pav":
        return [1 / (i + 1) for i in range(max_support)]
    elif rule == "cc":
        return [1] + [0] * (max_support - 1)
    else:
        raise ValueError(f"Unknown Thiele rule: {rule}")

def sequential_thiele(elec: MultiIssueElection, rule: str = "pav") -> Outcome:
    """
    Generic sequential Thiele method (includes seq-PAV, seq-CC).
    """
    winners = []
    scores = np.zeros((elec.n_voters, elec.candidates_per_issue))

    weight_vector = thiele_score_vector(rule, elec.candidates_per_issue)

    for issue in range(elec.n_issues):
        issue_scores = np.zeros(elec.candidates_per_issue)
        for voter in range(elec.n_voters):
            for cand in range(elec.candidates_per_issue):
                if elec.approvals[voter, issue, cand] == 1:
                    support = int(np.sum(scores[voter, :]))
                    issue_scores[cand] += weight_vector[min(support, len(weight_vector) - 1)]
        chosen = int(np.argmax(issue_scores))
        winners.append(chosen)

        for voter in range(elec.n_voters):
            if elec.approvals[voter, issue, chosen] == 1:
                scores[voter, chosen] += 1

    return Outcome(winners=winners)

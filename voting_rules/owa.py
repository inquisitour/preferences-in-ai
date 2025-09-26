import numpy as np
from core.types import MultiIssueElection, Outcome

def owa_aggregate(values, weights):
    """
    Generic OWA aggregation: sort values descending, weight them.
    """
    values_sorted = sorted(values, reverse=True)
    return sum(w * v for w, v in zip(weights, values_sorted))

def owa_rule(elec: MultiIssueElection, weights="leximin") -> Outcome:
    """
    Apply OWA-based rule for multi-issue decisions.
    Supported weights:
      - "leximin": [0, 0, ..., 1] (maximize the worst-off)
      - "mean": uniform weights
    """
    n_voters, n_issues, n_cands = elec.approvals.shape

    if weights == "leximin":
        weight_vec = [0] * (n_voters - 1) + [1]
    elif weights == "mean":
        weight_vec = [1 / n_voters] * n_voters
    else:
        raise ValueError(f"Unknown OWA weights: {weights}")

    winners = []
    for issue in range(n_issues):
        issue_scores = []
        for cand in range(n_cands):
            approvals = [elec.approvals[voter, issue, cand] for voter in range(n_voters)]
            score = owa_aggregate(approvals, weight_vec)
            issue_scores.append(score)
        winners.append(int(np.argmax(issue_scores)))

    return Outcome(winners=winners)

def leximin_owa(elec: MultiIssueElection) -> Outcome:
    return owa_rule(elec, weights="leximin")

def mean_owa(elec: MultiIssueElection) -> Outcome:
    return owa_rule(elec, weights="mean")

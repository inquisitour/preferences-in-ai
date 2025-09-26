import numpy as np
from core.types import MultiIssueElection, Outcome

def sequential_utilitarian(elec: MultiIssueElection) -> Outcome:
    """
    Sequential utilitarian rule:
    For each issue, pick the candidate with the highest number of approvals.
    """
    winners = []
    for issue in range(elec.n_issues):
        issue_scores = elec.approvals[:, issue, :].sum(axis=0)
        chosen = int(np.argmax(issue_scores))
        winners.append(chosen)
    return Outcome(winners=winners)

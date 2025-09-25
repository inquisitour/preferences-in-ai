import numpy as np
from core.types import MultiIssueElection, Outcome

def run_seq_utilitarian(elec: MultiIssueElection) -> Outcome:
    winners = []
    for issue in range(elec.n_issues):
        scores = elec.approvals[:, issue, :].sum(axis=0)
        winners.append(int(np.argmax(scores)))
    return Outcome(winners=winners)

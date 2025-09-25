import numpy as np
from core.types import MultiIssueElection, Outcome

def harmonic_weights(k):
    return [1 / i for i in range(1, k + 1)]

def run_seq_pav(elec: MultiIssueElection) -> Outcome:
    winners = []
    for issue in range(elec.n_issues):
        best_cand, best_score = None, -1
        for cand in range(elec.candidates_per_issue):
            scores = []
            for v in range(elec.n_voters):
                approved = elec.approvals[v, issue, cand]
                if approved:
                    scores.append(1)
            score = sum(scores)
            if score > best_score:
                best_cand, best_score = cand, score
        winners.append(best_cand)
    return Outcome(winners=winners)

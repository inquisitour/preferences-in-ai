from core.types import MultiIssueElection, Outcome
from voting_rules.utilitarian import run_seq_utilitarian

def detect_free_riding(elec: MultiIssueElection, rule=run_seq_utilitarian, max_flips=1):
    baseline = rule(elec)
    n_voters = elec.n_voters
    manip_successes = 0
    manip_harms = 0
    trials = 0
    for v in range(n_voters):
        for issue in range(elec.n_issues):
            trials += 1
            flipped = elec.approvals.copy()
            flipped[v, issue, :] = 1 - flipped[v, issue, :]
            new_elec = MultiIssueElection(flipped)
            new_out = rule(new_elec)
            if new_out.winners != baseline.winners:
                manip_successes += 1
                manip_harms += 1
    return dict(trials=trials, successes=manip_successes, harms=manip_harms)

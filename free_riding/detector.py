# File: free_riding/detector.py
import numpy as np
from core.types import MultiIssueElection, Outcome


def normalize_outcome(out) -> Outcome:
    """
    Ensure that the output of a voting rule is wrapped as an Outcome.
    Accepts either a list of winners or an Outcome object.
    """
    if isinstance(out, Outcome):
        return out
    elif isinstance(out, list):
        return Outcome(winners=out)
    else:
        raise TypeError(f"Unsupported outcome type: {type(out)}")


def voter_utility(elec: MultiIssueElection, outcome: Outcome, voter: int) -> int:
    """
    Compute the utility of a single voter for the given outcome
    (i.e., how many of the winners they approved).
    """
    score = 0
    for issue, cand in enumerate(outcome.winners):
        score += elec.approvals[voter, issue, cand]
    return score


def detect_free_riding(elec: MultiIssueElection, rule, max_flips: int = 1) -> dict:
    """
    Detect free-riding manipulations in a multi-issue election.

    Parameters
    ----------
    elec : MultiIssueElection
        Election instance with voter approvals.
    rule : callable
        Voting rule mapping MultiIssueElection -> Outcome (or list of winners).
    max_flips : int
        Max number of preference flips per voter/issue to consider.

    Returns
    -------
    dict with counts of trials, successes, and harms.
    """
    baseline = normalize_outcome(rule(elec))

    n_voters, n_issues, _ = elec.approvals.shape
    trials = 0
    successes = 0
    harms = 0

    for v in range(n_voters):
        base_util = voter_utility(elec, baseline, v)

        for issue in range(n_issues):
            trials += 1

            # Flip all approvals for this voter on this issue
            flipped = elec.approvals.copy()
            flipped[v, issue, :] = 1 - flipped[v, issue, :]

            new_elec = MultiIssueElection(flipped)
            new_out = normalize_outcome(rule(new_elec))

            new_util = voter_utility(new_elec, new_out, v)

            if new_out.winners != baseline.winners:
                if new_util > base_util:
                    successes += 1
                elif new_util < base_util:
                    harms += 1
                # if equal, neither success nor harm

    return dict(trials=trials, successes=successes, harms=harms)

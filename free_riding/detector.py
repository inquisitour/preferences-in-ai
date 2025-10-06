# File: free_riding/detector.py
import numpy as np
from core.types import MultiIssueElection, Outcome


def normalize_outcome(out) -> Outcome:
    """Wrap rule output as Outcome."""
    if isinstance(out, Outcome):
        return out
    if isinstance(out, list):
        return Outcome(winners=out)
    raise TypeError(f"Unsupported outcome type: {type(out)}")


def voter_utility_truthful(elec: MultiIssueElection, outcome: Outcome, voter: int) -> int:
    """Utility of voter under the *truthful* ballot (count approved winners)."""
    score = 0
    for i, w in enumerate(outcome.winners):
        score += elec.approvals[voter, i, w]
    return int(score)


def detect_free_riding(elec: MultiIssueElection, rule) -> dict:
    """
    Detect free-riding following the paper + Oliviero’s clarifications.

    For each voter v and issue i:
      • Consider free-riding only if v approved the original winner on i (eligibility).
      • Manipulation = drop that single approval on issue i; keep all other approvals identical.
      • Compute new outcome with the manipulated election.
      • Free-riding is *possible* if the winner of issue i remains unchanged (non-pivotal).
      • If possible, compare utilities using the *truthful* ballot:
          Δu = u_truthful(new_out) - u_truthful(baseline_out)
        Count success if Δu>0, harm if Δu<0; ignore Δu==0.
    Returns counts:
      trials (= n_voters*n_issues),
      eligible (# approved the original winner on that issue),
      possible (# non-pivotal manipulations),
      successes, harms.
    """
    baseline = normalize_outcome(rule(elec))

    n_voters, n_issues, _ = elec.approvals.shape
    trials = n_voters * n_issues

    eligible = 0
    possible = 0
    successes = 0
    harms = 0

    # Precompute truthful utilities vs baseline for all voters
    base_utils = [voter_utility_truthful(elec, baseline, v) for v in range(n_voters)]

    for v in range(n_voters):
        for i in range(n_issues):
            orig_winner = baseline.winners[i]

            # Only consider if voter approved the original winner on this issue
            if elec.approvals[v, i, orig_winner] != 1:
                continue
            eligible += 1

            # Build manipulated election: identical except drop that single approval
            approvals_new = elec.approvals.copy()
            approvals_new[v, i, orig_winner] = 0  # drop only this approval
            new_elec = MultiIssueElection(approvals_new)

            new_out = normalize_outcome(rule(new_elec))

            # Free-riding is defined only if the winner on issue i remains unchanged
            if new_out.winners[i] != orig_winner:
                continue
            possible += 1

            # Evaluate effect using the truthful ballot
            new_util = voter_utility_truthful(elec, new_out, v)
            if new_util > base_utils[v]:
                successes += 1
            elif new_util < base_utils[v]:
                harms += 1
            # else Δu==0 → neither success nor harm

    return {
        "trials": trials,
        "eligible": eligible,
        "possible": possible,
        "successes": successes,
        "harms": harms,
    }

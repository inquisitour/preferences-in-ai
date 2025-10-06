# File: free_riding/risk.py
from free_riding.detector import detect_free_riding
from core.types import MultiIssueElection


def evaluate_risk(elec: MultiIssueElection, rule) -> dict:
    """
    Summarize free-riding outcomes.

    Returns:
      - trials: total (voter, issue) pairs = n_voters * n_issues
      - eligible: # pairs where voter approved the original winner
      - possible: # eligible pairs where dropping that approval keeps the winner of that issue
      - successes, harms
      - success_rate := successes / trials
      - harm_rate    := harms / trials
      - risk         := harms / possible   (paper’s definition; 0 if possible==0)
    """
    res = detect_free_riding(elec, rule)

    trials = res["trials"]
    eligible = res["eligible"]
    possible = res["possible"]
    successes = res["successes"]
    harms = res["harms"]

    return {
        "trials": trials,
        "eligible": eligible,
        "possible": possible,
        "successes": successes,
        "harms": harms,
        "success_rate": successes / trials if trials else 0.0,
        "harm_rate": harms / trials if trials else 0.0,
        "risk": harms / possible if possible else 0.0,
    }

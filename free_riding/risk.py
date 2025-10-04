# File: free_riding/risk.py
from free_riding.detector import detect_free_riding
from core.types import MultiIssueElection


def evaluate_risk(elec: MultiIssueElection, rule) -> dict:
    """
    Evaluate manipulation risks for a given election and rule.

    Parameters
    ----------
    elec : MultiIssueElection
        Election instance with voter approvals.
    rule : callable
        Voting rule mapping MultiIssueElection -> Outcome (or list of winners).

    Returns
    -------
    dict with:
      - trials: total manipulation attempts
      - successes: # of successful manipulations
      - harms: # of harmful manipulations
      - success_rate: successes / trials
      - harm_rate: harms / trials
      - risk: harms / (successes + harms)  # proportion of harmful manipulations
    """
    res = detect_free_riding(elec, rule)
    trials = float(res["trials"])
    successes = float(res["successes"])
    harms = float(res["harms"])
    possible = successes + harms

    return {
        "trials": trials,
        "successes": successes,
        "harms": harms,
        "success_rate": successes / trials if trials > 0 else 0.0,
        "harm_rate": harms / trials if trials > 0 else 0.0,
        "risk": harms / possible if possible > 0 else 0.0,
    }

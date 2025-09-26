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
    """
    res = detect_free_riding(elec, rule)
    trials = res["trials"]

    return {
        "trials": trials,
        "successes": res["successes"],
        "harms": res["harms"],
        "success_rate": res["successes"] / trials if trials else 0.0,
        "harm_rate": res["harms"] / trials if trials else 0.0,
    }

from free_riding.detector import detect_free_riding
from core.types import MultiIssueElection

def evaluate_risk(elec: MultiIssueElection, rule):
    res = detect_free_riding(elec, rule)
    trials = res["trials"]
    return {
        "trials": trials,
        "successes": res["successes"],
        "harms": res["harms"],
        "success_rate": res["successes"] / trials if trials else 0,
        "harm_rate": res["harms"] / trials if trials else 0,
    }

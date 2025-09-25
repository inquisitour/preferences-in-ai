from core.types import utilitarian_welfare, egalitarian_welfare, nash_welfare, Outcome, MultiIssueElection

def welfare_summary(elec: MultiIssueElection, outcome: Outcome):
    return {
        "utilitarian": utilitarian_welfare(elec, outcome),
        "egalitarian": egalitarian_welfare(elec, outcome),
        "nash": nash_welfare(elec, outcome),
    }

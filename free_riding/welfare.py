# File: free_riding/welfare.py
from core.types import MultiIssueElection, Outcome, utilitarian_welfare, egalitarian_welfare, nash_welfare


def welfare_summary(elec: MultiIssueElection, winners) -> dict:
    """
    Compute a summary of welfare metrics for a given election outcome.

    Parameters
    ----------
    elec : MultiIssueElection
        The election instance with voter approvals.
    winners : list[int] or Outcome
        Either a list of candidate winners (one per issue),
        or an Outcome object.

    Returns
    -------
    dict
        {
            "utilitarian": float,
            "egalitarian": float,
            "nash": float
        }
    """
    # Normalize winners into Outcome
    if isinstance(winners, Outcome):
        outcome = winners
    else:
        outcome = Outcome(winners=list(winners))

    return {
        "utilitarian": utilitarian_welfare(elec, outcome),
        "egalitarian": egalitarian_welfare(elec, outcome),
        "nash": nash_welfare(elec, outcome),
    }

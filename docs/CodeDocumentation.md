# Code Documentation

This document explains the main modules and their responsibilities.

---

## `core/`

- **`types.py`**
  - `MultiIssueElection`: stores approval preferences as a NumPy array  
    (shape: n_voters × n_issues × n_candidates).
  - `Outcome`: winners per issue.

---

## `statistical_cultures/`

Preference generators used to create synthetic elections:

- **`p_ic.py`**
  - `PICConfig`: config for per-issue impartial culture (p-IC).
  - `sample_p_ic`: generates elections under p-IC.

- **`disjoint.py`**
  - `DisjointConfig`: voters partitioned into `n_groups` with internally aligned preferences.
  - `sample_disjoint`: generates elections from the disjoint model.

- **`resampling.py`**
  - `ResamplingConfig`: $(p, \phi)$ resampling with correlation across issues.
  - `sample_resampling`: generates elections from the resampling model.

- **`hamming_noise.py`**
  - `HammingConfig`: wraps a base culture (`p_ic`, `resampling`, or `disjoint`) and adds noise.
  - `sample_hamming`: samples from the base culture and flips approvals with probability `noise`.

---

## `voting_rules/`

- **`utilitarian.py`** – Implements the Sequential Utilitarian rule (equivalent to mean OWA, fully manipulation-immune).
- **`sequential_thiele.py`** – Implements the Sequential Thiele family with parameter x∈{1,5,7}; includes seq-PAV, seq-CC, and intermediate proportionality levels.
- **`owa.py`** – Implements the Sequential OWA family following Lackner et al. (2023, Sec. 5):
      - Parametric OWA with x∈{1,5,10,15}, interpolating between utilitarian (x=0) and leximin (x=n−1).

      - Leximin OWA, the limiting case maximizing the welfare of the worst-off voter.

      - All OWA weight vectors are now strictly positive (no zeros), normalized, and consistent with the definitions in the paper.

All rules return an `Outcome` (list of winners per issue).

---

## `free_riding/`

- **`detector.py`**
  - `detect_free_riding(elec, rule)`: Implements the free-riding definition consistent with \cite{lackner2023freeriding}.
    For each voter and issue:

      -  Checks eligibility (the voter originally approved the winner).

      -  Tests a restricted deviation where the voter drops only that approval, keeping all other approvals fixed.

      -  The deviation is counted as possible only if the issue winner remains unchanged (non-pivotal).

      -  The election is recomputed with the manipulated ballot, and the utility difference is computed using the voter’s truthful preferences.

- **`risk.py`**
  - `evaluate_risk(elec, rule)`: aggregates detector outputs into summary statistics: trials, eligible, possible, successes, harms,success_rate, harm_rate, and risk = harms / possible (conditional probability of harmful manipulation).

---

## `experiments/`

- **`run_experiments.py`**
  - Runs batch experiments across all cultures × rules × seeds.  
  - Computes and saves manipulation metrics consistent with the updated definition: trials, eligible, possible, successes, harms, success_rate, harm_rate, and risk = harms / possible.
  - Outputs:
        - results/combined.csv – consolidated numeric results

        - report/tables/combined.tex – LaTeX table for the report

- **`plot_results.py`**
  - Generates per-culture bar charts for success, harm, and risk metrics, plus an overview plot.
  - Plots saved under report/figures/.

---

## `report/`

- **`report.tex`** – Main LaTeX report integrating generated figures and tables.
- **`tables/combined.tex`** – Auto-generated LaTeX summary table from experiment results.
- **`figures/`** – Contains risk plots (risk_<culture>_<family>.pdf) and risk_overview.pdf.

---

## `tests/`

Pytest suite for cultures, rules, free-riding detection, and risk aggregation.

Run with:
```bash
python -m pytest tests/
```

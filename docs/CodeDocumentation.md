# Code Documentation

This document explains the functionality of each module in the project.

---

## `core/`
- **types.py**  
  Defines fundamental data structures (e.g., `Voter`, `Election`) and utility functions for computing welfare.  
  Also contains a common interface for voting rules.

---

## `statistical_cultures/`
- **p_ic.py**  
  Implements the per-issue impartial culture model, resampling independent preferences for each issue.
- **disjoint.py**  
  Implements disjoint groups: voters are clustered into fixed groups across issues.
- **resampling.py**  
  Implements the (p, φ)-resampling model: voters’ preferences are perturbed with probabilities p and φ.
- **hamming_noise.py**  
  Provides robustness tests by flipping preferences with some probability.

---

## `voting_rules/`
- **utilitarian.py**  
  Implements sequential utilitarian voting: at each issue, choose the candidate maximizing total approvals.
- **sequential_thiele.py**  
  Generic implementation of sequential Thiele methods, including seq-PAV via harmonic weights.

---

## `free_riding/`
- **detector.py**  
  Brute-force and sampled manipulation detection. Tests whether a voter can gain by strategic voting.
- **welfare.py**  
  Computes welfare outcomes under different rules, used in result tables.
- **risk.py**  
  Summarizes manipulation success and harm rates across experiments.

---

## `experiments/`
- **run_experiments.py**  
  End-to-end experiment pipeline: generates elections, applies rules, detects free-riding, outputs CSV + LaTeX tables.

---

## `tests/`
- Unit tests for statistical cultures, rules, and free-riding detectors.

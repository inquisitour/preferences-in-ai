# Code Documentation

This document provides a detailed explanation of each module in the project.

---

## `core/`
- **types.py**:  
  Defines fundamental dataclasses and utilities:  
  - `ElectionConfig`: number of voters, issues, candidates.  
  - `PreferenceProfile`: stores voter preferences.  
  - Welfare metrics (utilitarian, egalitarian, Nash).  
  - Base interface for voting rules.

---

## `statistical_cultures/`
Implements different models of generating preferences ("statistical cultures"):

- **p_ic.py**: Per-issue impartial culture (random independent draws).  
- **disjoint.py**: Divides voters into fixed groups with aligned preferences.  
- **resampling.py**: (p, φ)-resampling model where preferences are perturbed/resampled.  
- **hamming_noise.py**: Adds random perturbations to preferences for robustness tests.

---

## `voting_rules/`
Sequential multi-issue decision rules:

- **utilitarian.py**: Sequential utilitarian rule (chooses alternative maximizing total approvals).  
- **sequential_thiele.py**: General sequential Thiele method (specializes to seq-PAV with harmonic weights).

---

## `free_riding/`
Detects manipulation opportunities and measures robustness:

- **detector.py**: Brute-force / sampled search for free-riding manipulations.  
- **welfare.py**: Wraps welfare calculations for experiments.  
- **risk.py**: Summarizes manipulation risk (success rate, harm rate).

---

## `experiments/`
- **run_experiments.py**: Main driver script. Runs experiments across statistical cultures and voting rules.  
  Features:  
  - Batch mode (`--batch all`) for all rules/cultures.  
  - Outputs CSV and LaTeX tables.  
  - Supports seeds, voters, candidates, and parameter sweeps.

---

## `report/`
- **report.tex**: LaTeX report including tables and discussion.  
- **tables/**: Auto-generated LaTeX tables (`combined.tex`).  
- **references.bib**: Bibliography (AAMAS 2023 paper).

---

## `tests/`
Unit tests for reproducibility and correctness:  
- **test_cultures.py**: Checks preference generators.  
- **test_rules.py**: Verifies voting rule outputs.  
- **test_free_riding.py**: Ensures manipulation detection works.

---

## `docs/`
- **CodeDocumentation.md** (this file): Human-readable explanation of the project structure.

---

## Experiment Workflow
1. Generate preferences (`statistical_cultures`).  
2. Apply a voting rule (`voting_rules`).  
3. Run free-riding detection (`free_riding`).  
4. Collect welfare & risk metrics.  
5. Summarize into CSV + LaTeX (`experiments/run_experiments.py`).  
6. Include results in `report/report.tex`.  

---

## References
- Lackner, Maly, Nardi (AAMAS 2023): *Free-Riding in Multi-Issue Decisions*.  

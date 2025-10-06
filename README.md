# Preferences in AI – Free-Riding in Sequential Voting

This project replicates and extends the experiments from  
**Lackner & al. (2023), "Free-Riding in Multi-Issue Decisionsg"**.

We study **free-riding** (strategic manipulation) in **multi-issue elections** under different **statistical cultures** and voting rules.

---

## Implemented Cultures

- **p-IC** – per-issue impartial culture (preferences sampled independently).
- **Disjoint Groups** – voters partitioned into groups with aligned preferences.
- **Resampling Model** – $(p, \phi)$-resampling controlling correlation strength.
- **Hamming Noise** – preferences sampled from a base culture, then perturbed by flipping approvals with probability $\epsilon$.

---

## Implemented Voting Rules

- **Sequential Utilitarian** – selects the candidate with the highest total approvals per issue (equivalent to mean OWA; immune to manipulation).
- **Sequential Thiele Rules** – a parametric family of rules (e.g., seq-PAV, seq-CC) with parameters x∈{1,5,7} controlling proportionality.
- **Sequential OWA Rules** – aggregate voter satisfaction via Ordered Weighted Averages (OWAs), following Section 5 of Lackner et al. (2023):
  - **Leximin OWA** – limiting case maximizing the welfare of the worst-off voter.
  - **Parametric OWA ($x=1,5,10,15$)** – interpolating smoothly between utilitarian (x=0) and leximin (x=n−1); all weights are strictly positive and normalized (no zeros).

---

## Free-riding operationalization (used in the experiments):

A voter can attempt to free-ride on issue i only if they originally approved the winning candidate on i (eligible).

We test a restricted deviation: drop that single approval on issue i; all other approvals stay truthful. The manipulation is counted as possible only if the winner on i does not change (non-pivotal).

The rule is run on the manipulated profile, but the voter’s gain/harm is measured using their truthful utilities.

Reported metrics: trials, eligible, possible, successes, harms, success_rate, harm_rate, and
risk = harms / possible.

---

## Quickstart

### 1) Install
```bash
pip install -r requirements.txt
```

### 2) Run all experiments
```bash
python -m experiments.run_experiments --batch all --n_voters 20 --issues 5 --cands 4 --seeds 200 --csv results/combined.csv --latex report/tables/combined.tex --summary
```
Outputs:
- `results/combined.csv` – raw experiment results
- `report/tables/combined.tex` – LaTeX summary table

### 3) Plot results
```bash
python -m experiments.plot_results
```

Generates bar charts of success rate, harm rate, and risk (harms / possible):

Per culture × family:
report/figures/risk_<culture>_thiele.pdf and report/figures/risk_<culture>_owa.pdf

Overview across all cultures:
report/figures/risk_overview.pdf

### 4) Build the report (optional)
Open `report/report.tex` in your LaTeX editor and compile. The table and figures are included automatically.

---

## Running Tests

Make sure you run **from the repository root**:
```bash
# Option A
python -m pytest tests/

# Option B (quiet)
pytest -q tests/
```
If imports fail, verify you are in the repo root and that dependencies are installed.

---

## Project Layout

```
core/                 # Core types and interfaces
statistical_cultures/ # Preference generators (p-IC, disjoint, resampling, hamming)
voting_rules/         # Implementations of utilitarian, Thiele, and OWA rules
free_riding/          # Manipulation detector and risk evaluation
experiments/          # Experiment runner and plotting scripts
report/               # LaTeX sources, figures, generated tables
tests/                # Unit tests
docs/                 # Detailed code documentation
```

👉 **Detailed Code Documentation:** see [`docs/CodeDocumentation.md`](docs/CodeDocumentation.md)  
👉 **Generated Report:** see [`report/report.pdf`](report/report.pdf)  

---

## References

- Lackner, M., Maly, J., & Nardi, O. (2023).  
  *Free-Riding in Multi-Issue Decisions*.  
  [Free Riding (PDF)](https://dbai.tuwien.ac.at/staff/jmaly/freeriding.pdf)

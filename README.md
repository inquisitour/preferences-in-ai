# Preferences in AI – Free-Riding in Sequential Voting

This project replicates and extends the experiments from  
**Lackner & al. (2023), "Free-Riding in Sequential Multi-Winner Voting"**.

We study **free-riding** (strategic manipulation) in **multi-issue elections** under different **statistical cultures** and voting rules.

---

## Implemented Cultures

- **p-IC** – per-issue impartial culture (preferences sampled independently).
- **Disjoint Groups** – voters partitioned into groups with aligned preferences.
- **Resampling Model** – $(p, \phi)$-resampling controlling correlation strength.
- **Hamming Noise** – preferences sampled from a base culture, then perturbed by flipping approvals with probability $\epsilon$.

---

## Implemented Voting Rules

- **Sequential Utilitarian** – picks candidate with most approvals per issue (baseline).
- **Sequential Thiele Rules** – parametric family including seq-PAV, seq-CC, and intermediate $x$-values.
- **Sequential OWA Rules**:
  - **Leximin OWA** – maximizes worst-off voter’s satisfaction.
  - **Parametric OWA ($x=1,5,10,15$)** – interpolating between utilitarian and leximin.

---

## Quickstart

### 1) Install
```bash
pip install -r requirements.txt
```

### 2) Run all experiments
```bash
python -m experiments.run_experiments --batch all --n_voters 20 --issues 5 --cands 4 --seeds 30   --csv results/combined.csv --latex report/tables/combined.tex --summary
```
Outputs:
- `results/combined.csv` – raw experiment results
- `report/tables/combined.tex` – LaTeX summary table

### 3) Plot results
```bash
python -m experiments.plot_results
```
Plots are saved to `report/figures/`.

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

- Lackner, M., Maly, J., & Schmidt-Kraepelin, U. (2023).  
  *Free-Riding in Sequential Multi-Winner Voting*.  
  [Free Riding (PDF)](https://dbai.tuwien.ac.at/staff/jmaly/freeriding.pdf)

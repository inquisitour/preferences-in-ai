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

- **Sequential Utilitarian** – picks candidate with most approvals per issue.
- **Sequential PAV** – proportional approval voting with harmonic weights.
- **Sequential CC** – Chamberlin–Courant, rewarding first approvals.
- **Sequential OWA rules**:
  - **Leximin OWA** – maximizes worst-off voter’s satisfaction.
  - **Mean OWA** – averages satisfaction across voters.

---

## Evaluation Metrics

- **Welfare metrics:**
  - Utilitarian welfare
  - Egalitarian welfare
  - Nash welfare
- **Manipulation risk metrics:**
  - Trials (manipulation attempts)
  - Successes (beneficial manipulations)
  - Harms (backfiring manipulations)
  - Success rate
  - Harm rate

---

## Running Experiments

Run all experiments and save results:

```bash
python -m experiments.run_experiments --batch all --n_voters 20 --issues 5 --cands 4 --seeds 30   --csv results/combined.csv --latex report/tables/combined.tex --summary
```

This produces:
- `results/combined.csv` – raw experiment results
- `report/tables/combined.tex` – LaTeX summary table

---

## Plotting Results

Generate plots for welfare and risk comparisons:

```bash
python -m experiments.plot_results
```

This saves plots to `report/figures/`.

---

## Report

The full report (LaTeX + PDF) is in `report/`.  
It includes:
- Background on models, rules, and cultures
- Combined results table
- Global comparison figures
- Per-culture figures (appendix)
- Discussion and conclusion

---

## Repository Structure

```
core/                # Core types and welfare metrics
statistical_cultures/ # Preference generators (p-IC, disjoint, resampling, hamming)
voting_rules/        # Implementations of utilitarian, PAV, CC, OWA rules
free_riding/         # Manipulation detector, risk/welfare evaluation
experiments/         # Experiment runner and plotting scripts
report/              # LaTeX sources, figures, generated tables
tests/               # Unit tests
```

---

## References

- Lackner, M., Maly, J., & Schmidt-Kraepelin, U. (2023).  
  *Free-Riding in Sequential Multi-Winner Voting*.  
  [arXiv:2302.06685](https://arxiv.org/abs/2302.06685)

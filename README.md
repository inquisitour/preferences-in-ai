# Preferences in AI Project

📌 TU Wien – Logic & Computation  
📌 Course: Preferences in AI  
📌 Author: Pratik Deshmukh  

## Overview
This project replicates and extends experiments from  
[Nardi, Faliszewski, Lackner (AAAI 2022)](https://doi.org/10.1609/aaai.v36i5.20337)  
on **free-riding in sequential approval voting**, using different *statistical cultures* for preference generation.

Implemented cultures:
- **p-IC** (per-issue impartial culture)
- **Disjoint Groups**
- **(p, φ)-Resampling model**

Implemented voting rules:
- Sequential **Utilitarian**
- Sequential **PAV** (via Thiele scores)

The experiments evaluate **welfare** (utilitarian, egalitarian, Nash) and **manipulation risks** (success & harm rates).

## Repository Structure
```
core/                   # types, dataclasses, utilities
statistical_cultures/   # preference generation models
voting_rules/           # voting rules (utilitarian, seq-Thiele/PAV)
free_riding/            # manipulation detectors, welfare & risk metrics
experiments/            # experiment runner (main entry point)
report/                 # LaTeX report, tables, references
tests/                  # unit tests
requirements.txt
.gitignore
```

## Installation
Clone the repo and install dependencies:
```bash
git clone https://github.com/inquisitour/preferences-in-ai.git
cd preferences-in-ai
pip install -r requirements.txt
```

## Running Experiments
To run all experiments (with default parameters and save results + LaTeX tables):
```bash
run_all.bat   # Windows
./run_all.sh  # Linux / macOS
```

Or run manually:
```bash
python -m experiments.run_experiments --batch all --n_voters 20 --issues 5 --cands 4 --seeds 30 --latex report/tables/combined.tex --csv results/combined.csv --summary
```

## How to Reproduce
To exactly reproduce the results in the report:
- Number of voters: **20**
- Number of issues: **5**
- Candidates per issue: **4**
- Number of seeds (repetitions): **30**
- Cultures tested: **p-IC, Disjoint, Resampling**
- Rules tested: **Utilitarian, PAV (seq-Thiele)**

This will regenerate:
- `results/combined.csv` (full numerical results)
- `report/tables/combined.tex` (LaTeX table for direct inclusion in the report)

## Results
- CSV results: `results/combined.csv`
- LaTeX tables: `report/tables/combined.tex`
- Final report: `report/report.pdf`

## Report
The full report (with analysis and discussion) is available in  
[`report/report.pdf`](report/report.pdf).

## Repository Link in Report
The GitHub repository link is also included in the submitted LaTeX report:  
[https://github.com/inquisitour/preferences-in-ai](https://github.com/inquisitour/preferences-in-ai)

## License
This repository is for academic coursework at TU Wien.  
Not intended for production use.

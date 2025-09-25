#!/bin/bash
# Run all experiments across cultures × rules with 30 seeds
# Results saved to CSV + LaTeX for direct inclusion in report.

set -e

# Activate virtual environment if exists
if [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

echo "Running all experiments..."
python -m experiments.run_experiments \
    --batch all \
    --n_voters 20 \
    --issues 5 \
    --cands 4 \
    --seeds 30 \
    --csv results/combined.csv \
    --latex report/tables/combined.tex \
    --summary

echo "✅ Experiments finished."
echo "Results saved to results/combined.csv and report/tables/combined.tex"
echo "You can now run 'python -m experiments.plot_results' to generate plots."
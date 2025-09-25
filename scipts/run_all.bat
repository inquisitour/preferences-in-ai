@echo off
echo Running all experiments...

REM change directory to project root (adjust path if needed)
cd /d %~dp0..
python -m experiments.run_experiments --batch all --n_voters 20 --issues 5 --cands 4 --seeds 30 --csv results/combined.csv --latex report/tables/combined.tex --summary

echo Experiments finished.
pause
echo Results saved to results/combined.csv and report/tables/combined.tex
echo You can now run 'python -m experiments.plot_results' to generate plots.
# File: experiments/run_experiments.py
# Clean version following Section 5 setup: only risk metrics, no welfare

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List, Callable
import pandas as pd

from core.types import MultiIssueElection
from free_riding.risk import evaluate_risk

# Cultures
from statistical_cultures.p_ic import sample_p_ic, PICConfig
from statistical_cultures.disjoint import sample_disjoint, DisjointConfig
from statistical_cultures.resampling import sample_resampling, ResamplingConfig
from statistical_cultures.hamming_noise import add_hamming_noise
from statistical_cultures.hamming_noise import HammingConfig, sample_hamming

# Rules
from voting_rules.utilitarian import sequential_utilitarian
from voting_rules.sequential_thiele import sequential_thiele
from voting_rules.owa import owa_rule, leximin_owa


# =====================
# RULES
# =====================
def make_rules(n_voters: int) -> Dict[str, Callable[[MultiIssueElection], object]]:
    """
    Construct rules dictionary dynamically.
    Includes Thiele rules, utilitarian, and parametric OWA rules.
    """
    rules: Dict[str, Callable] = {
        # Utilitarian as baseline (same as Thiele x=0 and OWA mean)
        "utilitarian": lambda elec: sequential_utilitarian(elec),
    }

    # Parametric Thiele rules (subset suggested by professor)
    thiele_x_values = [1, 5, 7]  # drop x=0 (utilitarian already included)
    for x in thiele_x_values:
        rules[f"thiele_x{x}"] = lambda elec, xx=x: sequential_thiele(elec, x=xx)

    # Parametric OWA rules (subset suggested by professor)
    owa_x_values = [1, 5, 10, 15]
    for x in owa_x_values:
        rules[f"owa_x{x}"] = lambda elec, xx=x: owa_rule(elec, x=xx)

    # Leximin OWA for completeness
    rules["owa_leximin"] = lambda elec: leximin_owa(elec)

    return rules


# Now includes Hamming
CULTURES = ["p_ic", "disjoint", "resampling", "hamming"]


# =====================
# EXPERIMENT RUNNERS
# =====================
def run_single_experiment(elec: MultiIssueElection, rules: Dict[str, Callable]) -> Dict:
    results = {}
    for name, func in rules.items():
        out = func(elec)
        results[name] = {
            "winners": out.winners,
            "risk": evaluate_risk(elec, func),
        }
    return results


def run_batch(
    culture: str,
    rule: str,
    n_voters: int,
    issues: int,
    cands: int,
    seeds: int,
    p: float = 0.5,
    phi: float = 0.5,
    groups: int = 2,
    noise_prob: float = 0.1,
) -> pd.DataFrame:
    cands_per_issue = [cands] * issues
    rows = []
    rules = make_rules(n_voters)

    for s in range(seeds):
        # ---- culture selection ----
        if culture == "p_ic":
            cfg = PICConfig(n_voters=n_voters, candidates_per_issue=cands_per_issue, p=p, seed=s)
            elec = sample_p_ic(cfg)
        elif culture == "disjoint":
            cfg = DisjointConfig(
                n_voters=n_voters, candidates_per_issue=cands_per_issue,
                n_groups=groups, p=p, seed=s
            )
            elec = sample_disjoint(cfg)
        elif culture == "resampling":
            cfg = ResamplingConfig(
                n_voters=n_voters, candidates_per_issue=cands_per_issue,
                p=p, phi=phi, seed=s
            )
            elec = sample_resampling(cfg)
        elif culture == "hamming":
            cfg = HammingConfig(
                base="p_ic",   # default base culture
                n_voters=n_voters,
                candidates_per_issue=cands_per_issue,
                p=p,
                phi=phi,
                groups=groups,
                noise_prob=noise_prob,
                seed=s
            )
            elec = sample_hamming(cfg)
        else:
            raise ValueError("Unknown culture")

        # ---- rule application ----
        rule_func = rules[rule]
        out = rule_func(elec)
        risk = evaluate_risk(elec, rule_func)

        rows.append({
            "seed": s,
            "culture": culture,
            "rule": rule,
            "winners": out.winners,
            **risk,
        })
    return pd.DataFrame(rows)


def summarize_results(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.drop(columns=["winners", "seed"]).mean(numeric_only=True)
    summary = agg.to_frame(name="mean").T
    summary.insert(0, "culture", df["culture"].iloc[0])
    summary.insert(1, "rule", df["rule"].iloc[0])
    summary.insert(2, "seeds", df.shape[0])
    return summary


def df_to_latex_table(df: pd.DataFrame, file: str) -> None:
    os.makedirs(os.path.dirname(file), exist_ok=True)

    latex_str = df.to_latex(
        index=False,
        float_format="{:.3f}".format,
        escape=True,
        longtable=False,
        multicolumn=True,
        multicolumn_format='c',
        bold_rows=False,
    )
    latex_str = latex_str.replace(r"\hline", r"\midrule")

    with open(file, "w") as f:
        f.write(latex_str)
    print(f"Saved LaTeX table to {file}")


# =====================
# CLI ENTRYPOINT
# =====================
def main():
    parser = argparse.ArgumentParser(description="Run free-riding experiments.")
    parser.add_argument("--culture", choices=CULTURES, help="single culture run")
    parser.add_argument("--rule", help="rule to evaluate")
    parser.add_argument("--n_voters", type=int, default=10)
    parser.add_argument("--issues", type=int, default=3)
    parser.add_argument("--cands", type=int, default=3)
    parser.add_argument("--p", type=float, default=0.5)
    parser.add_argument("--phi", type=float, default=0.5)
    parser.add_argument("--groups", type=int, default=2)
    parser.add_argument("--seeds", type=int, default=1)
    parser.add_argument("--noise_prob", type=float, default=0.1)
    parser.add_argument("--csv", type=str, default=None)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--latex", type=str, default=None)
    parser.add_argument("--batch", choices=["all"], help="run all cultures × rules")
    args = parser.parse_args()

    rules = make_rules(args.n_voters)

    if args.batch == "all":
        all_summaries: List[pd.DataFrame] = []
        for culture in CULTURES:
            for rule in rules.keys():
                df = run_batch(
                    culture=culture,
                    rule=rule,
                    n_voters=args.n_voters,
                    issues=args.issues,
                    cands=args.cands,
                    seeds=args.seeds,
                    p=args.p,
                    phi=args.phi,
                    groups=args.groups,
                    noise_prob=args.noise_prob,
                )
                summary = summarize_results(df)
                all_summaries.append(summary)
        combined = pd.concat(all_summaries, ignore_index=True)
        print("Combined summary:\n", combined)
        if args.latex:
            df_to_latex_table(combined, args.latex)
        if args.csv:
            os.makedirs(os.path.dirname(args.csv), exist_ok=True)
            combined.to_csv(args.csv, index=False)
            print(f"Saved combined results to {args.csv}")
        return

    if args.seeds > 1 or args.csv or args.summary or args.latex:
        df = run_batch(
            culture=args.culture,
            rule=args.rule,
            n_voters=args.n_voters,
            issues=args.issues,
            cands=args.cands,
            seeds=args.seeds,
            p=args.p,
            phi=args.phi,
            groups=args.groups,
            noise_prob=args.noise_prob,
        )
        if args.csv:
            os.makedirs(os.path.dirname(args.csv), exist_ok=True)
            df.to_csv(args.csv, index=False)
            print(f"Saved detailed results to {args.csv}")
        if args.summary or args.latex:
            summary = summarize_results(df)
            print("\nSummary statistics:")
            print(summary.to_string(index=False))
            if args.latex:
                df_to_latex_table(summary, args.latex)
    else:
        # single run
        if args.culture == "p_ic":
            cfg = PICConfig(n_voters=args.n_voters, candidates_per_issue=[args.cands]*args.issues, p=args.p, seed=args.seeds)
            elec = sample_p_ic(cfg)
        elif args.culture == "disjoint":
            cfg = DisjointConfig(n_voters=args.n_voters, candidates_per_issue=[args.cands]*args.issues, n_groups=args.groups, p=args.p, seed=args.seeds)
            elec = sample_disjoint(cfg)
        elif args.culture == "resampling":
            cfg = ResamplingConfig(n_voters=args.n_voters, candidates_per_issue=[args.cands]*args.issues, p=args.p, phi=args.phi, seed=args.seeds)
            elec = sample_resampling(cfg)
        elif args.culture == "hamming":
            cfg = PICConfig(n_voters=args.n_voters, candidates_per_issue=[args.cands]*args.issues, p=args.p, seed=args.seeds)
            base = sample_p_ic(cfg)
            elec = add_hamming_noise(base, noise_prob=args.noise_prob, seed=args.seeds)
        else:
            raise ValueError("Unknown culture")

        rule_func = rules[args.rule]
        results = run_single_experiment(elec, {args.rule: rule_func})
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

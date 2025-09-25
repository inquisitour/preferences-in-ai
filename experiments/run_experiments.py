# File: experiments/run_experiments.py
# (Final version with LaTeX export, grouping, batch all, etc.)

from __future__ import annotations

import argparse
import json
from typing import Dict, List
import pandas as pd

from core.types import MultiIssueElection
from free_riding.welfare import welfare_summary
from free_riding.risk import evaluate_risk

# Cultures
from statistical_cultures.p_ic import sample_p_ic, PICConfig
from statistical_cultures.disjoint import sample_disjoint, DisjointConfig
from statistical_cultures.resampling import sample_resampling, ResamplingConfig

# Rules
from voting_rules.utilitarian import run_seq_utilitarian
from voting_rules.sequential_thiele import run_seq_pav

RULES = {
    "utilitarian": run_seq_utilitarian,
    "pav": run_seq_pav,
}

CULTURES = ["p_ic", "disjoint", "resampling"]


def run_single_experiment(elec: MultiIssueElection, rules: Dict[str, callable]):
    results = {}
    for name, func in rules.items():
        out = func(elec)
        results[name] = {
            "winners": out.winners,
            "welfare": welfare_summary(elec, out),
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
) -> pd.DataFrame:
    cands_per_issue = [cands] * issues
    rows = []
    for s in range(seeds):
        if culture == "p_ic":
            cfg = PICConfig(n_voters=n_voters, candidates_per_issue=cands_per_issue, p=p, seed=s)
            elec = sample_p_ic(cfg)
        elif culture == "disjoint":
            cfg = DisjointConfig(n_voters=n_voters, candidates_per_issue=cands_per_issue, n_groups=groups, p=p, seed=s)
            elec = sample_disjoint(cfg)
        elif culture == "resampling":
            cfg = ResamplingConfig(n_voters=n_voters, candidates_per_issue=cands_per_issue, p=p, phi=phi, seed=s)
            elec = sample_resampling(cfg)
        else:
            raise ValueError("Unknown culture")

        rule_func = RULES[rule]
        out = rule_func(elec)
        welfare = welfare_summary(elec, out)
        risk = evaluate_risk(elec, rule_func)

        rows.append({
            "seed": s,
            "culture": culture,
            "rule": rule,
            "winners": out.winners,
            **welfare,
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


import os
def df_to_latex_table(df: pd.DataFrame, file: str, group_columns: bool = True) -> None:
    # Ensure parent directory exists
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

    if group_columns and "utilitarian" in df.columns:
        cols = list(df.columns)
        welfare_cols = [c for c in cols if c in ["utilitarian", "egalitarian", "nash"]]
        risk_cols = [c for c in cols if c in ["trials", "successes", "harms", "success\_rate", "harm\_rate"]]
        other_cols = [c for c in cols if c not in welfare_cols + risk_cols]

        group_line = (
            " & " * 3   # placeholders for culture, rule, seeds
            + f"\\multicolumn{{{len(welfare_cols)}}}{{c}}{{Welfare}} & "
            + f"\\multicolumn{{{len(risk_cols)}}}{{c}}{{Risk}} \\\\"
        )


        latex_lines = latex_str.splitlines()
        latex_lines.insert(3, group_line)
        latex_str = "\n".join(latex_lines)

    with open(file, "w") as f:
        f.write(latex_str)
    print(f"Saved LaTeX table to {file}")


def main():
    parser = argparse.ArgumentParser(description="Run free-riding experiments.")
    parser.add_argument("--culture", choices=CULTURES, help="single culture run")
    parser.add_argument("--rule", choices=list(RULES.keys()), help="rule to evaluate")
    parser.add_argument("--n_voters", type=int, default=10)
    parser.add_argument("--issues", type=int, default=3)
    parser.add_argument("--cands", type=int, default=3)
    parser.add_argument("--p", type=float, default=0.5)
    parser.add_argument("--phi", type=float, default=0.5)
    parser.add_argument("--groups", type=int, default=2)
    parser.add_argument("--seeds", type=int, default=1)
    parser.add_argument("--csv", type=str, default=None)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--latex", type=str, default=None)
    parser.add_argument("--batch", choices=["all"], help="run all cultures × rules")
    args = parser.parse_args()

    if args.batch == "all":
        all_summaries: List[pd.DataFrame] = []
        for culture in CULTURES:
            for rule in RULES.keys():
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
        cands = [args.cands] * args.issues
        if args.culture == "p_ic":
            cfg = PICConfig(n_voters=args.n_voters, candidates_per_issue=cands, p=args.p, seed=args.seeds)
            elec = sample_p_ic(cfg)
        elif args.culture == "disjoint":
            cfg = DisjointConfig(n_voters=args.n_voters, candidates_per_issue=cands, n_groups=args.groups, p=args.p, seed=args.seeds)
            elec = sample_disjoint(cfg)
        elif args.culture == "resampling":
            cfg = ResamplingConfig(n_voters=args.n_voters, candidates_per_issue=cands, p=args.p, phi=args.phi, seed=args.seeds)
            elec = sample_resampling(cfg)
        else:
            raise ValueError("Unknown culture")

        rule_func = RULES[args.rule]
        results = run_single_experiment(elec, {args.rule: rule_func})
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

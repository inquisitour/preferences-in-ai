# File: experiments/plot_results.py
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_welfare(df: pd.DataFrame, out_file: str):
    """Generate per-culture welfare comparison plots."""
    metrics = ["utilitarian", "egalitarian", "nash"]

    for culture in df["culture"].unique():
        subset = df[df["culture"] == culture]
        df_melted = subset.melt(
            id_vars=["rule"], value_vars=metrics,
            var_name="metric", value_name="value"
        )
        pivot = df_melted.pivot(index="rule", columns="metric", values="value")

        fig, ax = plt.subplots(figsize=(8, 5))
        pivot.plot(kind="bar", ax=ax, alpha=0.8, width=0.8)

        ax.set_title(f"Welfare comparison – {culture}")
        ax.set_ylabel("Score")
        ax.set_xlabel("Rule")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        plt.savefig(out_file.replace(".pdf", f"_{culture}.pdf"))
        plt.close(fig)


def plot_risk(df: pd.DataFrame, out_file: str):
    """Generate per-culture risk comparison plots."""
    metrics = ["success_rate", "harm_rate"]

    for culture in df["culture"].unique():
        subset = df[df["culture"] == culture]
        df_melted = subset.melt(
            id_vars=["rule"], value_vars=metrics,
            var_name="metric", value_name="value"
        )
        pivot = df_melted.pivot(index="rule", columns="metric", values="value")

        fig, ax = plt.subplots(figsize=(8, 5))
        pivot.plot(kind="bar", ax=ax, alpha=0.8, width=0.8)

        ax.set_title(f"Risk comparison – {culture}")
        ax.set_ylabel("Rate")
        ax.set_xlabel("Rule")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        plt.savefig(out_file.replace(".pdf", f"_{culture}.pdf"))
        plt.close(fig)


if __name__ == "__main__":
    df = pd.read_csv("results/combined.csv")

    plot_welfare(df, "report/figures/welfare_comparison.pdf")
    plot_risk(df, "report/figures/risk_comparison.pdf")

    print("Plots saved to report/figures/")

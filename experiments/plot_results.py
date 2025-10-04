# File: experiments/plot_results.py
import os
import pandas as pd
import matplotlib.pyplot as plt


def add_risk_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add 'risk' column if missing (harms/successes)."""
    if "risk" not in df.columns and "successes" in df.columns and "harms" in df.columns:
        df = df.copy()
        df["risk"] = df.apply(
            lambda row: row["harms"] / row["successes"] if row["successes"] > 0 else 0.0,
            axis=1,
        )
    return df


def extract_family_and_param(rule: str):
    """Extract family ('thiele' or 'owa') and parameter value (int)."""
    if rule.startswith("thiele_x"):
        return "thiele", int(rule.split("x")[1])
    if rule.startswith("owa_x"):
        return "owa", int(rule.split("x")[1])
    return rule, None


def plot_risk_by_family(df: pd.DataFrame, out_dir: str):
    """
    Generate risk plots per culture × family.
    Metrics: success_rate, harm_rate, risk.
    """
    df = add_risk_column(df)
    metrics = ["success_rate", "harm_rate", "risk"]

    os.makedirs(out_dir, exist_ok=True)

    # --- Plot per culture and rule family ---
    for culture in df["culture"].unique():
        subset_culture = df[df["culture"] == culture]

        for family in ["thiele", "owa"]:
            subset_family = []
            for _, row in subset_culture.iterrows():
                fam, param = extract_family_and_param(row["rule"])
                if fam == family:
                    new_row = row.copy()
                    new_row["param"] = param
                    subset_family.append(new_row)

            if not subset_family:
                continue

            fam_df = pd.DataFrame(subset_family).sort_values("param")
            fig, ax = plt.subplots(figsize=(8, 5))

            for metric, style, color in zip(metrics, ["-", "--", "-."], ["tab:blue", "tab:orange", "tab:green"]):
                ax.plot(
                    fam_df["param"],
                    fam_df[metric],
                    style,
                    marker="o",
                    label=metric.replace("_", " ").title(),
                    color=color,
                )

            ax.set_title(f"Manipulation Risk – {culture} ({family})")
            ax.set_xlabel("Parameter x")
            ax.set_ylabel("Rate")
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()

            out_file = os.path.join(out_dir, f"risk_{culture}_{family}.pdf")
            plt.savefig(out_file)
            plt.close(fig)
            print(f"Saved {out_file}")

    print("\n✅ All culture-family risk plots saved.")


def plot_risk_overview(df: pd.DataFrame, out_dir: str):
    """
    Generate a single overview plot comparing risk across all cultures.
    """
    df = add_risk_column(df)
    os.makedirs(out_dir, exist_ok=True)

    overview = (
        df.groupby(["culture", "rule"], as_index=False)
        .agg({"success_rate": "mean", "harm_rate": "mean", "risk": "mean"})
    )

    fig, ax = plt.subplots(figsize=(9, 6))
    for culture in df["culture"].unique():
        subset = overview[overview["culture"] == culture]
        ax.scatter(
            subset["success_rate"], subset["harm_rate"],
            s=60, alpha=0.7, label=culture
        )

    ax.set_title("Manipulation Success vs Harm Rates (Overview)")
    ax.set_xlabel("Success Rate")
    ax.set_ylabel("Harm Rate")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()

    out_file = os.path.join(out_dir, "risk_overview.pdf")
    plt.savefig(out_file)
    plt.close(fig)
    print(f"Saved {out_file}")


if __name__ == "__main__":
    df = pd.read_csv("results/combined.csv")
    plot_risk_by_family(df, "report/figures")
    plot_risk_overview(df, "report/figures")
    print("\nAll risk plots saved to report/figures/")

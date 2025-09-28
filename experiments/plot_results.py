# File: experiments/plot_results.py
import os
import pandas as pd
import matplotlib.pyplot as plt


def add_risk_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add 'risk' column if missing (harms/successes).
    """
    if "risk" not in df.columns and "successes" in df.columns and "harms" in df.columns:
        df = df.copy()
        df["risk"] = df.apply(
            lambda row: row["harms"] / row["successes"] if row["successes"] > 0 else 0.0,
            axis=1,
        )
    return df


def extract_family_and_param(rule: str):
    """
    Extract family ('thiele' or 'owa') and parameter value (int).
    Returns (family, param) or (None, None) for utilitarian/leximin.
    """
    if rule.startswith("thiele_x"):
        return "thiele", int(rule.split("x")[1])
    if rule.startswith("owa_x"):
        return "owa", int(rule.split("x")[1])
    return None, None


def plot_risk_by_family(df: pd.DataFrame, out_dir: str):
    """
    Generate risk plots per culture × family.
    Metrics: success_rate, harm_rate, risk.
    """
    df = add_risk_column(df)
    metrics = ["success_rate", "harm_rate", "risk"]

    os.makedirs(out_dir, exist_ok=True)

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

            fam_df = pd.DataFrame(subset_family)

            df_melted = fam_df.melt(
                id_vars=["param"], value_vars=metrics,
                var_name="metric", value_name="value"
            )
            pivot = df_melted.pivot(index="param", columns="metric", values="value")

            fig, ax = plt.subplots(figsize=(8, 5))
            pivot.plot(kind="bar", ax=ax, alpha=0.85, width=0.8)

            ax.set_title(f"Manipulation Risk – {culture} ({family})")
            ax.set_ylabel("Rate")
            ax.set_xlabel("Parameter x")
            plt.xticks(rotation=0)
            plt.tight_layout()

            out_file = os.path.join(out_dir, f"risk_{culture}_{family}.pdf")
            plt.savefig(out_file)
            plt.close(fig)
            print(f"Saved {out_file}")


if __name__ == "__main__":
    df = pd.read_csv("results/combined.csv")
    plot_risk_by_family(df, "report/figures")
    print("All risk plots saved to report/figures/")

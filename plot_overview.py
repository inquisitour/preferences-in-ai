import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load results
df = pd.read_csv("results/combined.csv")

# Ensure output folder exists
os.makedirs("figures", exist_ok=True)

# --- Welfare Comparison ---
welfare_metrics = ["utilitarian", "egalitarian", "nash"]
rules = df["rule"].unique()
cultures = df["culture"].unique()

x = np.arange(len(cultures))  # positions for cultures
width = 0.15  # bar width

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

for i, metric in enumerate(welfare_metrics):
    ax = axes[i]
    for j, rule in enumerate(rules):
        vals = [
            df[(df["culture"] == culture) & (df["rule"] == rule)][metric].mean()
            for culture in cultures
        ]
        ax.bar(x + j * width, vals, width, label=rule)
    ax.set_title(f"{metric.capitalize()} Welfare")
    ax.set_xticks(x + width * (len(rules) - 1) / 2)
    ax.set_xticklabels(cultures, rotation=30)
    ax.set_ylabel("Average score")
    if i == 2:
        ax.legend()

plt.tight_layout()
plt.savefig("figures/welfare_comparison_all.pdf")
plt.close()

# --- Risk Comparison ---
risk_metrics = ["success_rate", "harm_rate"]

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=False)

for i, metric in enumerate(risk_metrics):
    ax = axes[i]
    for j, rule in enumerate(rules):
        vals = [
            df[(df["culture"] == culture) & (df["rule"] == rule)][metric].mean()
            for culture in cultures
        ]
        ax.bar(x + j * width, vals, width, label=rule)
    ax.set_title(metric.replace("_", " ").capitalize())
    ax.set_xticks(x + width * (len(rules) - 1) / 2)
    ax.set_xticklabels(cultures, rotation=30)
    ax.set_ylabel("Rate")
    if i == 1:
        ax.legend()

plt.tight_layout()
plt.savefig("figures/risk_comparison_all.pdf")
plt.close()

print("✅ Bar chart figures saved in 'figures/'")

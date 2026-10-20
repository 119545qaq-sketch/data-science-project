"""Recreate two charts from the explicitly simulated commute dataset."""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "commute_modes.csv"
FIGURES = ROOT
COLORS = {
    "Shared transport": "#137d83",
    "Active travel": "#c77b1e",
    "Private transport": "#75849a",
}


def load_data():
    with DATA.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["share_percent"] = float(row["share_percent"])
        row["mean_minutes"] = float(row["mean_minutes"])
    if abs(sum(row["share_percent"] for row in rows) - 100) > 1e-9:
        raise ValueError("Mode shares must sum to 100%")
    return sorted(rows, key=lambda row: row["share_percent"], reverse=True)


def save_comparison(rows):
    labels = [row["mode"] for row in rows]
    y = list(range(len(rows)))
    colors = [COLORS[row["category"]] for row in rows]
    fig, (ax_share, ax_time) = plt.subplots(
        1, 2, figsize=(12, 5), sharey=True, gridspec_kw={"width_ratios": [1, 1]}
    )
    fig.suptitle("How might 1,000 students commute?", fontsize=17, weight="bold")
    fig.text(0.5, 0.91, "Illustrative Macau campus scenario · SIMULATED DATA", ha="center", color="#58677a")

    ax_share.barh(y, [row["share_percent"] for row in rows], color=colors, height=0.58)
    ax_share.set_yticks(y, labels)
    ax_share.invert_yaxis()
    ax_share.set_xlim(0, 39)
    ax_share.set_xlabel("Share of hypothetical commuters (%)")
    ax_share.set_title("Mode share")
    for pos, row in zip(y, rows):
        ax_share.text(row["share_percent"] + 0.7, pos, f'{row["share_percent"]:.0f}%', va="center")

    for pos, row, color in zip(y, rows, colors):
        ax_time.plot([0, row["mean_minutes"]], [pos, pos], color=color, linewidth=3)
        ax_time.scatter(row["mean_minutes"], pos, color=color, s=65, zorder=3)
        ax_time.text(row["mean_minutes"] + 0.7, pos, f'{row["mean_minutes"]:.0f} min', va="center")
    ax_time.set_xlim(0, 35)
    ax_time.set_xlabel("Assumed mean one-way minutes")
    ax_time.set_title("Travel time")
    for ax in (ax_share, ax_time):
        ax.grid(axis="x", color="#e5eaf0")
        ax.set_axisbelow(True)
        ax.spines[["top", "right", "left"]].set_visible(False)
    fig.subplots_adjust(left=0.22, right=0.96, top=0.82, bottom=0.18, wspace=0.12)
    fig.text(0.5, 0.045, "All values are invented for a visualization exercise; they are not survey findings.", ha="center", fontsize=9, color="#58677a")
    fig.savefig(FIGURES / "mode_share_and_time.png", dpi=180)
    plt.close(fig)


def save_tradeoff(rows):
    fig, ax = plt.subplots(figsize=(9, 6))
    fig.suptitle("Common choices can have longer assumed trips", fontsize=17, weight="bold")
    ax.set_title("Illustrative Macau campus scenario · SIMULATED DATA", color="#58677a")
    for row in rows:
        color = COLORS[row["category"]]
        ax.scatter(row["mean_minutes"], row["share_percent"], s=150, color=color)
        ax.annotate(row["mode"], (row["mean_minutes"], row["share_percent"]), xytext=(6, 5), textcoords="offset points", fontsize=9)
    ax.set_xlim(0, 34)
    ax.set_ylim(0, 38)
    ax.set_xlabel("Assumed mean one-way minutes")
    ax.set_ylabel("Share of hypothetical commuters (%)")
    ax.grid(color="#e5eaf0")
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.5, 0.02, "Each point is one travel mode. The relationship is descriptive only; it is not causal evidence.", ha="center", fontsize=9, color="#58677a")
    fig.tight_layout(rect=(0, 0.04, 1, 0.92))
    fig.savefig(FIGURES / "share_vs_time.png", dpi=180)
    plt.close(fig)


def main():
    FIGURES.mkdir(exist_ok=True)
    rows = load_data()
    shared = [row for row in rows if row["category"] == "Shared transport"]
    share = sum(row["share_percent"] for row in shared)
    weighted_time = sum(row["share_percent"] * row["mean_minutes"] for row in shared) / share
    print(f"Bus + campus shuttle: {share:.0f}% of hypothetical commuters; {weighted_time:.1f} mean minutes")
    save_comparison(rows)
    save_tradeoff(rows)


if __name__ == "__main__":
    main()

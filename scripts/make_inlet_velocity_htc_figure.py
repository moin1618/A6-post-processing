"""Generate inlet velocity versus heat transfer coefficients figure.

Run from the project root:
    python3 scripts/make_inlet_velocity_htc_figure.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator, MaxNLocator


DATA_FILE = Path("data_files/htc_experimental/full_experimental_cases.csv")
OUTPUT_DIR = Path("figures")
OUTPUT_FILE = OUTPUT_DIR / "inlet_velocity_heat_transfer_coefficients.png"

SERIES = [
    {
        "column": "hc (W/m2K)",
        "label": "Convective, hc",
        "color": "#0072B2",
        "marker": "o",
        "linestyle": "-",
    },
    {
        "column": "hr (W/m2K)",
        "label": "Radiative, hr",
        "color": "#D55E00",
        "marker": "s",
        "linestyle": "--",
    },
    {
        "column": "ht (W/m2K)",
        "label": "Total, ht",
        "color": "#009E73",
        "marker": "^",
        "linestyle": "-.",
    },
]

TEXT_COLOR = "#111111"
AXIS_COLOR = "#222222"
GRID_COLOR = "#E5E7EB"


def load_data() -> tuple[np.ndarray, dict[str, np.ndarray]]:
    with DATA_FILE.open(newline="") as data_handle:
        rows = list(csv.DictReader(data_handle))

    velocity = np.array([float(row["Va (m/s)"]) for row in rows])
    sort_order = np.argsort(velocity)
    values = {
        series["column"]: np.array([float(row[series["column"]]) for row in rows])[sort_order]
        for series in SERIES
    }
    return velocity[sort_order], values


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    velocity, values = load_data()

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.weight": "regular",
            "axes.labelweight": "regular",
            "axes.linewidth": 0.9,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "axes.labelsize": 11,
            "legend.fontsize": 10,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    figure, axis = plt.subplots(figsize=(6.4, 4.25), constrained_layout=True)
    figure.patch.set_facecolor("white")
    axis.set_facecolor("white")

    for series in SERIES:
        coefficient = values[series["column"]]
        axis.plot(
            velocity,
            coefficient,
            color=series["color"],
            linestyle=series["linestyle"],
            linewidth=2.0,
            marker=series["marker"],
            markersize=6.0,
            markerfacecolor="white",
            markeredgecolor=series["color"],
            markeredgewidth=1.6,
            label=series["label"],
            zorder=3,
        )

    last_velocity = float(velocity[-1])
    label_offsets = {
        "hc (W/m2K)": 0.0,
        "hr (W/m2K)": -0.18,
        "ht (W/m2K)": 0.2,
    }
    for series in SERIES:
        column = series["column"]
        axis.annotate(
            series["label"],
            xy=(last_velocity, values[column][-1]),
            xytext=(9, label_offsets[column]),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=10,
            color=series["color"],
        )

    all_values = np.concatenate([values[series["column"]] for series in SERIES])
    x_range = float(np.max(velocity) - np.min(velocity))
    y_range = float(np.max(all_values) - np.min(all_values))
    axis.set_xlim(float(np.min(velocity)) - 0.08 * x_range, float(np.max(velocity)) + 0.36 * x_range)
    axis.set_ylim(max(0, float(np.min(all_values)) - 0.14 * y_range), float(np.max(all_values)) + 0.16 * y_range)

    axis.set_xlabel("Inlet velocity, Va (m/s)")
    axis.set_ylabel("Heat transfer coefficient (W/m² K)")
    axis.set_xticks([0, 2.5, 5, 7.5, 10, 12.5])
    axis.set_xticklabels(["0", "2.5", "5", "7.5", "10", "12.5"])
    axis.set_xticks([0.25, 0.5, 1], minor=True)
    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_minor_locator(AutoMinorLocator(2))
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.7)

    axis.legend(
        loc="upper left",
        frameon=False,
        handlelength=2.4,
        borderaxespad=0.4,
        labelspacing=0.45,
    )

    axis.tick_params(axis="both", which="major", direction="in", length=4.5, width=0.8, top=True, right=True, color=AXIS_COLOR)
    axis.tick_params(axis="both", which="minor", direction="in", length=2.5, width=0.6, top=True, right=True, color=AXIS_COLOR)
    for spine in axis.spines.values():
        spine.set_color(AXIS_COLOR)
        spine.set_linewidth(0.9)

    figure.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
"""Generate the grid-independence study figure.

Run from the project root:
    python3 scripts/make_grid_independence_figure.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator, MaxNLocator, NullFormatter


DATA_FILE = Path("data_files/grid_independence/grid_independence_study.csv")
OUTPUT_DIR = Path("figures")
OUTPUT_FILE = OUTPUT_DIR / "grid_independence_study.png"

SELECTED_MESH_INDEX = -2

PANEL_SPECS = [
    {
        "column": "Convective heat flux (W/m^2)",
        "ylabel": "Convective heat flux (W/m²)",
        "color": "#0072B2",
        "marker": "o",
        "linestyle": "-",
        "panel": "a",
    },
    {
        "column": "Radiative heat flux (W/m^2)",
        "ylabel": "Radiative heat flux (W/m²)",
        "color": "#D55E00",
        "marker": "s",
        "linestyle": "--",
        "panel": "b",
    },
    {
        "column": "Temperature (degC)",
        "ylabel": "Temperature (°C)",
        "color": "#009E73",
        "marker": "^",
        "linestyle": "-.",
        "panel": "c",
    },
]


def load_grid_data() -> dict[str, np.ndarray]:
    with DATA_FILE.open(newline="") as data_handle:
        rows = list(csv.DictReader(data_handle))

    elements = np.array([float(row["Number of elements"]) for row in rows])
    sort_order = np.argsort(elements)

    data = {"Number of elements": elements[sort_order]}
    for spec in PANEL_SPECS:
        values = np.array([float(row[spec["column"]]) for row in rows])
        data[spec["column"]] = values[sort_order]
    return data


def padded_limits(values: np.ndarray, lower_padding: float = 0.12, upper_padding: float = 0.18) -> tuple[float, float]:
    value_min = float(np.min(values))
    value_max = float(np.max(values))
    value_range = value_max - value_min
    if value_range == 0:
        value_range = abs(value_max) * 0.1 or 1.0
    return value_min - lower_padding * value_range, value_max + upper_padding * value_range


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = load_grid_data()
    elements = data["Number of elements"]
    selected_mesh = elements[SELECTED_MESH_INDEX]

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.weight": "regular",
            "axes.labelweight": "regular",
            "axes.titleweight": "regular",
            "axes.linewidth": 0.8,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "axes.labelsize": 11,
            "legend.fontsize": 10,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    figure, axes = plt.subplots(3, 1, figsize=(7.2, 6.4), sharex=True, constrained_layout=True)
    figure.patch.set_facecolor("white")

    x_ticks = [5_000, 10_000, 30_000, 100_000]
    x_tick_labels = ["5", "10", "30", "100"]

    for axis, spec in zip(axes, PANEL_SPECS):
        values = data[spec["column"]]
        selected_value = values[SELECTED_MESH_INDEX]

        axis.set_facecolor("white")
        axis.set_xscale("log")
        axis.plot(
            elements,
            values,
            color=spec["color"],
            linestyle=spec["linestyle"],
            linewidth=1.8,
            marker=spec["marker"],
            markersize=5.2,
            markerfacecolor="white",
            markeredgecolor=spec["color"],
            markeredgewidth=1.4,
            zorder=3,
        )
        axis.scatter(
            [selected_mesh],
            [selected_value],
            marker="D",
            s=46,
            facecolor=spec["color"],
            edgecolor="black",
            linewidth=0.8,
            zorder=5,
        )
        axis.axvline(
            selected_mesh,
            color="#222222",
            linestyle=(0, (4, 3)),
            linewidth=1.0,
            zorder=2,
        )

        axis.set_ylabel(spec["ylabel"])
        axis.set_ylim(*padded_limits(values))
        axis.yaxis.set_major_locator(MaxNLocator(nbins=4, prune=None))
        axis.yaxis.set_minor_locator(AutoMinorLocator(2))
        axis.tick_params(axis="both", which="major", direction="in", length=4.5, width=0.8, top=True, right=True)
        axis.tick_params(axis="both", which="minor", direction="in", length=2.5, width=0.6, top=True, right=True)
        axis.text(
            -0.075,
            1.02,
            spec["panel"],
            transform=axis.transAxes,
            ha="left",
            va="bottom",
            fontsize=12,
            fontweight="bold",
            color="#111111",
        )

    axes[0].text(
        selected_mesh * 1.035,
        axes[0].get_ylim()[1] - 0.08 * (axes[0].get_ylim()[1] - axes[0].get_ylim()[0]),
        "selected mesh\n65,602",
        ha="left",
        va="top",
        fontsize=10,
        color="#111111",
        linespacing=1.1,
        bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "none", "alpha": 0.95},
    )

    axes[-1].set_xlim(4_200, 115_000)
    axes[-1].set_xticks(x_ticks)
    axes[-1].set_xticklabels(x_tick_labels)
    axes[-1].xaxis.set_minor_formatter(NullFormatter())
    axes[-1].set_xlabel("Number of elements, N (×10³; log scale)")

    figure.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
"""Generate simulation-parameter figure from sim-more para.csv.

Run from the project root:
    python3 scripts/make_sim_more_parameter_figure.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from PIL import Image


DATA_FILE = Path("data_files/study_extension_velocity/simulation_velocity_extension.csv")
OUTPUT_DIR = Path("figures")
OUTPUT_FILE = OUTPUT_DIR / "sim_more_parameter_study.png"

TEXT_COLOR = "#111111"
AXIS_COLOR = "#222222"
GRID_COLOR = "#E5E7EB"

PANEL_SPECS = [
    {
        "panel": "a",
        "ylabel": "Heat transfer coefficient (W/m² K)",
        "series": [
            {
                "column": "ht (W/m^2.K)",
                "label": "ht",
                "color": "#0072B2",
                "marker": "o",
                "linestyle": "-",
                "label_offset": 4,
            },
            {
                "column": "hc (W/m^2.K)",
                "label": "hc",
                "color": "#D55E00",
                "marker": "s",
                "linestyle": "--",
                "label_offset": -1,
            },
            {
                "column": "hr (W/m^2.K)",
                "label": "hr",
                "color": "#009E73",
                "marker": "^",
                "linestyle": "-.",
                "label_offset": -2,
            },
        ],
    },
    {
        "panel": "b",
        "ylabel": "Heat flux (W/m²)",
        "series": [
            {
                "column": "Total heat flux (W/m^2)",
                "label": "Total",
                "color": "#0072B2",
                "marker": "o",
                "linestyle": "-",
                "label_offset": 2,
            },
            {
                "column": "Convective heat flux (W/m^2)",
                "label": "Conv.",
                "color": "#D55E00",
                "marker": "s",
                "linestyle": "--",
                "label_offset": 0,
            },
            {
                "column": "Radiative heat flux (W/m^2)",
                "label": "Rad.",
                "color": "#009E73",
                "marker": "^",
                "linestyle": "-.",
                "label_offset": -4,
            },
        ],
    },
    {
        "panel": "c",
        "ylabel": "Temperature (°C)",
        "series": [
            {
                "column": "Ts (degC)",
                "label": "Ts",
                "color": "#0072B2",
                "marker": "o",
                "linestyle": "-",
                "label_offset": 3,
            },
            {
                "column": "Ta,mid (degC)",
                "label": "Ta,mid",
                "color": "#D55E00",
                "marker": "s",
                "linestyle": "--",
                "label_offset": 0,
            },
            {
                "column": "T_AUST (degC)",
                "label": "AUST",
                "color": "#009E73",
                "marker": "^",
                "linestyle": "-.",
                "label_offset": -4,
            },
        ],
    },
]


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_FILE)
    return data.sort_values("Va (m/s)").reset_index(drop=True)


def padded_limits(values: np.ndarray, lower_padding: float = 0.13, upper_padding: float = 0.22) -> tuple[float, float]:
    value_min = float(np.min(values))
    value_max = float(np.max(values))
    value_range = value_max - value_min
    if value_range == 0:
        value_range = abs(value_max) * 0.1 or 1.0
    return value_min - lower_padding * value_range, value_max + upper_padding * value_range


def style_axis(axis: plt.Axes) -> None:
    axis.set_facecolor("white")
    axis.tick_params(
        axis="both",
        which="major",
        direction="in",
        length=4.5,
        width=0.8,
        top=True,
        right=True,
        color=AXIS_COLOR,
    )
    axis.tick_params(
        axis="both",
        which="minor",
        direction="in",
        length=2.5,
        width=0.6,
        top=True,
        right=True,
        color=AXIS_COLOR,
    )
    for spine in axis.spines.values():
        spine.set_color(AXIS_COLOR)
        spine.set_linewidth(0.9)


def add_panel_label(axis: plt.Axes, label: str) -> None:
    axis.text(
        0.02,
        0.96,
        label,
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
        color=TEXT_COLOR,
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5},
    )



def plot_panel(axis: plt.Axes, data: pd.DataFrame, spec: dict[str, object]) -> None:
    velocity = data["Va (m/s)"].to_numpy(dtype=float)
    all_values = []

    for series in spec["series"]:
        values = data[series["column"]].to_numpy(dtype=float)
        all_values.append(values)
        axis.plot(
            velocity,
            values,
            color=series["color"],
            linestyle=series["linestyle"],
            linewidth=1.9,
            marker=series["marker"],
            markersize=5.0,
            markerfacecolor="white",
            markeredgecolor=series["color"],
            markeredgewidth=1.35,
            label=series["label"],
            zorder=3,
        )

    values_array = np.concatenate(all_values)
    x_range = float(np.max(velocity) - np.min(velocity))
    axis.set_xlim(float(np.min(velocity)) - 0.05 * x_range, float(np.max(velocity)) + 0.08 * x_range)
    axis.set_ylim(*padded_limits(values_array))
    axis.set_xlabel("Inlet velocity (m/s)")
    axis.set_ylabel(spec["ylabel"])
    axis.set_xticks([5, 7.5, 10, 12.5])
    axis.set_xticklabels(["5", "7.5", "10", "12.5"])
    axis.xaxis.set_minor_locator(AutoMinorLocator(2))
    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_minor_locator(AutoMinorLocator(2))
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.7)
    style_axis(axis)

    axis.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.045),
        ncol=3,
        frameon=False,
        handlelength=1.7,
        handletextpad=0.42,
        columnspacing=0.8,
        borderaxespad=0.0,
    )

    add_panel_label(axis, spec["panel"])


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = load_data()

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

    figure = plt.figure(figsize=(7.1, 5.45), constrained_layout=True)
    figure.set_constrained_layout_pads(w_pad=0.08, h_pad=0.08, wspace=0.08, hspace=0.2)
    figure.patch.set_facecolor("white")
    grid = figure.add_gridspec(2, 4, height_ratios=[1.0, 1.0])

    axes = [
        figure.add_subplot(grid[0, 0:2]),
        figure.add_subplot(grid[0, 2:4]),
        figure.add_subplot(grid[1, 1:3]),
    ]

    for axis, spec in zip(axes, PANEL_SPECS):
        plot_panel(axis, data, spec)

    figure.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(figure)

    with Image.open(OUTPUT_FILE) as image:
        image.convert("RGB").save(OUTPUT_FILE, dpi=(300, 300))
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
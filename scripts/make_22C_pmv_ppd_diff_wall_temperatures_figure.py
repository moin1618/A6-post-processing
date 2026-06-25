"""Generate a grouped bar chart for 22C inlet PMV/PPD wall-temperature data.

Run from the project root:
    python3 scripts/make_22C_pmv_ppd_diff_wall_temperatures_figure.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.ticker import AutoMinorLocator, FixedLocator, FormatStrFormatter
from PIL import Image


DATA_FILE = Path("data_files/22C_pmv_ppd_diff_wall_temperatures/average_pmv_ppd_wall_temp_22.csv")
OUTPUT_DIR = Path("figures")
OUTPUT_FILE = OUTPUT_DIR / "22C_pmv_ppd_diff_wall_temperatures.png"

TEXT_COLOR = "#111111"
AXIS_COLOR = "#222222"
GRID_COLOR = "#E5E7EB"
CATEGORY_STYLES = {
    "Class A": {"line": "#A7F3D0", "text": "#047857"},
    "Class B": {"line": "#FEF08A", "text": "#A16207"},
    "Class C": {"line": "#FECACA", "text": "#B91C1C"},
}
SITTING_COLOR = "#0072B2"
STANDING_COLOR = "#D55E00"

BAR_WIDTH = 0.34
POSTURES = [
    {
        "label": "Sitting",
        "pmv_column": "PMV_sitting",
        "ppd_column": "PPD_sitting (%)",
        "offset": -BAR_WIDTH / 2,
        "color": SITTING_COLOR,
        "hatch": "",
    },
    {
        "label": "Standing",
        "pmv_column": "PMV_standing",
        "ppd_column": "PPD_standing (%)",
        "offset": BAR_WIDTH / 2,
        "color": STANDING_COLOR,
        "hatch": "////",
    },
]

PMV_LIMITS = [(0.2, "Class A"), (0.5, "Class B"), (0.7, "Class C")]
PPD_LIMITS = [(6.0, "Class A"), (10.0, "Class B"), (15.0, "Class C")]


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_FILE)
    data = data.sort_values("T_wall (K)").reset_index(drop=True)
    data["Wall temperature (°C)"] = data["T_wall (K)"] - 273.15
    return data


def style_axis(axis: plt.Axes) -> None:
    axis.set_facecolor("white")
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.65, zorder=0)
    axis.tick_params(
        axis="both",
        which="major",
        direction="in",
        length=4.5,
        width=0.8,
        top=False,
        right=True,
        color=AXIS_COLOR,
        labelcolor=TEXT_COLOR,
    )
    axis.tick_params(
        axis="both",
        which="minor",
        direction="in",
        length=2.5,
        width=0.6,
        top=False,
        right=True,
        color=AXIS_COLOR,
    )
    for spine in axis.spines.values():
        spine.set_color(AXIS_COLOR)
        spine.set_linewidth(0.9)


def add_panel_label(axis: plt.Axes, label: str) -> None:
    axis.text(
        -0.085,
        1.03,
        label,
        transform=axis.transAxes,
        ha="left",
        va="bottom",
        fontsize=13,
        fontweight="bold",
        color=TEXT_COLOR,
        clip_on=False,
    )


def add_bars(axis: plt.Axes, data: pd.DataFrame, column_key: str) -> None:
    x_positions = np.arange(len(data))
    for posture in POSTURES:
        values = data[posture[column_key]].to_numpy(dtype=float)
        axis.bar(
            x_positions + posture["offset"],
            values,
            width=BAR_WIDTH,
            color=posture["color"],
            edgecolor=AXIS_COLOR,
            linewidth=0.65,
            hatch=posture["hatch"],
            zorder=3,
        )


def configure_axis(axis: plt.Axes, data: pd.DataFrame, ylabel: str, ylim: tuple[float, float]) -> None:
    x_positions = np.arange(len(data))
    axis.set_xlim(-0.58, len(data) - 0.42)
    axis.set_ylim(*ylim)
    axis.set_ylabel(ylabel)
    axis.set_xticks(x_positions)
    axis.set_xticklabels([f"{value:.0f}" for value in data["Wall temperature (°C)"]])
    axis.yaxis.set_minor_locator(AutoMinorLocator(2))
    style_axis(axis)


def add_limit_label(axis: plt.Axes, value: float, label: str) -> None:
    style = CATEGORY_STYLES[label]
    axis.text(
        1.012,
        value,
        label,
        transform=axis.get_yaxis_transform(),
        ha="left",
        va="center",
        fontsize=11,
        color=style["text"],
        clip_on=False,
    )


def add_pmv_limits(axis: plt.Axes) -> None:
    axis.axhline(0, color=AXIS_COLOR, linewidth=0.9, zorder=2)
    for value, label in PMV_LIMITS:
        style = CATEGORY_STYLES[label]
        axis.axhline(value, color=style["line"], linestyle=(0, (4.0, 2.3)), linewidth=1.35, zorder=2)
        axis.axhline(-value, color=style["line"], linestyle=(0, (4.0, 2.3)), linewidth=1.35, zorder=2)
        add_limit_label(axis, value, label)


def add_ppd_limits(axis: plt.Axes) -> None:
    for value, label in PPD_LIMITS:
        style = CATEGORY_STYLES[label]
        axis.axhline(value, color=style["line"], linestyle=(0, (4.0, 2.3)), linewidth=1.35, zorder=2)
        add_limit_label(axis, value, label)


def add_legend(axis: plt.Axes) -> None:
    handles = [
        Patch(facecolor=SITTING_COLOR, edgecolor=AXIS_COLOR, linewidth=0.65, label="Sitting"),
        Patch(facecolor=STANDING_COLOR, edgecolor=AXIS_COLOR, linewidth=0.65, hatch="////", label="Standing"),
    ]
    axis.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.16),
        ncol=2,
        frameon=False,
        fontsize=10.5,
        handlelength=1.8,
        columnspacing=1.2,
        handletextpad=0.45,
        borderaxespad=0,
    )


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
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "axes.labelsize": 12,
            "legend.fontsize": 10.5,
            "hatch.linewidth": 0.55,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    figure, axes = plt.subplots(2, 1, figsize=(7.4, 4.95), sharex=True)
    figure.subplots_adjust(left=0.105, right=0.84, top=0.88, bottom=0.12, hspace=0.10)
    figure.patch.set_facecolor("white")

    add_bars(axes[0], data, "pmv_column")
    configure_axis(axes[0], data, "PMV (unitless)", (-0.78, 0.78))
    axes[0].yaxis.set_major_locator(FixedLocator([-0.7, -0.5, -0.2, 0.0, 0.2, 0.5, 0.7]))
    axes[0].yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    axes[0].tick_params(labelbottom=False)
    add_pmv_limits(axes[0])
    add_panel_label(axes[0], "a")
    add_legend(axes[0])

    add_bars(axes[1], data, "ppd_column")
    configure_axis(axes[1], data, "PPD (%)", (0.0, 16.0))
    axes[1].set_xlabel("Wall temperature (°C)")
    axes[1].yaxis.set_major_locator(FixedLocator([0, 5, 10, 15]))
    add_ppd_limits(axes[1])
    add_panel_label(axes[1], "b")

    figure.savefig(OUTPUT_FILE, dpi=300, facecolor="white")
    plt.close(figure)

    with Image.open(OUTPUT_FILE) as image:
        image.convert("RGB").save(OUTPUT_FILE, dpi=(300, 300))
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
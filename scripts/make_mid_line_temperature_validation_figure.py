"""Generate mid-line temperature validation figure.

Run from the project root:
    python3 scripts/make_mid_line_temperature_validation_figure.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.ticker import AutoMinorLocator, FixedLocator
from PIL import Image


EXPERIMENT_FILE = Path("data_files/mid_line_temperature/centerline_temperature_experiment.csv")
SIMULATION_FILE = Path("data_files/mid_line_temperature/centerline _temperature_simulation.csv")
OUTPUT_DIR = Path("figures")
OUTPUT_FILE = OUTPUT_DIR / "mid_line_temperature_validation.png"

ROOM_WIDTH_M = 1.8
ROOM_HEIGHT_M = 2.7

TEXT_COLOR = "#111111"
AXIS_COLOR = "#222222"
GRID_COLOR = "#E5E7EB"
SIMULATION_COLOR = "#0072B2"
MEASUREMENT_COLOR = "#D55E00"
CENTERLINE_COLOR = "#6B7280"


def load_data() -> pd.DataFrame:
    experiment = pd.read_csv(EXPERIMENT_FILE)
    simulation = pd.read_csv(SIMULATION_FILE)
    data = experiment.merge(
        simulation,
        on=["height_m", "velocity_m_s"],
        suffixes=("_experiment", "_simulation"),
        validate="one_to_one",
    )
    data["error_degC"] = data["Ta_degC_simulation"] - data["Ta_degC_experiment"]
    return data.sort_values(["velocity_m_s", "height_m"]).reset_index(drop=True)


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
        labelcolor=TEXT_COLOR,
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


def add_panel_label(axis: plt.Axes, panel: str) -> None:
    axis.text(
        0.035,
        0.965,
        panel,
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
        color=TEXT_COLOR,
    )


def plot_room_axis(axis: plt.Axes, heights: np.ndarray) -> None:
    centerline_x = ROOM_WIDTH_M / 2.0
    axis.add_patch(
        Rectangle(
            (0, 0),
            ROOM_WIDTH_M,
            ROOM_HEIGHT_M,
            facecolor="white",
            edgecolor=AXIS_COLOR,
            linewidth=1.2,
            zorder=2,
        )
    )
    axis.plot(
        [centerline_x, centerline_x],
        [0, ROOM_HEIGHT_M],
        color=CENTERLINE_COLOR,
        linestyle=(0, (4, 3)),
        linewidth=1.2,
        zorder=3,
    )
    axis.scatter(
        np.full_like(heights, centerline_x),
        heights,
        s=34,
        marker="o",
        facecolor=MEASUREMENT_COLOR,
        edgecolor=TEXT_COLOR,
        linewidth=0.7,
        zorder=4,
    )
    axis.set_xlim(-0.06, ROOM_WIDTH_M + 0.06)
    axis.set_ylim(-0.04, ROOM_HEIGHT_M + 0.04)
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlabel("Width (m)")
    axis.set_ylabel("Height (m)")
    axis.xaxis.set_major_locator(FixedLocator([0.0, centerline_x, ROOM_WIDTH_M]))
    axis.set_xticklabels(["0", "0.9", "1.8"])
    axis.yaxis.set_major_locator(FixedLocator([0.0, 0.5, 1.0, 1.5, 2.0, ROOM_HEIGHT_M]))
    axis.set_yticklabels(["0", "0.5", "1.0", "1.5", "2.0", "2.7"])
    axis.xaxis.set_minor_locator(AutoMinorLocator(2))
    axis.yaxis.set_minor_locator(AutoMinorLocator(2))
    style_axis(axis)
    add_panel_label(axis, "a")


def plot_temperature_axis(axis: plt.Axes, data: pd.DataFrame, velocity: float) -> None:
    velocity_data = data[data["velocity_m_s"] == velocity].sort_values("height_m")
    heights = velocity_data["height_m"].to_numpy(dtype=float)
    experiment = velocity_data["Ta_degC_experiment"].to_numpy(dtype=float)
    simulation = velocity_data["Ta_degC_simulation"].to_numpy(dtype=float)
    mean_absolute_error = float(np.mean(np.abs(velocity_data["error_degC"].to_numpy(dtype=float))))

    axis.plot(
        experiment,
        heights,
        color=TEXT_COLOR,
        linestyle="-",
        linewidth=1.8,
        marker="o",
        markersize=5.6,
        markerfacecolor="white",
        markeredgecolor=TEXT_COLOR,
        markeredgewidth=1.2,
        zorder=4,
    )
    axis.plot(
        simulation,
        heights,
        color=SIMULATION_COLOR,
        linestyle="--",
        linewidth=1.8,
        marker="s",
        markersize=5.2,
        markerfacecolor=SIMULATION_COLOR,
        markeredgecolor=SIMULATION_COLOR,
        markeredgewidth=1.0,
        zorder=4,
    )

    axis.set_xlim(22.0, 29.0)
    axis.set_ylim(0.0, ROOM_HEIGHT_M)
    axis.set_xlabel("Air temperature (°C)")
    axis.set_ylabel("Height (m)")
    axis.xaxis.set_major_locator(FixedLocator([22.0, 24.0, 26.0, 28.0]))
    axis.yaxis.set_major_locator(FixedLocator([0.0, 0.5, 1.0, 1.5, 2.0, ROOM_HEIGHT_M]))
    axis.set_yticklabels(["0", "0.5", "1.0", "1.5", "2.0", "2.7"])
    axis.xaxis.set_minor_locator(AutoMinorLocator(3))
    axis.yaxis.set_minor_locator(AutoMinorLocator(2))
    axis.grid(axis="x", color=GRID_COLOR, linewidth=0.65, zorder=0)
    style_axis(axis)

    axis.text(
        0.055,
        0.065,
        f"{velocity:g} m/s\nMAE = {mean_absolute_error:.2f} °C",
        transform=axis.transAxes,
        ha="left",
        va="bottom",
        fontsize=10,
        color=TEXT_COLOR,
        linespacing=1.35,
    )
    axis.annotate(
        "Measured",
        xy=(float(experiment[-1]), float(heights[-1])),
        xytext=(6, -9),
        textcoords="offset points",
        ha="left",
        va="top",
        fontsize=10,
        color=TEXT_COLOR,
    )
    axis.annotate(
        "Simulation",
        xy=(float(simulation[-1]), float(heights[-1])),
        xytext=(6, 9),
        textcoords="offset points",
        ha="left",
        va="bottom",
        fontsize=10,
        color=SIMULATION_COLOR,
    )


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = load_data()
    heights = np.sort(data["height_m"].unique())
    velocities = sorted(data["velocity_m_s"].unique())

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

    figure = plt.figure(figsize=(7.4, 3.75), constrained_layout=True)
    figure.patch.set_facecolor("white")
    grid = figure.add_gridspec(1, 3, width_ratios=[0.82, 1.0, 1.0])

    room_axis = figure.add_subplot(grid[0, 0])
    first_profile_axis = figure.add_subplot(grid[0, 1])
    second_profile_axis = figure.add_subplot(grid[0, 2])

    plot_room_axis(room_axis, heights)
    for panel, axis, velocity in zip(["b", "c"], [first_profile_axis, second_profile_axis], velocities):
        plot_temperature_axis(axis, data, float(velocity))
        add_panel_label(axis, panel)

    figure.savefig(OUTPUT_FILE, dpi=300, facecolor="white")
    plt.close(figure)

    with Image.open(OUTPUT_FILE) as image:
        image.convert("RGB").save(OUTPUT_FILE, dpi=(300, 300))
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
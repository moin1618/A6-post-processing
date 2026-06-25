"""Generate heat-transfer coefficient validation figure.

Run from the project root:
    python3 scripts/make_heat_transfer_coefficient_validation_figure.py
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


DATA_FILE = Path("data_files/htc_experiment_simulation/heat transfer comparison_table.csv")
OUTPUT_DIR = Path("figures")
OUTPUT_FILE = OUTPUT_DIR / "heat_transfer_coefficient_validation.png"

TEXT_COLOR = "#111111"
AXIS_COLOR = "#222222"
GRID_COLOR = "#E5E7EB"
SIM_COLOR = "#0072B2"
BAR_COLOR = "#BDBDBD"

COEFFICIENTS = [
    {
        "name": "hc",
        "exp_column": "hc (W/m^2K) (Exp)",
        "sim_column": "hc (W/m^2K) (Sim)",
        "error_column": "hc % Error",
        "ylabel": "hc (W/m² K)",
        "panel": "a",
    },
    {
        "name": "hr",
        "exp_column": "hr (W/m^2K) (Exp)",
        "sim_column": "hr (W/m^2K) (Sim)",
        "error_column": "hr % Error",
        "ylabel": "hr (W/m² K)",
        "panel": "b",
    },
    {
        "name": "ht",
        "exp_column": "ht (W/m^2K) (Exp)",
        "sim_column": "ht (W/m^2K) (Sim)",
        "error_column": "ht % Error",
        "ylabel": "ht (W/m² K)",
        "panel": "c",
    },
]


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_FILE)
    return data.sort_values("Va (m/s)").reset_index(drop=True)


def padded_limits(values: np.ndarray, lower_padding: float = 0.16, upper_padding: float = 0.24) -> tuple[float, float]:
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


def add_panel_label(axis: plt.Axes, panel: str) -> None:
    axis.text(
        -0.14,
        1.06,
        panel,
        transform=axis.transAxes,
        ha="left",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color=TEXT_COLOR,
    )


def plot_coefficient(axis: plt.Axes, velocity: np.ndarray, experiment: np.ndarray, simulation: np.ndarray, ylabel: str) -> None:
    axis.plot(
        velocity,
        experiment,
        color=TEXT_COLOR,
        linestyle="-",
        linewidth=1.9,
        marker="o",
        markersize=5.8,
        markerfacecolor="white",
        markeredgecolor=TEXT_COLOR,
        markeredgewidth=1.3,
        zorder=3,
    )
    axis.plot(
        velocity,
        simulation,
        color=SIM_COLOR,
        linestyle="--",
        linewidth=1.9,
        marker="s",
        markersize=5.8,
        markerfacecolor=SIM_COLOR,
        markeredgecolor=SIM_COLOR,
        markeredgewidth=1.3,
        zorder=3,
    )

    all_values = np.concatenate([experiment, simulation])
    x_range = float(np.max(velocity) - np.min(velocity))
    axis.set_xlim(float(np.min(velocity)) - 0.08 * x_range, float(np.max(velocity)) + 0.48 * x_range)
    axis.set_ylim(0, float(np.max(all_values)) * 1.18)
    axis.set_xticks([5, 10, 12.5])
    axis.set_xticklabels(["5", "10", "12.5"])
    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_minor_locator(AutoMinorLocator(2))
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.7)
    axis.set_xlabel("Inlet velocity (m/s)")
    axis.set_ylabel(ylabel)
    style_axis(axis)

    y_span = axis.get_ylim()[1] - axis.get_ylim()[0]
    experiment_offset = -0.02 * y_span if experiment[-1] > simulation[-1] else 0.02 * y_span
    simulation_offset = 0.02 * y_span if experiment[-1] > simulation[-1] else -0.02 * y_span
    axis.annotate(
        "Experiment",
        xy=(float(velocity[-1]), float(experiment[-1])),
        xytext=(8, experiment_offset),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=10,
        color=TEXT_COLOR,
    )
    axis.annotate(
        "Simulation",
        xy=(float(velocity[-1]), float(simulation[-1])),
        xytext=(8, simulation_offset),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=10,
        color=SIM_COLOR,
    )


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = load_data()
    velocity = data["Va (m/s)"].to_numpy(dtype=float)

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

    figure = plt.figure(figsize=(7.4, 6.25), constrained_layout=True)
    figure.patch.set_facecolor("white")
    grid = figure.add_gridspec(2, 2, height_ratios=[1.0, 1.0])

    axes = [
        figure.add_subplot(grid[0, 0]),
        figure.add_subplot(grid[0, 1]),
        figure.add_subplot(grid[1, 0]),
    ]
    error_axis = figure.add_subplot(grid[1, 1])

    mean_absolute_errors: list[float] = []
    error_labels: list[str] = []
    for axis, spec in zip(axes, COEFFICIENTS):
        experiment = data[spec["exp_column"]].to_numpy(dtype=float)
        simulation = data[spec["sim_column"]].to_numpy(dtype=float)
        plot_coefficient(axis, velocity, experiment, simulation, spec["ylabel"])
        add_panel_label(axis, spec["panel"])
        mean_absolute_errors.append(float(np.mean(np.abs(data[spec["error_column"]].to_numpy(dtype=float)))))
        error_labels.append(spec["name"])

    y_positions = np.arange(len(error_labels))
    error_axis.barh(
        y_positions,
        mean_absolute_errors,
        height=0.62,
        color=BAR_COLOR,
        edgecolor=AXIS_COLOR,
        linewidth=0.8,
        zorder=3,
    )
    error_axis.set_yticks(y_positions)
    error_axis.set_yticklabels(error_labels)
    error_axis.invert_yaxis()
    error_axis.set_xlim(0, max(22.0, float(max(mean_absolute_errors)) * 1.28))
    error_axis.set_xlabel("Mean absolute percent error (%)")
    error_axis.set_ylabel("Coefficient")
    error_axis.xaxis.set_major_locator(MaxNLocator(nbins=5))
    error_axis.xaxis.set_minor_locator(AutoMinorLocator(2))
    error_axis.grid(axis="x", color=GRID_COLOR, linewidth=0.7)
    style_axis(error_axis)
    add_panel_label(error_axis, "d")

    label_offset = error_axis.get_xlim()[1] * 0.025
    for position, value in zip(y_positions, mean_absolute_errors):
        error_axis.text(
            value + label_offset,
            position,
            f"{value:.1f}%",
            ha="left",
            va="center",
            fontsize=10,
            color=TEXT_COLOR,
        )

    figure.savefig(OUTPUT_FILE, dpi=300, facecolor="white")
    plt.close(figure)

    with Image.open(OUTPUT_FILE) as image:
        image.convert("RGB").save(OUTPUT_FILE, dpi=(300, 300))
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
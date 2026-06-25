"""Generate predicted percentage dissatisfied (PPD) as a function of PMV.

Run from the project root:
    python3 scripts/make_ppd_figure.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path("figures")
OUTPUT_FILE = OUTPUT_DIR / "ppd_vs_pmv.png"


def predicted_percentage_dissatisfied(pmv: np.ndarray) -> np.ndarray:
    """Return PPD (%) from PMV using the standard PMV--PPD relation."""
    return 100 - 95 * np.exp(-0.03353 * pmv**4 - 0.2179 * pmv**2)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    pmv = np.linspace(-3, 3, 600)
    ppd = predicted_percentage_dissatisfied(pmv)
    comfort_min, comfort_max = -0.5, 0.5
    comfort_ppd = predicted_percentage_dissatisfied(np.array([comfort_min, comfort_max]))[0]

    figure, axes = plt.subplots(figsize=(7.4, 4.4), constrained_layout=True)
    axes.set_xlim(-3, 3)
    axes.set_ylim(0, 100)

    axes.axvspan(
        comfort_min,
        comfort_max,
        color="#1B7837",
        alpha=0.08,
        label="Recommended comfort band",
    )
    axes.plot(pmv, ppd, color="#1F4E79", linewidth=2.6)
    axes.hlines(
        comfort_ppd,
        comfort_min,
        comfort_max,
        color="#1B7837",
        linestyle="--",
        linewidth=1.2,
    )
    axes.vlines(
        [comfort_min, comfort_max],
        0,
        comfort_ppd,
        color="#1B7837",
        linestyle="--",
        linewidth=1.1,
    )

    axes.scatter([0], [5], color="#1F4E79", s=28, zorder=4)
    axes.annotate(
        "Minimum PPD = 5%\nat PMV = 0",
        xy=(0, 5),
        xytext=(-1.35, 18),
        arrowprops={"arrowstyle": "->", "color": "#444444", "linewidth": 0.9},
        fontsize=9.5,
        color="#333333",
    )
    axes.text(
        0,
        91,
        "Recommended comfort band\nPPD ≤ 10%",
        ha="center",
        va="center",
        fontsize=9.5,
        color="#1B7837",
        fontweight="bold",
    )

    axes.set_xlabel("Predicted mean vote (PMV)", fontsize=11)
    axes.set_ylabel("Predicted percentage dissatisfied, PPD (%)", fontsize=11)
    axes.set_xticks(np.arange(-3, 4, 1))
    axes.set_yticks(np.arange(0, 101, 20))
    axes.grid(axis="y", color="#DDDDDD", linewidth=0.8)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    axes.tick_params(labelsize=10)

    figure.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
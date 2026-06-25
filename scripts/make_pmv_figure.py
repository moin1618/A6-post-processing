"""Generate the PMV thermal sensation scale figure as a PNG.

Run from the project root:
    python3 scripts/make_pmv_figure.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


OUTPUT_DIR = Path("figures")
OUTPUT_FILE = OUTPUT_DIR / "pmv_comfort_band.png"


COLORS = {
    "cold": "#2166AC",
    "cool": "#67A9CF",
    "slightly_cool": "#D1E5F0",
    "neutral": "#F7F7F7",
    "slightly_warm": "#FDDBC7",
    "warm": "#EF8A62",
    "hot": "#B2182B",
    "comfort": "#1B7837",
}


SEGMENTS = [
    (-3.5, -2.5, "Cold", COLORS["cold"], "white"),
    (-2.5, -1.5, "Cool", COLORS["cool"], "white"),
    (-1.5, -0.5, "Slightly\ncool", COLORS["slightly_cool"], "#4A4A4A"),
    (-0.5, 0.5, "Neutral", COLORS["neutral"], "#4A4A4A"),
    (0.5, 1.5, "Slightly\nwarm", COLORS["slightly_warm"], "#4A4A4A"),
    (1.5, 2.5, "Warm", COLORS["warm"], "white"),
    (2.5, 3.5, "Hot", COLORS["hot"], "white"),
]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    figure, axes = plt.subplots(figsize=(9.4, 2.25), constrained_layout=True)
    axes.set_xlim(-3.85, 3.85)
    axes.set_ylim(-0.62, 1.35)
    axes.axis("off")

    for segment_min, segment_max, label, fill_color, text_color in SEGMENTS:
        segment_center = (segment_min + segment_max) / 2
        axes.add_patch(
            Rectangle(
                (segment_min, 0),
                segment_max - segment_min,
                0.68,
                facecolor=fill_color,
                edgecolor="white",
                linewidth=1.4,
            )
        )
        axes.text(
            segment_center,
            0.34,
            label,
            ha="center",
            va="center",
            color=text_color,
            fontsize=11,
            fontweight="bold",
        )

    axes.add_patch(
        Rectangle(
            (-3.5, 0),
            7,
            0.68,
            facecolor="none",
            edgecolor="#555555",
            linewidth=1.1,
        )
    )

    comfort_min, comfort_max = -0.5, 0.5
    axes.add_patch(
        Rectangle(
            (comfort_min, -0.04),
            comfort_max - comfort_min,
            0.76,
            facecolor=COLORS["comfort"],
            alpha=0.08,
            edgecolor=COLORS["comfort"],
            linewidth=2.0,
        )
    )
    axes.plot([0, 0], [0.76, 1.05], color=COLORS["comfort"], linewidth=1.8)
    axes.text(
        0,
        1.28,
        "Comfort band\n-0.5 to +0.5",
        ha="center",
        va="center",
        color=COLORS["comfort"],
        fontsize=13,
        fontweight="bold",
    )

    for tick_value in range(-3, 4):
        axes.plot([tick_value, tick_value], [-0.06, -0.18], color="#666666", linewidth=1.0)
        tick_label = f"{tick_value:+d}" if tick_value > 0 else str(tick_value)
        axes.text(
            tick_value,
            -0.4,
            tick_label,
            ha="center",
            va="center",
            color="#444444",
            fontsize=11,
        )

    figure.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
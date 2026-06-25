"""Generate the room schematic figure as a PNG.

Run from the project root:
    python3 scripts/make_room_schematic.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle


OUTPUT_DIR = Path("figures")

ROOM_EDGE = "#1F2937"
HEATED_WALL = "#EF4444"
HEATED_WALL_TEXT = "#B91C1C"
COOLED_CEILING = "#2563EB"
DIFFUSER_EDGE = "#64748B"
DIFFUSER_TEXT = "#334155"
CENTERLINE_GUIDE = "#94A3B8"
CENTERLINE_TEXT = "#475569"
FLOW_COLOR = "#0891B2"
CASE_LABEL_TEXT = "#1F2937"
CASE_LABEL_EDGE = "#CBD5E1"


def _box() -> dict[str, object]:
    return {"boxstyle": "round,pad=0.16", "fc": "white", "ec": "none", "alpha": 0.95}


def save_figure(fig: Figure, name: str, png_dpi: int = 300, pad_inches: float = 0.02) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    for extension in ("png", "pdf"):
        output_file = OUTPUT_DIR / f"{name}.{extension}"
        save_kwargs = {
            "bbox_inches": "tight",
            "pad_inches": pad_inches,
            "facecolor": "white",
        }
        if extension == "png":
            save_kwargs["dpi"] = png_dpi
        fig.savefig(output_file, **save_kwargs)
        print(f"Wrote {output_file}")
    plt.close(fig)


def plot_room_schematic() -> None:
    fig, ax = plt.subplots(figsize=(5.2, 6.9))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(-0.34, 2.02)
    ax.set_ylim(-0.24, 2.9)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 1.8, 2.7, fill=False, ec=ROOM_EDGE, lw=2.0))
    ax.add_patch(
        Rectangle(
            (0.0, 0.0),
            0.075,
            2.7,
            facecolor=(239 / 255, 68 / 255, 68 / 255, 0.08),
            ec=HEATED_WALL,
            lw=1.8,
            hatch="////",
        )
    )
    ax.add_patch(
        Rectangle(
            (0.0, 2.63),
            1.8,
            0.07,
            facecolor=(37 / 255, 99 / 255, 235 / 255, 0.06),
            ec=COOLED_CEILING,
            lw=1.8,
            hatch="...",
        )
    )

    ax.add_patch(Rectangle((1.77, 2.02), 0.08, 0.28, facecolor="white", ec=COOLED_CEILING, lw=1.7))
    ax.add_patch(Rectangle((0.03, 0.00), 0.18, 0.07, facecolor="white", ec=DIFFUSER_EDGE, lw=1.7))
    ax.plot([0.9, 0.9], [0.0, 2.7], linestyle="--", color=CENTERLINE_GUIDE, lw=1.0)

    arrow_style = {
        "arrowstyle": "->",
        "color": FLOW_COLOR,
        "lw": 1.8,
        "mutation_scale": 12,
        "shrinkA": 0,
        "shrinkB": 0,
    }
    ax.annotate("", xy=(0.40, 2.00), xytext=(0.40, 0.72), arrowprops=arrow_style)
    ax.annotate("", xy=(1.28, 2.00), xytext=(0.40, 2.00), arrowprops=arrow_style)
    ax.annotate("", xy=(1.48, 0.74), xytext=(1.48, 1.92), arrowprops=arrow_style)
    ax.annotate("", xy=(0.56, 0.74), xytext=(1.48, 0.74), arrowprops=arrow_style)

    ax.text(
        0.97,
        0.50,
        "Schematic\nairflow",
        fontsize=11.5,
        color=FLOW_COLOR,
        ha="center",
        va="center",
        bbox=dict(
            boxstyle="round,pad=0.25",
            fc="white",
            ec="#CBD5E1",
            lw=1.2,
        ),
    )

    ax.text(0.90, 2.52, "Cooled ceiling", ha="center", va="bottom", fontsize=12.5, color=COOLED_CEILING, bbox=_box())
    ax.text(1.50, 2.05, "Outlet", ha="center", va="center", fontsize=11.3, color=COOLED_CEILING, bbox=_box())
    ax.text(
        0.12,
        1.34,
        "Radiant\nheated wall",
        ha="center",
        va="center",
        rotation=90,
        fontsize=11.5,
        color=HEATED_WALL_TEXT,
        bbox={"boxstyle": "round,pad=0.12", "fc": "white", "ec": "none", "alpha": 0.95},
    )
    ax.text(1.00, 1.52, "Vertical\ncenterline", ha="center", va="center", fontsize=12.5, color=CENTERLINE_TEXT, bbox=_box())
    ax.text(
        -0.01,
        0.16,
        "Slot diffuser\n(baseboard level)",
        ha="left",
        va="bottom",
        fontsize=11.0,
        color=DIFFUSER_TEXT,
        bbox={"boxstyle": "round,pad=0.12", "fc": "white", "ec": "none", "alpha": 0.96},
    )

    ax.annotate(
        "",
        xy=(-0.20, 2.7),
        xytext=(-0.20, 0.0),
        arrowprops={"arrowstyle": "<->", "color": "black", "lw": 1.0, "mutation_scale": 10},
    )
    ax.text(-0.27, 1.35, "2.7 m", rotation=90, ha="center", va="center", fontsize=11.5, color="black")
    ax.annotate(
        "",
        xy=(1.8, -0.16),
        xytext=(0.0, -0.16),
        arrowprops={"arrowstyle": "<->", "color": "black", "lw": 1.0, "mutation_scale": 10},
    )
    ax.text(0.90, -0.25, "1.8 m", ha="center", va="top", fontsize=11.5, color="black")

    save_figure(fig, "room_schematic", png_dpi=240, pad_inches=0.02)


def main() -> None:
    plot_room_schematic()


if __name__ == "__main__":
    main()
"""Render the reported ablation results; run with python3 from any directory.

Values are transcribed unchanged from the original ablation table in
sections/experiments.tex. No aggregation or rescaling is performed.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np


OUTPUT = Path(__file__).resolve().parents[1] / "pic" / "ablation"
# Coral, teal, blue-violet and gold from the supplied palette.
COLORS = ["#f58e87", "#4ab4a6", "#8898c1", "#fec02f"]
HATCHES = ["//", ".", "xx", "\\\\"]
EDGE = "#666666"
FULL = ("Full", [0.7796, 0.7790, 0.8958, 0.2230])
GROUPS = {
    "pipeline_stages": [
        FULL,
        ("Permuting prior evidence", [0.3471, 0.3532, 0.2241, 0.8606]),
        ("Permuting coverage", [0.6649, 0.6605, 0.5996, 0.5702]),
        ("Zeroing decomposition representations", [0.6371, 0.6554, 0.7878, 0.4366]),
    ],
    "decomposition_design": [
        FULL,
        ("Collapsing semantic units", [0.6580, 0.6292, 0.8591, 0.4073]),
        ("Disabling slot competition", [0.6701, 0.6874, 0.7665, 0.3985]),
        ("Removing noisy-OR support", [0.6210, 0.5520, 0.6291, 0.6068]),
    ],
}


def draw(name, rows):
    fig, axes = plt.subplots(1, 4, figsize=(8.8, 2.7), sharey=True)
    fig.subplots_adjust(left=0.065, right=0.99, bottom=0.10, top=0.65, wspace=0.60)
    for metric, (ax, title) in enumerate(zip(
        axes, ["Accuracy ↑", "Macro-F1 ↑", "QWK ↑", "MAE ↓"]
    )):
        values = [row[1][metric] for row in rows]
        bars = ax.bar(np.arange(4), values, width=0.68, color=COLORS,
                      edgecolor=EDGE, linewidth=0.7, zorder=3)
        for idx, (bar, value) in enumerate(zip(bars, values)):
            bar.set_hatch(HATCHES[idx])
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.018,
                    f"{value:.4f}", ha="center", va="bottom", fontsize=6.5,
                    fontweight="bold" if idx == 0 else "normal")
        ax.set_ylim(0, 1.02)
        ax.set_xlim(-0.65, 3.65)
        ax.set_yticks(np.arange(0, 1.01, 0.2))
        ax.set_xticks([])
        ax.set_title(title, loc="left", pad=7, fontsize=10, fontweight="bold")
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#D8D8D8", linewidth=0.7, zorder=0)
        ax.tick_params(axis="y", length=2.5, width=0.6, color="#999999",
                       labelsize=8, pad=4, labelleft=True)
        for spine in ax.spines.values():
            spine.set_color("#B0B0B0")
            spine.set_linewidth(0.7)
    # Matplotlib fills legends column-first: reorder to match the bars row-first.
    order = [0, 2, 1, 3]
    handles = [Patch(facecolor=COLORS[i], edgecolor=EDGE, linewidth=0.7,
                     hatch=HATCHES[i], label=rows[i][0]) for i in order]
    legend = fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.51, 1.0),
                        ncol=2, frameon=True, fancybox=False, edgecolor="#DDDDDD",
                        fontsize=9, handlelength=1.8,
                        handleheight=1, columnspacing=2.2, labelspacing=0.65)
    legend.get_texts()[0].set_fontweight("bold")
    for extension in ("pdf", "png"):
        fig.savefig(OUTPUT / f"{name}.{extension}", dpi=300, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42,
                         "hatch.linewidth": 0.6})
    for name, rows in GROUPS.items():
        draw(name, rows)

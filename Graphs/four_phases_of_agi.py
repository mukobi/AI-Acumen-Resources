"""
I believe the development of AGI is best thought of in 4 separate phases:
- Below-human artificial general intelligence (BAGI): Below human level, like current systems
- Human-level artificial general intelligence (HAGI): At human level, like HLMI from AI Impacts. What most non-technical people might imagine the ceiling being.
- Moderately-superhuman artificial general intelligence (MAGI): Clearly smarter than humans, can do some tricky shit including unexpected loss of control, but not gigabrained (prob no sudden diamondoid bacteria)
- Superintelligent artificial general intelligence (SAGI): Yudkowsky fears no man. But that thing...

This is a graph illustrating this transition with:
- Made up capabilities progress line that looks like a steps of random heights at random intervals (but overall like a y=x line).
- Bands of configurable width in the background indicating each phase that blend with each other with a gradient at the boundaries.
"""

from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import numpy as np

import chart_utils


def main() -> None:
    chart_utils.initialize_plot_no_markers()

    # Define the AGI development phases
    phases = [
        "Below-\nHuman",
        "Human-\nLevel",
        "Moderately-\nSuperhuman",
        "Super-\nintelligent",
    ]
    colors = ["blue", "green", "yellow", "red"]  # Colors for each phase
    phase_widths = [
        2,
        1,
        3,
        2,
    ]  # Configurable widths for each phase, adjust as needed

    n_steps = 22  # Number of steps in the capability progress line

    plt.figure(figsize=chart_utils.FIGSIZE_DEFAULT)

    # Generate a capabilities progress line
    np.random.seed(42)  # For reproducibility
    x = np.linspace(0, sum(phase_widths), n_steps)
    y = np.cumsum(np.random.rand(n_steps) * 0.2)  # Random heights at random intervals

    # Draw the background bands for each phase
    start = 0
    for i, (color, width) in enumerate(zip(colors, phase_widths)):
        plt.fill_betweenx([0, max(y)], start, start + width, color=color, alpha=0.3)
        start += width
        # Write the label in the graph
        ypos = max(y) / 2
        if i == 1:
            ypos = max(y) / 3 * 2
        elif i == 2:
            ypos = max(y) / 3
        plt.text(
            start - width / 2,
            ypos,
            phases[i],
            ha="center",
            va="center",
            fontsize=chart_utils.LABELSIZE_DEFAULT,
            color="black",
            fontweight="bold",
        )

    # Plot the capabilities progress line
    plt.step(
        x, y, where="post", linewidth=3, color="#444", label="Capabilities\nAdvancement"
    )

    # Customize the plot
    # plt.legend(loc="upper left")
    plt.title("Four Phases of AGI")
    plt.xlabel("Time")
    plt.ylabel("General Capabilities")
    plt.xlim([0, max(x)])
    plt.ylim([0, max(y)])
    plt.xticks([])
    plt.yticks([])

    chart_utils.save_plot("four_phases_of_agi.png")


if __name__ == "__main__":
    main()

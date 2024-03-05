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
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

import chart_utils


def main() -> None:
    chart_utils.initialize_plot_no_markers()

    # Define the AGI development phases and configurations
    phase_names = [
        "Below\nHuman",
        "Human\nLevel",
        "Moderately\nSuperhuman",
        "Super-\nIntelligent",
    ]
    # https://coolors.co/aeb5ea-aaeebd-fbda74-fbacc0
    phase_colors = ["#AEB5EA", "#AAEEBD", "#FBDA74", "#FBACC0"]
    # https://coolors.co/0c1027-082b13-332500-280b0c
    text_colors = ["#0C1027", "#082B13", "#332500", "#280B0C"]
    phase_widths = [2.25, 1.25, 2.5, 2.25]
    phase_label_heights = [0.325, 0.425, 0.47, 0.55]
    phase_label_x_offsets = [0, -0.1, 0, 0]
    solid_fraction = 0.75  # Fraction of each band that should be solid color

    plt.figure(figsize=chart_utils.FIGSIZE_DEFAULT)

    # Generate capabilities progress line
    np.random.seed(65)
    n_steps = 20
    # x = np.linspace(0, sum(phase_widths), n_steps)
    # Make x randomly spaced too
    x = np.cumsum(np.random.rand(n_steps))
    x = x / max(x) * sum(phase_widths)
    # y = np.cumsum(np.random.rand(n_steps) * 0.2)
    # y is random increases at each
    y = np.cumsum(np.random.rand(n_steps) * 0.2)

    # Create a modified colormap for gradient and solid bands
    total_width = sum(phase_widths)
    n_colors = 16  # Number of colors in the gradient
    colors_repeated = []
    for color, width in zip(phase_colors, phase_widths):
        n_solid = int(np.round(n_colors * (width / total_width) * solid_fraction))
        n_gradient = int(n_colors * (width / total_width)) - n_solid
        colors_repeated.extend([color] * n_solid)
        if n_gradient > 0:  # Ensure there's a gradient part
            colors_repeated.append(color)
    modified_cmap = LinearSegmentedColormap.from_list(
        "Modified_AGIPhases", colors_repeated
    )

    # Display the colormap as a background
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    extent = [0, total_width, 0, max(y)]
    plt.imshow(gradient, aspect="auto", cmap=modified_cmap, extent=extent)

    # Draw labels over the bands
    start = 0
    for i, (width, phase) in enumerate(zip(phase_widths, phase_names)):
        xpos = start + width / 2 + phase_label_x_offsets[i]
        ypos = max(y) * phase_label_heights[i]
        plt.text(
            xpos,
            ypos,
            phase,
            ha="center",
            va="center",
            fontsize=chart_utils.LABELSIZE_DEFAULT,
            color=text_colors[i],
            fontweight="bold",
        )
        start += width

    # Plot the capabilities progress line
    plt.step(x, y, where="post", linewidth=3, color="#444", label="Mock Data")

    # Customize the plot
    plt.title("Four Phases of AGI")
    plt.xlabel(r"Time and Investment $\rightarrow$")
    plt.ylabel(r"General Capabilities $\rightarrow$")
    plt.xlim([min(x), max(x)])
    plt.ylim([min(y), max(y)])
    plt.xticks([])
    plt.yticks([])
    # Black border
    plt.gca().spines[:].set_color("black")

    # Add mock data disclaimer as legend
    plt.legend(
        loc="upper left",
        fontsize=chart_utils.LABELSIZE_DEFAULT * 0.66,
        # facecolor="white",
        labelspacing=0.2,
        # borderpad=0.2,
        framealpha=0.66,
        handlelength=1,
    )

    # Add logo overlay
    img_path = "./Resources/ai_acumen_wide.png"
    image = plt.imread(img_path)
    zoom_level = 0.03
    image_center_x = max(x) - 1.475
    image_center_y = 0.1625
    oi = OffsetImage(image, zoom=zoom_level)
    ab = AnnotationBbox(oi, (image_center_x, image_center_y), frameon=False)
    ax = plt.gca()
    ax.add_artist(ab)

    chart_utils.save_plot("four_phases_of_agi.png")


if __name__ == "__main__":
    main()

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
    # https://coolors.co/aeb5ea-aaeebd-fbda74-fbadaf
    phase_colors = ["#AEB5EA", "#AAEEBD", "#FBDA74", "#FBADAF"]
    # https://coolors.co/0c1027-082b13-332500-280b0c
    text_colors = ["#0C1027", "#082B13", "#332500", "#280B0C"]
    phase_widths = [2, 1, 3, 2]
    solid_fraction = 0.75  # Fraction of each band that should be solid color

    plt.figure(figsize=chart_utils.FIGSIZE_DEFAULT)

    # Generate capabilities progress line
    np.random.seed(66)
    n_steps = 20
    x = np.linspace(0, sum(phase_widths), n_steps)
    # Make x randomly spaced too
    # x = np.cumsum(np.random.rand(n_steps))
    # x = x / max(x) * sum(phase_widths)
    y = np.cumsum(np.random.rand(n_steps) * 0.2)
    # y is random increases at each
    # y = np.cumsum(np.random.rand(n_steps) * 0.2)

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
        ypos = max(y) * 0.4
        if i == 1:
            ypos = max(y) * 0.55
        elif i == 2:
            ypos = max(y) * 0.4
        elif i == 3:
            ypos = max(y) * 0.65
        plt.text(
            start + width / 2,
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
    plt.step(
        x, y, where="post", linewidth=3, color="#333", label="Capabilities\nAdvancement"
    )

    # Customize the plot
    plt.title("Four Phases of AGI (Illustrative Data)")
    plt.xlabel(r"Time and Investment $\rightarrow$")
    plt.ylabel(r"General Capabilities $\rightarrow$")
    plt.xlim([0, max(x)])
    plt.ylim([0, max(y)])
    plt.xticks([])
    plt.yticks([])

    # # Overlay logo
    # img_path = "./Resources/ai_acumen_wide.png"
    # image = plt.imread(img_path)
    # image_ar = image.shape[1] / image.shape[0]
    # axes_ar = max(x) / max(y)
    # fig_ar = chart_utils.FIGSIZE_DEFAULT[0] / chart_utils.FIGSIZE_DEFAULT[1]
    # width = 2.25
    # height = width / image_ar / axes_ar * fig_ar
    # right, bottom = max(x) - 0.05, 0.04
    # left, top = right - width, bottom + height
    # plt.imshow(image, aspect="auto", extent=[left, right, bottom, top], zorder=10)
    # # plt.imshow(image, aspect="auto", extent=None, zorder=10)

    # Load the image
    img_path = "./Resources/ai_acumen_wide.png"
    image = plt.imread(img_path)

    # Create an OffsetImage
    # zoom determines the scale of the image; adjust as needed
    zoom_level = 0.03  # Adjust this based on your needs
    image_center_x = max(x) - 1.5
    image_center_y = 0.15
    oi = OffsetImage(image, zoom=zoom_level)
    ab = AnnotationBbox(oi, (image_center_x, image_center_y), frameon=False)

    # Add the AnnotationBbox to the current Axes
    ax = plt.gca()
    ax.add_artist(ab)

    chart_utils.save_plot("four_phases_of_agi.png")


if __name__ == "__main__":
    main()

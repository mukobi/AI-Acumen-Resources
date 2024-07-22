"""
Conceptual cycle of the timing of the 3 major ML conferences.
"""

from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

import chart_utils

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    """Main execution function."""
    chart_utils.initialize_plot_no_markers()

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={"projection": "polar"})

    # Calculate angles for each month (12 months)
    angles = np.linspace(0, 2 * np.pi, 12, endpoint=False).tolist()
    # Add another range with 2pi added to each element
    angles += [angle + 2 * np.pi for angle in angles]

    def get_angle(month_index: float) -> float:
        # If int in range, return the angle
        if month_index % 1 == 0:
            assert 0 <= month_index <= 24
            return angles[int(month_index)]
        # If float, interpolate the angle
        else:
            lower = int(month_index)
            upper = lower + 1
            return np.interp(
                month_index, [lower, upper], [angles[lower], angles[upper]]
            )

    # Define angles for submission and conference dates based on corrected months
    # December, April/May, July
    angles_conf = [get_angle(i) for i in [0, 4.5, 7]]
    # May, September/October, January/February
    angles_sub = [get_angle(i) for i in [5, 9.5, 13.5]]

    # Conference names, submission dates, and conference dates
    conferences = ["NeurIPS", "ICLR", "ICML"]
    # sub_dates = ["May", "Sept/Oct", "Jan/Feb"]
    # conf_dates = ["Dec", "Apr/May", "Jul"]

    # Define colors for each conference
    colors = ["#916CA3", "#2CA02C", "#1F77B4"]

    # # Plot the arrows
    # for i in range(len(conferences)):
    #     ax.annotate(
    #         "",
    #         xy=(angles_conf[i], 1),
    #         xytext=(angles_sub[i], 1),
    #         arrowprops=dict(arrowstyle="->", color=colors[i], lw=2),
    #     )

    # Plot arc curves for each conference
    curve_radii = [0.9, 0.8, 0.7]
    for i in range(len(conferences))[::-1]:
        start = angles_conf[i]
        end = angles_sub[i]
        radius = curve_radii[i]
        # Plot a line for each using many subdivisions to turn it into a curve
        num_subdivisions = 500
        for j in range(num_subdivisions):
            start_angle = start + (end - start) * (j / num_subdivisions)
            end_angle = start + (end - start) * ((j + 1) / num_subdivisions)
            ax.plot(
                [start_angle, end_angle],
                [radius, radius],
                color=colors[i],
                linewidth=10,
                alpha=0.8,
            )
        # Plot a larger circle at the deadline
        ax.plot(
            [end, end + 0.01],
            [radius, radius],
            color=colors[i],
            linewidth=20,
            alpha=1.0,
        )

    # Add text annotations for submission and conference dates
    text_radii = [0.55, 0.5, 0.45]
    for i, conf in enumerate(conferences):
        mid_angle = (angles_sub[i] + angles_conf[i]) / 2
        radius = text_radii[i]
        ax.text(
            mid_angle,
            radius,
            conf,
            horizontalalignment="center",
            verticalalignment="center",
            size=16,
            weight="bold",
            color=colors[i],
        )
        # ax.text(
        #     angles_sub[i],
        #     0.95,
        #     sub_date,
        #     horizontalalignment="center",
        #     verticalalignment="center",
        #     size=12,
        #     color=colors[i],
        # )
        # ax.text(
        #     angles_conf[i],
        #     0.95,
        #     conf_date,
        #     horizontalalignment="center",
        #     verticalalignment="center",
        #     size=12,
        #     color=colors[i],
        # )

    # Set the theta direction and offset
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)

    # Hide the radial labels and grid
    ax.set_yticklabels([])
    ax.grid(False)

    # Set y scale
    ax.set_ylim(0, 1)

    # Set the x-ticks and labels
    tick_months = list(range(12))
    months = [
        "Dec",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
    ]
    ax.set_xticks([angles[i] for i in tick_months])
    ax.set_xticklabels(months, size=12)
    plt.tight_layout()

    chart_utils.save_plot("ml_conference_cycle_no_title.png")

    plt.title("ML Conference Submission Cycle", size=20, pad=30, y=1.075)
    # Add subtitle explaining what the arcs are
    plt.text(
        0.5,
        1.135,
        "Arcs go from conference date to next submission deadline",
        horizontalalignment="center",
        verticalalignment="center",
        size=11,
        transform=ax.transAxes,
    )

    chart_utils.save_plot("ml_conference_cycle.png")


if __name__ == "__main__":
    main()

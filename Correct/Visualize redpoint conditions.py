from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Initial blue point
initial_blue = [0.5, 0.25]

# Function to update the plot based on the blue point position
def update_plot(blue_x, blue_y):
    # Set the blue point
    blue = [Fraction(blue_x), Fraction(blue_y)]

    # Create a grid of red points to evaluate feasibility
    x = np.linspace(-1, 2, 400)
    y = np.linspace(-1, 2, 400)
    X, Y = np.meshgrid(x, y)

    # Calculate midpoint and perpendicular slope for each red point
    mid_x = (X + float(blue[0])) / 2
    mid_y = (Y + float(blue[1])) / 2

    slope = (Y - float(blue[1])) / (X - float(blue[0]))
    with np.errstate(divide='ignore', invalid='ignore'):
        perp_slope = -1 / slope

    # Calculate the intercept of the perpendicular bisector
    intercept = mid_y - perp_slope * mid_x

    # Determine if the perpendicular bisector intersects the x-axis between values of 0 and 1
    intersect = -intercept / perp_slope  # x-intercept when y = 0
    feasible_region = (intersect >= 0) & (intersect <= 1)

    # Calculate the centers of the circles where red points are feasible
    center_x_1 = 0
    center_y_1 = 0
    center_x_2 = 1
    center_y_2 = 0

    # Define the unit square polygon
    unit_square = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])

    # Calculate the area of the circles inside the unit square
    radius_1 = np.sqrt((blue_x - center_x_1) ** 2 + (blue_y - center_y_1) ** 2)
    radius_2 = np.sqrt((blue_x - center_x_2) ** 2 + (blue_y - center_y_2) ** 2)

    circle_1 = Point(center_x_1, center_y_1).buffer(radius_1)
    circle_2 = Point(center_x_2, center_y_2).buffer(radius_2)

    intersection = circle_1.intersection(circle_2)
    circle_1_area = circle_1.intersection(unit_square).area
    circle_2_area = circle_2.intersection(unit_square).area
    overlap_area = intersection.intersection(unit_square).area

    volume_1 = circle_1_area
    volume_2 = circle_2_area
    overlap_volume = overlap_area

    total_volume = max(volume_1 - overlap_volume, 0) + max(volume_2 - overlap_volume, 0)

    # Clear the plot
    ax.clear()

    # Plot the initial boundaries of the map
    boundary_points = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    ax.plot(boundary_points[:, 0], boundary_points[:, 1], 'k-', linewidth=1, label='Initial Boundary')

    # Plot the blue point
    ax.plot(blue[0], blue[1], 'bo', label='Blue Point')

    # Plot the centers of the circles
    ax.plot(center_x_1, center_y_1, 'rx', label='Circle Center 1')
    ax.plot(center_x_2, center_y_2, 'gx', label='Circle Center 2')

    # Plot heatmap of feasible region
    ax.imshow(feasible_region, extent=[-1, 2, -1, 2], origin='lower', cmap='viridis', alpha=0.5)

    # Set plot limits
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)

    # Add labels and legend
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Feasible Region for Red Points (Heatmap)')
    ax.legend()

    # Display volume information
    volume_text = (f"Volume of Sphere 1 (inside unit square): {volume_1:.3f}\n"
                f"Volume of Sphere 2 (inside unit square): {volume_2:.3f}\n"
                f"Overlap Volume (inside unit square): {overlap_volume:.3f}\n"
                f"Total Volume (inside unit square): {total_volume:.3f}\n\n"
                f"Equation of Sphere 1: (x - {center_x_1})^2 + (y - {center_y_1})^2 = {radius_1:.3f}^2\n"
                f"Equation of Sphere 2: (x - {center_x_2})^2 + (y - {center_y_2})^2 = {radius_2:.3f}^2\n")
    ax.text(1.05, 0.5, volume_text, transform=ax.transAxes, fontsize=10, verticalalignment='center', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5))

    # Redraw the plot
    fig.canvas.draw_idle()

# Create the plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)

# Initial plot
update_plot(initial_blue[0], initial_blue[1])

# Add sliders for blue point position
ax_blue_x = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_blue_y = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')

slider_blue_x = Slider(ax_blue_x, 'Blue X', -1.0, 2.0, valinit=initial_blue[0])
slider_blue_y = Slider(ax_blue_y, 'Blue Y', -1.0, 2.0, valinit=initial_blue[1])

# Update the plot when the slider value changes
def update(val):
    blue_x = slider_blue_x.val
    blue_y = slider_blue_y.val
    update_plot(blue_x, blue_y)

slider_blue_x.on_changed(update)
slider_blue_y.on_changed(update)

# Show plot
plt.show()

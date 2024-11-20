from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Initial blue point
initial_blue = [0.5, 0.25]

# Function to update the plot based on the blue point position
def update_plot(blue_x, blue_y):
    # Set the blue point
    blue = [Fraction(blue_x), Fraction(blue_y)]

    # Create a grid of red points to evaluate feasibility
    x = np.linspace(-1, 2, 600)
    y = np.linspace(-1, 2, 600)
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
    boundary_points = np.array([[0, 0], [1, 0], [0.5, 0.5], [0, 0]])
    ax.plot(boundary_points[:, 0], boundary_points[:, 1], 'k-', linewidth=1, label='Triangle Boundary')

    # Plot the blue point
    ax.plot(blue[0], blue[1], 'bo', label='Blue Point')

    # Plot the centers of the circles
    ax.plot(center_x_1, center_y_1, 'rx', label='Circle Center 1')
    ax.plot(center_x_2, center_y_2, 'gx', label='Circle Center 2')

    # Plot heatmap of feasible region
    ax.imshow(feasible_region, extent=[-1, 2, -1, 2], origin='lower', cmap='viridis', alpha=0.5)  # The current colormap is set to 'viridis'. Some other options you can use are 'plasma', 'inferno', 'magma', 'cividis', 'hot', 'cool', 'spring', 'summer', 'autumn', 'winter', and 'jet'. You can change the 'cmap' parameter to one of these to achieve different visual effects.

    # Set plot limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Add labels and legend
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Feasible Region for Red Points (Heatmap)')
    ax.legend(loc='best', fontsize='medium', frameon=True)

    # Display volume information
    volume_text = (f"Volume of Sphere 1 (inside unit square): {volume_1:.6f}\n"
                f"Volume of Sphere 2 (inside unit square): {volume_2:.6f}\n"
                f"Overlap Volume (inside unit square): {overlap_volume:.6f}\n"
                f"Total Volume (inside unit square): {total_volume:.6f}\n\n"
                f"Equation of Sphere 1: (x - {center_x_1})^2 + (y - {center_y_1})^2 = {radius_1**2:.6f}\n"
                f"Equation of Sphere 2: (x - {center_x_2})^2 + (y - {center_y_2})^2 = {radius_2**2:.6f}\n")
    ax.text(1.05, 0.5, volume_text, transform=ax.transAxes, fontsize=12, verticalalignment='center', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5))

    # Redraw the plot
    fig.canvas.draw_idle()

# Create the plot
fig, ax = plt.subplots(figsize=(12, 11))
plt.subplots_adjust(left=-.27, bottom=0.3)

# Initial plot
update_plot(initial_blue[0], initial_blue[1])

# Define a function for a DVD-like bounce within the triangle
class DVD_Bounce:
    def __init__(self, initial_position, velocity, triangle_vertices):
        self.position = np.array(initial_position, dtype='float')
        self.velocity = np.array(velocity, dtype='float') + np.random.uniform(-0.001, 0.001, size=2)
        self.triangle = Polygon(triangle_vertices)
        self.edges = [
            (triangle_vertices[i], triangle_vertices[(i + 1) % len(triangle_vertices)])
            for i in range(len(triangle_vertices))
        ]

    def step(self):
        # Update position
        self.position += self.velocity
        point = Point(self.position)

        # Check for collisions with triangle boundaries and bounce
        if not self.triangle.contains(point):
            for edge in self.edges:
                p1, p2 = edge
                edge_vector = np.array(p2) - np.array(p1)
                edge_normal = np.array([-edge_vector[1], edge_vector[0]])
                edge_normal = edge_normal / np.linalg.norm(edge_normal)

                p1_to_pos = self.position - np.array(p1)
                dist_to_edge = np.dot(p1_to_pos, edge_normal)

                if dist_to_edge <= 0:
                    self.velocity -= 2 * np.dot(self.velocity, edge_normal) * edge_normal
                    break
            # Add a small random perturbation to prevent loops
            self.velocity += np.random.uniform(-0.000002, 0.000002, size=2)
        return self.position

# Initialize DVD bounce within the triangle
triangle_vertices = [(0, 0), (1, 0), (0.5, 0.5)]  # Vertices of the triangle
initial_position = [0.5, 0.25]
initial_velocity = [0.01, 0.015]
dvd_bounce = DVD_Bounce(initial_position, initial_velocity, triangle_vertices)


# Update function for animation
def animate(i):
    position = dvd_bounce.step()
    update_plot(position[0], position[1])

# Create the animation
ani = FuncAnimation(fig, animate, frames=800, interval=50, repeat=True)

# Show plot
plt.show()

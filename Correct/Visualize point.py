from fractions import Fraction
import random
import matplotlib.pyplot as plt

# Set denominator for fractions
N = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000  # You can adjust N to control the granularity of the fractions

# Randomly generate two points (blue and red) within [0, 1] x [0, 1]
blue = [Fraction(random.randint(0, N), N), Fraction(random.randint(0, N), N)]
red = [Fraction(random.randint(0, N), N), Fraction(random.randint(0, N), N)]

# Determine which boundary (x = 0, y = 0, x = 1, y = 1) blue is closest to
boundaries = {
    'x = 0': blue[0],
    'y = 0': blue[1],
    'x = 1': Fraction(1, 1) - blue[0],
    'y = 1': Fraction(1, 1) - blue[1]
}
closest_boundary = min(boundaries, key=boundaries.get)

# Calculate midpoint of blue and red
mid_point = [(blue[0] + red[0]) / 2, (blue[1] + red[1]) / 2]

# Calculate the slope of the line connecting blue and red
if red[0] != blue[0]:
    slope = (red[1] - blue[1]) / (red[0] - blue[0])
else:
    slope = None  # Vertical line

# Calculate the slope of the perpendicular bisector
if slope is not None:
    if slope == 0:
        perp_slope = None  # Perpendicular to horizontal line is vertical
    else:
        perp_slope = -1 / slope
else:
    perp_slope = Fraction(0, 1)  # Perpendicular to vertical line is horizontal

# Output the equation of the perpendicular bisector
if perp_slope is None:
    bisector_x = mid_point[0]
    bisector_eq = f"x = {bisector_x}"
elif perp_slope == 0:
    bisector_y = mid_point[1]
    bisector_eq = f"y = {bisector_y}"
else:
    intercept = mid_point[1] - perp_slope * mid_point[0]
    bisector_eq = f"y = {perp_slope}x + {intercept}"

# Check if the perpendicular bisector intersects the closest boundary to blue
intersection = False

if closest_boundary == 'x = 0':
    if perp_slope is None:
        # Vertical line x = bisector_x
        intersection = bisector_x == 0
    elif perp_slope == 0:
        # Horizontal line y = bisector_y intersects x = 0 if y is within [0, 1]
        intersection = (0 <= bisector_y <= 1)
    else:
        y_at_x0 = intercept  # Since x = 0
        intersection = (0 <= y_at_x0 <= 1)
elif closest_boundary == 'x = 1':
    if perp_slope is None:
        intersection = bisector_x == 1
    elif perp_slope == 0:
        intersection = (0 <= bisector_y <= 1)
    else:
        y_at_x1 = perp_slope * 1 + intercept
        intersection = (0 <= y_at_x1 <= 1)
elif closest_boundary == 'y = 0':
    if perp_slope == 0:
        intersection = bisector_y == 0
    elif perp_slope is None:
        intersection = (0 <= bisector_x <= 1)
    else:
        x_at_y0 = -intercept / perp_slope
        intersection = (0 <= x_at_y0 <= 1)
elif closest_boundary == 'y = 1':
    if perp_slope == 0:
        intersection = bisector_y == 1
    elif perp_slope is None:
        intersection = (0 <= bisector_x <= 1)
    else:
        x_at_y1 = (1 - intercept) / perp_slope
        intersection = (0 <= x_at_y1 <= 1)

# Output the results
print(f"Blue Point: {blue}")
print(f"Red Point: {red}")
print(f"Closest Boundary to Blue: {closest_boundary}")
print(f"Midpoint: {mid_point}")
print(f"Perpendicular Bisector Equation: {bisector_eq}")
print(f"Does the Perpendicular Bisector Intersect the Closest Boundary? {intersection}")

# Plotting
# Convert fractions to floats for plotting
blue_float = [float(blue[0]), float(blue[1])]
red_float = [float(red[0]), float(red[1])]
mid_point_float = [float(mid_point[0]), float(mid_point[1])]

fig, ax = plt.subplots()

# Plot blue and red points
ax.plot(blue_float[0], blue_float[1], 'bo', label='Blue Point')
ax.plot(red_float[0], red_float[1], 'ro', label='Red Point')

# Plot line connecting blue and red
ax.plot([blue_float[0], red_float[0]], [blue_float[1], red_float[1]], 'k-', label='Line Between Blue and Red')

# Plot midpoint
ax.plot(mid_point_float[0], mid_point_float[1], 'go', label='Midpoint')

# Plot perpendicular bisector
if perp_slope is None:
    # Vertical line within y = [0, 1]
    bisector_x_float = float(bisector_x)
    ax.plot([bisector_x_float, bisector_x_float], [0, 1], 'purple', linestyle='--', label='Perpendicular Bisector')
elif perp_slope == 0:
    # Horizontal line within x = [0, 1]
    bisector_y_float = float(bisector_y)
    ax.plot([0, 1], [bisector_y_float, bisector_y_float], 'purple', linestyle='--', label='Perpendicular Bisector')
else:
    # Line within the square boundaries
    x_vals = []
    y_vals = []
    # Intersect with x = 0
    y_at_x0 = intercept
    if 0 <= y_at_x0 <= 1:
        x_vals.append(0)
        y_vals.append(float(y_at_x0))
    # Intersect with x = 1
    y_at_x1 = perp_slope * 1 + intercept
    if 0 <= y_at_x1 <= 1:
        x_vals.append(1)
        y_vals.append(float(y_at_x1))
    # Intersect with y = 0
    if perp_slope != 0:
        x_at_y0 = -intercept / perp_slope
        if 0 <= x_at_y0 <= 1:
            x_vals.append(float(x_at_y0))
            y_vals.append(0)
    # Intersect with y = 1
    x_at_y1 = (1 - intercept) / perp_slope
    if 0 <= x_at_y1 <= 1:
        x_vals.append(float(x_at_y1))
        y_vals.append(1)
    # Plot the line segment within the square
    if len(x_vals) >= 2:
        ax.plot(x_vals, y_vals, 'purple', linestyle='--', label='Perpendicular Bisector')

# Highlight the closest boundary
if closest_boundary == 'x = 0':
    ax.axvline(x=0, color='orange', linestyle='-', linewidth=2, label='Closest Boundary (x = 0)')
elif closest_boundary == 'y = 0':
    ax.axhline(y=0, color='orange', linestyle='-', linewidth=2, label='Closest Boundary (y = 0)')
elif closest_boundary == 'x = 1':
    ax.axvline(x=1, color='orange', linestyle='-', linewidth=2, label='Closest Boundary (x = 1)')
elif closest_boundary == 'y = 1':
    ax.axhline(y=1, color='orange', linestyle='-', linewidth=2, label='Closest Boundary (y = 1)')

# Set plot limits
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Add labels and legend
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Blue and Red Points with Midpoint and Perpendicular Bisector')
ax.legend()

# Show plot
plt.show()
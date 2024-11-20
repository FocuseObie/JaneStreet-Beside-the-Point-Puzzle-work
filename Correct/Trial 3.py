import numpy as np
import time

# Number of points to simulate
num_points = 100_000_000
num_iterations = 720  # Number of iterations for averaging

# Initialize accumulators for probability and runtime
total_probability = 0
total_runtime = 0

for i in range(num_iterations):
    # Start the timer
    start_time = time.time()

    # Randomly generate two sets of points (blue and red) within [0, 1] x [0, 1]
    blue = np.random.rand(num_points, 2)
    red = np.random.rand(num_points, 2)

    # Determine which boundary (x = 0, y = 0, x = 1, y = 1) blue is closest to
    boundaries = np.stack([
        blue[:, 0],           # Distance to x = 0
        blue[:, 1],           # Distance to y = 0
        1 - blue[:, 0],       # Distance to x = 1
        1 - blue[:, 1]        # Distance to y = 1
    ], axis=1)
    closest_boundary_indices = np.argmin(boundaries, axis=1)

    # Calculate midpoint of blue and red
    mid_point = (blue + red) / 2

    # Calculate the slope of the line connecting blue and red
    delta_x = red[:, 0] - blue[:, 0]
    delta_y = red[:, 1] - blue[:, 1]
    slope = np.where(delta_x != 0, delta_y / delta_x, np.nan)

    # Calculate the slope of the perpendicular bisector
    perp_slope = np.where(np.isnan(slope), 0, np.where(slope == 0, np.nan, -1 / slope))

    # Initialize an array to store the intersection results
    intersection = np.zeros(num_points, dtype=bool)

    # Process each boundary separately using vectorized operations

    # Boundary x = 0
    idx0 = closest_boundary_indices == 0
    perp_slope0 = perp_slope[idx0]
    mid_point0 = mid_point[idx0]

    # y at x = 0
    y_at_x0 = mid_point0[:, 1] - perp_slope0 * mid_point0[:, 0]
    condition0 = np.where(
        np.isnan(perp_slope0),
        mid_point0[:, 0] == 0,
        np.where(
            perp_slope0 == 0,
            (0 <= mid_point0[:, 1]) & (mid_point0[:, 1] <= 1),
            (0 <= y_at_x0) & (y_at_x0 <= 1)
        )
    )
    intersection[idx0] = condition0

    # Boundary y = 0
    idx1 = closest_boundary_indices == 1
    perp_slope1 = perp_slope[idx1]
    mid_point1 = mid_point[idx1]

    # x at y = 0
    x_at_y0 = mid_point1[:, 0] - mid_point1[:, 1] / perp_slope1
    condition1 = np.where(
        perp_slope1 == 0,
        mid_point1[:, 1] == 0,
        np.where(
            np.isnan(perp_slope1),
            (0 <= mid_point1[:, 0]) & (mid_point1[:, 0] <= 1),
            (0 <= x_at_y0) & (x_at_y0 <= 1)
        )
    )
    intersection[idx1] = condition1

    # Boundary x = 1
    idx2 = closest_boundary_indices == 2
    perp_slope2 = perp_slope[idx2]
    mid_point2 = mid_point[idx2]

    # y at x = 1
    y_at_x1 = perp_slope2 * (1 - mid_point2[:, 0]) + mid_point2[:, 1]
    condition2 = np.where(
        np.isnan(perp_slope2),
        mid_point2[:, 0] == 1,
        np.where(
            perp_slope2 == 0,
            (0 <= mid_point2[:, 1]) & (mid_point2[:, 1] <= 1),
            (0 <= y_at_x1) & (y_at_x1 <= 1)
        )
    )
    intersection[idx2] = condition2

    # Boundary y = 1
    idx3 = closest_boundary_indices == 3
    perp_slope3 = perp_slope[idx3]
    mid_point3 = mid_point[idx3]

    # x at y = 1
    x_at_y1 = mid_point3[:, 0] + (1 - mid_point3[:, 1]) / perp_slope3
    condition3 = np.where(
        perp_slope3 == 0,
        mid_point3[:, 1] == 1,
        np.where(
            np.isnan(perp_slope3),
            (0 <= mid_point3[:, 0]) & (mid_point3[:, 0] <= 1),
            (0 <= x_at_y1) & (x_at_y1 <= 1)
        )
    )
    intersection[idx3] = condition3

    # Calculate the probability for this iteration
    probability = np.sum(intersection) / num_points
    total_probability += probability

    # End the timer and calculate runtime
    end_time = time.time()
    runtime = end_time - start_time
    total_runtime += runtime

    print(f"Iteration {i + 1}: Probability = {probability:.6f}, Runtime = {runtime:.2f} seconds")

# Calculate averages
average_probability = total_probability / num_iterations
average_runtime = total_runtime / num_iterations

# Display final results
print(f"\nAverage Probability over {num_iterations} iterations: {average_probability:.6f}")
print(f"Average Runtime per iteration: {average_runtime:.2f} seconds")

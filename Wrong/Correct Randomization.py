import numpy as np

def simulate_bisector_intersections_vectorized(z):
    """
    Simulate z pairs of (x, y) variables, assign one point as the chosen point,
    and determine whether the perpendicular bisector of the pair intersects
    the closest side of the unit square to the chosen point.

    This is the vectorized version for improved performance with large z.

    Parameters:
        z (int): The number of pairs to simulate.

    Returns:
        float: The probability that the perpendicular bisector intersects the
               closest side to the chosen point.
    """
    # Initialize the Philox random number generator
    rng = np.random.Generator(np.random.Philox())

    # Generate z pairs of (x, y) points within the unit square [0, 1] x [0, 1]
    xy_pairs = rng.uniform(0, 1, size=(z, 2, 2))  # Shape: (z, 2, 2)

    # Randomly assign one point in each pair as the chosen point (50/50 chance)
    random_choices = rng.integers(0, 2, size=z)  # 0 or 1 for each pair
    P_chosen = xy_pairs[np.arange(z), random_choices]        # Shape: (z, 2)
    P_other = xy_pairs[np.arange(z), 1 - random_choices]     # Shape: (z, 2)

    # Coordinates of the chosen points
    x_chosen = P_chosen[:, 0]  # Shape: (z,)
    y_chosen = P_chosen[:, 1]  # Shape: (z,)

    # Compute distances to the sides from the chosen points
    distances = np.stack([
        x_chosen,          # Distance to left side (x = 0)
        1 - x_chosen,      # Distance to right side (x = 1)
        y_chosen,          # Distance to bottom side (y = 0)
        1 - y_chosen       # Distance to top side (y = 1)
    ], axis=1)  # Shape: (z, 4)

    # Identify the closest sides (0: left, 1: right, 2: bottom, 3: top)
    closest_sides = np.argmin(distances, axis=1)  # Shape: (z,)

    # Compute the midpoints M of the line segments connecting P_chosen and P_other
    M = (P_chosen + P_other) / 2  # Shape: (z, 2)
    Mx = M[:, 0]
    My = M[:, 1]

    # Direction vectors D of the line segments
    D = P_other - P_chosen  # Shape: (z, 2)
    D_x = D[:, 0]
    D_y = D[:, 1]

    # Initialize an array to store whether there is an intersection
    intersects = np.zeros(z, dtype=bool)

    # Compute intersection with the left side (x = 0)
    mask_left = (closest_sides == 0) & (D_y != 0)
    y_intersect_left = My[mask_left] + (D_x[mask_left] * (0 - Mx[mask_left])) / D_y[mask_left]
    intersects[mask_left] = (y_intersect_left >= 0) & (y_intersect_left <= 1)

    # Compute intersection with the right side (x = 1)
    mask_right = (closest_sides == 1) & (D_y != 0)
    y_intersect_right = My[mask_right] + (D_x[mask_right] * (1 - Mx[mask_right])) / D_y[mask_right]
    intersects[mask_right] = (y_intersect_right >= 0) & (y_intersect_right <= 1)

    # Compute intersection with the bottom side (y = 0)
    mask_bottom = (closest_sides == 2) & (D_x != 0)
    x_intersect_bottom = Mx[mask_bottom] + (D_y[mask_bottom] * (0 - My[mask_bottom])) / D_x[mask_bottom]
    intersects[mask_bottom] = (x_intersect_bottom >= 0) & (x_intersect_bottom <= 1)

    # Compute intersection with the top side (y = 1)
    mask_top = (closest_sides == 3) & (D_x != 0)
    x_intersect_top = Mx[mask_top] + (D_y[mask_top] * (1 - My[mask_top])) / D_x[mask_top]
    intersects[mask_top] = (x_intersect_top >= 0) & (x_intersect_top <= 1)

    # Calculate the probability over all pairs
    count_intersect = np.sum(intersects)
    probability = count_intersect / z
    return probability

# Example usage:
if __name__ == "__main__":
    z = 100000000  # Large number of pairs to simulate
    probability = simulate_bisector_intersections_vectorized(z)
    print(f"Probability of intersection: {probability}")

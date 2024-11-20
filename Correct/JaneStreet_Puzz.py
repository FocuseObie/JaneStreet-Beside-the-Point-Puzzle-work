import random
import numpy as np
import torch
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2, ks_2samp
import randomgen
import random
import numpy as np
import secrets
import tensorflow as tf
import torch
from Crypto.Random import get_random_bytes
import randomgen
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

z = 100000000  # Set a larger number of iterations for distribution analysis

# Preallocate storage for results (z samples, 8 generators, 4 values each: x_bounded, y_bounded, x_free, y_free)
results = np.empty((z, 8, 4))

# Function to generate bounded points using oversampling to ensure final count matches z
def generate_bounded_points_oversample(generator, z, factor=4):
    # Generate more points initially to increase the chance of having enough valid points
    oversample_size = z * factor
    x = generator(oversample_size)
    y = generator(oversample_size)
    mask = (y < x) & (y < 1 - x)
    
    # Extract the first z points that satisfy the condition
    x_bounded = x[mask][:z]
    y_bounded = y[mask][:z]
    
    # If not enough points are found, recursively try again with a larger factor
    while len(x_bounded) < z:
        factor += 1
        oversample_size = z * factor
        x = generator(oversample_size)
        y = generator(oversample_size)
        mask = (y < x) & (y < 1 - x)
        x_bounded = x[mask][:z]
        y_bounded = y[mask][:z]
    
    return x_bounded, y_bounded

# List of generators to be used
generators = [
    lambda size: np.random.uniform(0, 1, size=size),  # Python's random module (MT19937)
    lambda size: np.random.RandomState().uniform(0, 1, size=size),  # NumPy RandomState (legacy)
    lambda size: np.random.Generator(np.random.PCG64()).uniform(0, 1, size=size),  # NumPy Generator with PCG64
    lambda size: np.random.Generator(np.random.Philox()).uniform(0, 1, size=size),  # NumPy Generator with Philox
    lambda size: np.random.Generator(np.random.SFC64()).uniform(0, 1, size=size),  # NumPy Generator with SFC64
    lambda size: torch.rand(size).numpy(),  # PyTorch random number generation
    lambda size: randomgen.Xoroshiro128().random_raw(size) / (2**64),  # RandomGen Xoroshiro128
    lambda size: randomgen.JSF().random_raw(size) / (2**64),  # RandomGen JSF
]

methods = [
    "Python random",
    "NumPy RandomState",
    "PCG64",
    "Philox",
    "SFC64",
    "PyTorch",
    "Xoroshiro128",
    "JSF",
]

# Generate all points for each generator
for i, generator in enumerate(generators):
    x_bounded, y_bounded = generate_bounded_points_oversample(generator, z)
    results[:, i, 0] = x_bounded
    results[:, i, 1] = y_bounded
    results[:, i, 2:4] = generator((z, 2))  # Free points


# Now, compute the probability that such an x exists for each generator
probabilities = np.zeros(len(generators))  # To store the estimated probabilities for each method

for i in range(len(generators)):
    x1 = results[:, i, 0]  # x_bounded
    y1 = results[:, i, 1]  # y_bounded
    x2 = results[:, i, 2]  # x_free
    y2 = results[:, i, 3]  # y_free

    # Initialize an array to store the solutions x
    x_sol = np.empty(z)
    x_sol.fill(np.nan)  # Fill with NaN to identify undefined cases

    # Identify cases where x1 != x2
    not_equal_mask = x1 != x2

    # Compute x for x1 != x2
    numerator = (x1[not_equal_mask]**2 - x2[not_equal_mask]**2) + (y1[not_equal_mask]**2 - y2[not_equal_mask]**2)
    denominator = 2 * (x1[not_equal_mask] - x2[not_equal_mask])
    x_sol[not_equal_mask] = numerator / denominator

    # Handle cases where x1 == x2
    equal_mask = ~not_equal_mask
    y_equal_mask = equal_mask & (y1 == y2)
    y_not_equal_mask = equal_mask & (y1 != y2)

    # For x1 == x2 and y1 == y2, any x suffices (choose x = 0.5 for simplicity)
    x_sol[y_equal_mask] = 0.5  # Arbitrary value within [0,1]

    # For x1 == x2 and y1 != y2, there is no solution (x_sol remains NaN)

    # Check if the computed x lies within [0,1]
    exists = (x_sol >= 0) & (x_sol <= 1)
    count = np.sum(exists)

    # Estimate the probability
    probabilities[i] = count / z

# Print the estimated probabilities for each method
for method, prob in zip(methods, probabilities):
    print(f"Method: {method}, Estimated Probability: {prob:.6f}")
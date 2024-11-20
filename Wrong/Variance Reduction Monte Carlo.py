import numpy as np
from scipy.stats.qmc import Sobol

# Number of samples - much larger number needed for higher accuracy
N = 100000000  # Adjust to an even larger number if possible for high accuracy

# Use Sobol sequence to generate quasi-random samples
sampler = Sobol(d=4, scramble=True)
samples = sampler.random(N)

# Extract x1, x2, y2 from [0, 1] range
x1 = samples[:, 0]
x2 = samples[:, 1]
y2 = samples[:, 2]

# Generate y1 based on the bounds: [0, min(x1, 1 - x1)]
y1_upper_bound = np.minimum(x1, 1 - x1)
y1 = samples[:, 3] * y1_upper_bound

# Calculate x3 for each sample
denominator = 2 * (x1 - x2)
# Avoid division by zero
valid_denominator = denominator != 0

# Only consider samples where the denominator is not zero
x3 = np.zeros(N)
x3[valid_denominator] = (x1[valid_denominator]**2 + y1[valid_denominator]**2 - x2[valid_denominator]**2 - y2[valid_denominator]**2) / denominator[valid_denominator]

# Count how many values of x3 are in [0, 1]
count = np.sum((x3 >= 0) & (x3 <= 1) & valid_denominator)

# Estimate the probability
P = count / N

print(f"Estimated Probability: {P:.11f}")

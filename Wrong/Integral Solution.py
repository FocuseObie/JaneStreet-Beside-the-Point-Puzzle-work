import mpmath

mpmath.mp.dps = 15  # Set decimal precision to 15 digits

def integrand(x1, y1, x2, y2):
    if x1 == x2:
        return mpmath.mpf(0)
    numerator = (x1**2 - x2**2) + (y1**2 - y2**2)
    denominator = 2 * (x1 - x2)
    x = numerator / denominator
    if 0 <= x <= 1:
        return mpmath.mpf(1)
    else:
        return mpmath.mpf(0)

# Integration limits
x1_min = mpmath.mpf(0)
x1_max = mpmath.mpf(0.5)
y1_min = lambda x1: mpmath.mpf(0)
y1_max = lambda x1: x1
x2_min = mpmath.mpf(0)
x2_max = mpmath.mpf(1)
y2_min = mpmath.mpf(0)
y2_max = mpmath.mpf(1)

# Integration with manual iteration to minimize nested calls
def integrate():
    total_integral = mpmath.mpf(0)
    precision = 1e-12  # Define a small step size for numerical integration manually
    
    # Iterate over x1
    x1 = x1_min
    while x1 <= x1_max:
        # Iterate over y1 within the limits of y1_min to y1_max(x1)
        y1 = y1_min(x1)
        while y1 <= y1_max(x1):
            # Integrate over x2 for fixed x1 and y1
            inner_integral_x2 = mpmath.quad(
                lambda x2: mpmath.quad(
                    lambda y2: integrand(x1, y1, x2, y2), [y2_min, y2_max]
                ), [x2_min, x2_max]
            )
            total_integral += inner_integral_x2 * precision * precision
            y1 += precision
        x1 += precision
    
    return total_integral

# Compute the probability
P = 4 * integrate()
print(f"Estimated Probability: {P:.10f}")

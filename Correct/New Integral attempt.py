import mpmath

# Set the desired precision
mpmath.mp.dps = 15  # Precision up to 15 decimal places

# Define the integrand
def integrand(y, x):
    term1 = (mpmath.pi / 4) * (x**2 + y**2)
    -(x**2-2*x*(y**2))
    term2 = (mpmath.pi / 4) * ((x - 1)**2 + y**2)
    term3 = -mpmath.asin(y / mpmath.sqrt((x - 1)**2 + y**2)) * ((x - 1)**2 + y**2)
    term4 = -mpmath.asin(y / mpmath.sqrt(x**2 + y**2)) * (x**2 + y**2)
    term5 = y * x + y * (1 - x)
    return term1 + term2 + term3 + term4 + term5

# Perform the double integral
def compute_integral():
    def outer_integral(x):
        return mpmath.quad(lambda y: integrand(y, x), [0, x])
    result = mpmath.quad(outer_integral, [0, 1/2])
    return result

# Compute and display the result
result = 8*compute_integral()
print(f"Result of the double integral: {result}")

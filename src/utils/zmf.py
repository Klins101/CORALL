import numpy as np

def zmf(x, a, b):
    """
    Z-shaped membership function based on the piecewise definition.
    """
    if a >= b:
        raise ValueError("Parameter `a` must be smaller than `b`.")
    
    # Apply the piecewise function using direct if-else conditions
    y = np.zeros_like(x, dtype=float)
    
    # Condition 1: x <= a
    y[x <= a] = 1

    # Condition 2: a < x <= (a + b) / 2
    mask_1 = (a < x) & (x <= (a + b) / 2)
    y[mask_1] = 1 - 2 * ((x[mask_1] - a) / (b - a))**2

    # Condition 3: (a + b) / 2 < x <= b
    mask_2 = ((a + b) / 2 < x) & (x <= b)
    y[mask_2] = 2 * ((x[mask_2] - b) / (b - a))**2

    # Condition 4: x > b
    y[x > b] = 0

    return y
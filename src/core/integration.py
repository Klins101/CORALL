def integration(x_0, x_dot, dt):
    """
    Perform first-order Euler integration.

    Parameters:
    x_0 (float or numpy.array): Initial state
    x_dot (float or numpy.array): Rate of change
    dt (float): Time step

    Returns:
    float or numpy.array: Integrated state
    """
    return x_0 + x_dot * dt

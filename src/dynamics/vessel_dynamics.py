import numpy as np


def vessel_dynamics(x_0, inputs):
    """
    Calculate the vessel dynamics.

    Parameters:
    x_0 (numpy.array): Initial state [x, y, psi, r, b, u]
    inputs (numpy.array): Control inputs [tau_c, u_c]

    Returns:
    numpy.array: State derivatives [x_dot, y_dot, psi_dot, r_dot, b_dot, u_dot]
    """
    x, y, psi, r, b, u = x_0
    tau_c, u_c = inputs

    k_psi = 0.01
    t_psi = 30.0

    k_v = 1.0
    t_v = 50.0

    t_b = 20 * t_psi

    x_dot = u_c * np.cos(psi)
    y_dot = u_c * np.sin(psi)
    psi_dot = r

    w_r = 0
    w_b = 0.5 * np.random.randn()

    # Nomoto model
    r_dot = -(1/t_psi) * r + (1/t_psi) * k_psi * (tau_c - b) + w_r
    b_dot = -(1/t_b) * b + w_b
    u_dot = -(1/t_v) * u + (1/t_v) * k_v * u_c

    x_dot = np.array([x_dot, y_dot, psi_dot, r_dot, b_dot, u_dot])

    return x_dot

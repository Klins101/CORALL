import numpy as np
# Assuming you've defined the integration function in a separate file
from src.core.integration import integration


def obstacle_sim(x_ob0, y_ob0, v_ob, psi_ob, dt):
    """
    Simulate obstacle movement.

    Parameters:
    x_ob0 (array-like): Initial x-positions of obstacles
    y_ob0 (array-like): Initial y-positions of obstacles
    v_ob (array-like): Velocities of obstacles
    psi_ob (array-like): Heading angles of obstacles
    dt (float): Time step

    Returns:
    tuple: (x_ob, y_ob, vx_ob, vy_ob)
        x_ob (numpy.array): Updated x-positions of obstacles
        y_ob (numpy.array): Updated y-positions of obstacles
        vx_ob (numpy.array): x-components of obstacle velocities
        vy_ob (numpy.array): y-components of obstacle velocities
    """
    x_ob = np.zeros_like(x_ob0)
    y_ob = np.zeros_like(y_ob0)
    vx_ob = np.zeros_like(v_ob)
    vy_ob = np.zeros_like(v_ob)

    for i in range(len(x_ob0)):
        x_0 = np.array([x_ob0[i], y_ob0[i]])

        vx_ob[i] = v_ob[i] * np.cos(psi_ob[i])
        vy_ob[i] = v_ob[i] * np.sin(psi_ob[i])

        x_dot = np.array([vx_ob[i], vy_ob[i]])

        x = integration(x_0, x_dot, dt)

        x_ob[i] = x[0]
        y_ob[i] = x[1]

    return x_ob, y_ob, vx_ob, vy_ob

import numpy as np


def cpa_calculations2(v_x, v_y, vx_ob, vy_ob, psi, psi_ob, distance_ob, bearing_ob):
    """
    Calculate Closest Point of Approach (CPA) parameters using velocities and angles.

    Parameters:
    v_x, v_y (float): Velocity components of the vessel
    vx_ob, vy_ob (float): Velocity components of the obstacle
    psi (float): Heading angle of the vessel
    psi_ob (float): Heading angle of the obstacle
    distance_ob (float): Distance to the obstacle
    bearing_ob (float): Bearing to the obstacle

    Returns:
    tuple: (DCPA, TCPA, v_rel, psi_rel, alpha)
        DCPA (float): Distance at Closest Point of Approach
        TCPA (float): Time to Closest Point of Approach
        v_rel (float): Relative velocity between vessel and obstacle
        psi_rel (float): Relative heading angle
        alpha (float): Angle between line of sight and relative velocity
    """

    psi = -(psi - np.pi/2)
    psi_ob = -(psi_ob - np.pi/2)

    v = np.sqrt(v_x**2 + v_y**2)
    v_ob = np.sqrt(vx_ob**2 + vy_ob**2)

    v_rel = np.sqrt(v**2 + v_ob**2 - 2*v*v_ob*np.cos(psi - psi_ob))

    if psi < psi_ob:
        psi_rel = psi - \
            np.arccos((v_rel**2 + v_ob**2 - v**2) / (2 * v_rel * v))
    else:
        psi_rel = psi + \
            np.arccos((v_rel**2 + v_ob**2 - v**2) / (2 * v_rel * v))

    alpha = psi_rel - psi - bearing_ob

    DCPA = abs(distance_ob * np.sin(alpha))
    TCPA = abs((distance_ob / v_rel) * np.cos(alpha))

    return DCPA, TCPA, v_rel, psi_rel, alpha

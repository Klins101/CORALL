import numpy as np


def cpa_calculations(x, y, x_1, y_1, x_obs, y_obs, x_obs_1, y_obs_1, ts):
    """
    Calculate Closest Point of Approach (CPA) parameters using positions.

    Parameters:
    x, y (float): Current position of the vessel
    x_1, y_1 (float): Previous position of the vessel
    x_obs, y_obs (float): Current position of the obstacle
    x_obs_1, y_obs_1 (float): Previous position of the obstacle
    ts (float): Time step

    Returns:
    tuple: (DCPA, TCPA, v_rel, alpha, psi_v_rel)
        DCPA (float): Distance at Closest Point of Approach
        TCPA (float): Time to Closest Point of Approach
        v_rel (float): Relative velocity between vessel and obstacle
        alpha (float): Angle between line of sight and relative velocity
        psi_v_rel (float): Angle of relative velocity
    """

    x_rel_1 = x_1 - x_obs_1
    y_rel_1 = y_1 - y_obs_1

    x_rel = x - x_obs
    y_rel = y - y_obs

    v_rel = np.sqrt((x_rel - x_rel_1)**2 + (y_rel - y_rel_1)**2) / ts

    psi_LOS = np.arctan2(y - y_obs, x - x_obs)

    psi_v_rel = np.arctan2(-(y_rel - y_rel_1), -(x_rel - x_rel_1))

    alpha = psi_LOS - psi_v_rel

    dist = np.sqrt((x - x_obs)**2 + (y - y_obs)**2)

    DCPA = dist * np.sin(alpha)
    TCPA = (dist * np.cos(alpha)) / v_rel

    return DCPA, TCPA, v_rel, alpha, psi_v_rel

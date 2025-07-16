import numpy as np


def cpa_calculations_0speed(x, y, x_obs, y_obs, v_x, v_y, vx_ob, vy_ob, distance_ob):
    """
    Calculate Closest Point of Approach (CPA) parameters.

    Parameters:
    x, y (float): Position of the vessel
    x_obs, y_obs (float): Position of the obstacle
    v_x, v_y (float): Velocity components of the vessel
    vx_ob, vy_ob (float): Velocity components of the obstacle
    distance_ob (float): Distance to the obstacle

    Returns:
    tuple: (DCPA, TCPA, relative_speed, alpha, psi_Vrel)
        DCPA (float): Distance at Closest Point of Approach
        TCPA (float): Time to Closest Point of Approach
        relative_speed (float): Relative speed between vessel and obstacle
        alpha (float): Angle between line of sight and relative velocity
        psi_Vrel (float): Angle of relative velocity
    """

    v_x_rel = vx_ob - v_x
    v_y_rel = vy_ob - v_y

    relative_speed = np.sqrt(v_x_rel**2 + v_y_rel**2)

    psi_Vrel = np.arctan2(vy_ob - v_y, vx_ob - v_x)

    psi_LOS = np.arctan2(y - y_obs, x - x_obs)

    alpha = psi_LOS - psi_Vrel

    DCPA = distance_ob * np.sin(alpha)
    TCPA = distance_ob * np.cos(alpha) / relative_speed

    return DCPA, TCPA, relative_speed, alpha, psi_Vrel

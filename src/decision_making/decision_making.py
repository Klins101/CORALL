import numpy as np


def decision_making(x, y, psi, x_ob, y_ob, psi_ob, v_rel, u, risk):
    """
    Make collision avoidance decisions based on COLREG rules.

    Parameters:
    x, y (float): Position of the vessel
    psi (float): Heading angle of the vessel
    x_ob, y_ob (array-like): Positions of the obstacles
    psi_ob (array-like): Heading angles of the obstacles
    v_rel (float): Relative velocity
    u (float): Speed of the vessel
    risk (array-like): Risk levels for each obstacle

    Returns:
    tuple: (colreg_no, heading_dir, speed_level, relative_bearing_ob)
        colreg_no (int): COLREG rule number
        heading_dir (int): Heading direction (-1: port, 0: maintain, 1: starboard)
        speed_level (int): Speed level
        relative_bearing_ob (array): Relative bearings to obstacles
    """

    colreg_no = 0
    heading_dir = 1  # 0: Head-on, 1: move to starboard, -1: move to port
    speed_level = 0

    distance_ob = np.sqrt((np.array(x_ob) - x)**2 + (np.array(y_ob) - y)**2)
    los_ob = np.arctan2((np.array(y_ob) - y), (np.array(x_ob) - x))

    relative_bearing_ob = psi - los_ob

    for i in range(len(x_ob)):
        if abs(relative_bearing_ob[i]) <= 6 * np.pi / 180:
            # Head-on (overtake/move to starboard)
            if v_rel >= u:
                # Head-on move to starboard
                colreg_no = 14
                heading_dir = 1
            else:
                # Head-on Overtake
                colreg_no = 13
                heading_dir = 1  # or -1 based on the risk

        elif 6 * np.pi / 180 < relative_bearing_ob[i] <= 112 * np.pi / 180:
            # Crossing - Give way
            colreg_no = 15.1
            heading_dir = 1

        elif -118 * np.pi / 180 <= relative_bearing_ob[i] < -6 * np.pi / 180:
            # Crossing - Stand on
            colreg_no = 15.2
            heading_dir = 0

        elif 112 * np.pi / 180 < relative_bearing_ob[i] or relative_bearing_ob[i] < -118 * np.pi / 180:
            # Overtaking - Stand on
            if v_rel >= u:
                # Head-on move to starboard
                colreg_no = 13
                heading_dir = 0
            else:
                # Head-on Overtake
                colreg_no = 13
                heading_dir = 0  # or -1 based on the risk

    return colreg_no, heading_dir, speed_level, relative_bearing_ob

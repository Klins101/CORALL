import numpy as np

def waypoint_selection(Xwpt, Ywpt, x, y, i_wpt):
    """
    Updates the waypoint index based on the vessel's position.

    Parameters:
    Xwpt (array-like): X-coordinates of waypoints
    Ywpt (array-like): Y-coordinates of waypoints
    x (float): Current x-position of the vessel
    y (float): Current y-position of the vessel
    i_wpt (int): Current waypoint index

    Returns:
    int: Updated waypoint index
    """
   
    Circ = 200/1852  # Threshold distance for selecting the next waypoint

    for j in range(i_wpt, len(Xwpt)):
        if np.sqrt((Xwpt[j] - x)**2 + (Ywpt[j] - y)**2) < Circ:
            if i_wpt < len(Xwpt) - 1:
                i_wpt += 1

    return i_wpt

def planning(Xwpt, Ywpt, x, y, i_wpt):
    """
    Calculates the planned heading angle based on waypoints.

    Parameters:
    Xwpt (array-like): X-coordinates of waypoints
    Ywpt (array-like): Y-coordinates of waypoints
    x (float): Current x-position of the vessel
    y (float): Current y-position of the vessel
    i_wpt (int): Current waypoint index

    Returns:
    float: Planned heading angle (psi_p)
    """
    
    # Ensure i_wpt is valid
    if i_wpt == 0:
        return None  # Handle case for the first waypoint

    Xewpt = Xwpt[i_wpt] - x
    Yewpt = Ywpt[i_wpt] - y
    # print(Xewpt, Yewpt)

    L = np.sqrt((Xwpt[i_wpt] - Xwpt[i_wpt - 1])**2 + (Ywpt[i_wpt] - Ywpt[i_wpt - 1])**2)
    S = (Xewpt * (Xwpt[i_wpt] - Xwpt[i_wpt - 1]) + Yewpt * (Ywpt[i_wpt] - Ywpt[i_wpt - 1])) / L

    delta_p = np.arctan2(Ywpt[i_wpt] - Ywpt[i_wpt - 1], Xwpt[i_wpt] - Xwpt[i_wpt - 1]) - np.arctan2(Yewpt, Xewpt)
    err = S * np.tan(delta_p)
    #print(err)
    
    rho = 2200/1852

    psi_p = np.arctan2(Yewpt, Xewpt) - np.arctan(err / rho) 

    return psi_p

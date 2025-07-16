def controller(psi_p, psi, r, v_p, b, ui_psi1, Ts):
    """
    Controller function for yaw and speed control.

    Parameters:
    psi_p (float): Desired yaw angle
    psi (float): Current yaw angle
    r (float): Yaw rate
    v_p (float): Desired speed
    u (float): Current speed (not used in this function)
    ui_psi1 (float): Previous integral error for yaw
    ts (float): Time step

    Returns:
    tuple: (tau_c, v_c, ui_psi1)
        tau_c (float): Yaw control input
        v_c (float): Speed control input
        ui_psi1 (float): Updated integral error for yaw
    """

    # Yaw Controller
    kp_yaw = 100.0
    kd_yaw = -500.0
    ki_yaw = 0.0

    # For unstable mode (commented out in the original)
    # kp_yaw = -100.0
    # kd_yaw = 500.0
    # ki_yaw = 0

    e_psi = psi_p - psi
    ui_psi = ui_psi1 + Ts * e_psi
    ui_psi1 = ui_psi

    tau_c = kp_yaw * e_psi + ki_yaw * ui_psi + kd_yaw * r

    # Speed Controller
    v_c = v_p

    return tau_c, v_c, ui_psi1

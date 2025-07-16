import numpy as np


def actuator_modeling(tau_c, sat_amp_s):
    tau_ac = tau_c

    if abs(tau_c) > sat_amp_s:
        tau_ac = np.sign(tau_c) * sat_amp_s

    return tau_ac

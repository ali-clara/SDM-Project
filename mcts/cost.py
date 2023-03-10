import numpy as np

gamma = 20  # Experimentally determined value


def getCost(current_state, next_state):
    """
    T - theta angles
    K - stiffness values
    P - pressure values"""
    K = np.matrix([[current_state.K[0], 0, 0], [0, current_state.K[1], 0], [0, 0, current_state.K[2]]])
    dt0 = np.matrix(current_state.dT)
    dt1 = np.matrix(next_state.dT)
    ddt = dt0 - dt1
    P0 = np.matrix(current_state.P)
    P1 = np.matrix(next_state.P)
    dP = P0 - P1
    return K * dt0 * np.transpose(ddt) + gamma * P0 * np.transpose(dP)

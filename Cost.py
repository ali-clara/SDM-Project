import numpy as np

gamma = 20  # Experimentally determined value


def getCost(current_state, next_state):
    K = np.matrix([[current_state.k1, 0, 0], [0, current_state.k2, 0], [0, 0, current_state.k3]])
    dt0 = np.matrix([[current_state.t1], [current_state.t2], [current_state.t2]])
    dt1 = np.matrix([[next_state.t1], [next_state.t2], [next_state.t2]])
    ddt = dt0 - dt1
    P0 = np.matrix([current_state.p1, current_state.p2, current_state.p3])
    P1 = np.matrix([next_state.p1, next_state.p2, next_state.p3])
    dP = P0 - P1
    return K * dt0 * np.transpose(ddt) + gamma * P0 * np.transpose(dP)

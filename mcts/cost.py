from state import State
from state_space import StateSpace
import numpy as np

_gamma = 0.2  # Experimentally determined value


def getCost(current_state, next_state, gamma=_gamma):
    """
    T - theta angles
    K - stiffness values
    P - pressure values"""
    K = np.diag(current_state.get_stiffness())
    dt0 = np.array(current_state.dT)
    dt1 = np.array(next_state.dT)
    ddt = dt1 - dt0
    P0 = np.array(current_state.P)
    P1 = np.array(next_state.P)
    dP = P1 - P0

    cost = ddt@K@dt0 + gamma * P0@dP
    return cost


if __name__ == "__main__":
    state_1 = State()
    ss = StateSpace(state_1)

    state_1.set_controls([1, 0.25, 0.5], 1)
    state_1.initialise()
    state_2 = ss.move_with_checks("p1_increase", sim=True, state=state_1)
    state_3 = ss.move_with_checks("fa_increase", sim=True, state=state_2)
    print(state_1)
    print(np.rad2deg(state_1.T))
    print(state_2)
    print(np.rad2deg(state_2.T))
    print(getCost(state_1, state_2))
    print(state_3)
    print(np.rad2deg(state_3.T))
    print(getCost(state_2, state_3))







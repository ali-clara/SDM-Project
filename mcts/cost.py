from state import State
from state_space import StateSpace
import numpy as np

gamma = 20  # Experimentally determined value


def getCost(current_state, next_state, gamma=20):
    """
    T - theta angles
    K - stiffness values
    P - pressure values"""
    K = np.diag(current_state.get_stiffness())
    dt0 = np.array(current_state.dT)
    dt1 = np.array(next_state.dT)
    ddt = dt0 - dt1
    P0 = np.array(current_state.P)
    P1 = np.array(next_state.P)
    dP = P0 - P1

    cost = ddt@K@dt0 + gamma * P0@dP
    return cost

if __name__ == "__main__":
    state_1 = State()
    ss = StateSpace(state_1)

    state_1.set_controls([1, 0.25, 0.5], 1)
    state_2 = ss.move_with_checks("p1_increase", sim=True, state=state_1)
    state_3 = ss.move_with_checks("p2_increase", sim=True, state=state_2)
    
    print(state_2, state_3)

    print(getCost(state_2, state_3))





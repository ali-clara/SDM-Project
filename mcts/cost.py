from state import State
from state_space import StateSpace
import numpy as np

gamma = 20  # Experimentally determined value


def getCost(current_state, next_state):
    """
    T - theta angles
    K - stiffness values
    P - pressure values"""
    K = np.diag(current_state.get_stiffness())
    print(K)
    dt0 = np.matrix(current_state.dT)
    print(dt0)
    dt1 = np.matrix(next_state.dT)
    ddt = dt0 - dt1
    print(ddt)
    P0 = np.matrix(current_state.P)
    P1 = np.matrix(next_state.P)
    dP = P0 - P1

    print(K*dt0*np.transpose(ddt))
    print(gamma*P0*np.transpose(dP))

    cost =  K * dt0 * np.transpose(ddt) + gamma * P0 * np.transpose(dP)
    return cost

if __name__ == "__main__":
    state_1 = State()
    ss = StateSpace(state_1)


    state_1.set_controls([0.25, 0, 0], 0)
    state_2 = ss.move_with_checks("p1_increase", sim=True, state=state_1)
    state_3 = ss.move_with_checks("p2_increase", sim=True, state=state_2)
    
    print(state_2, state_3)

    print(getCost(state_2, state_3))

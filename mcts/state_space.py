import random
import numpy as np
import copy
from mapping_pressure_to_stiffness import getStiffness
from quasistatics import Quasistatics
from state import State

## need a way to initialize the first k vals ##


class StateSpace:
    def __init__(self, state, start_pos=(np.deg2rad(45), 0, 0), goal_pos=(np.deg2rad(45), 0, 0)):
        self.start_pos = start_pos  # Starting joint angles
        self.goal_pos = goal_pos    # Goal joint angles
        self.state = state
        step_size = 0.25
        self.quasi_converter = Quasistatics()
        self.actions = {"p1_increase": step_size, 
                        # "p1_decrease": -step_size,
                        "p2_increase": step_size, 
                        # "p2_decrease": -step_size,
                        "p3_increase": step_size, 
                        # "p3_decrease": -step_size,
                        "fa_increase": step_size*8}
                        # "fa_decrease": -step_size}

    def update_state(self, action=None, dev=2, sim=False):
        """Updates the current state """
        if action is None:
            action = self.get_random_action()
        new_state = self.move_with_checks(action, dev, sim)
        self.state = new_state

    def move_with_checks(self, action, dev=2, sim=False, state=None):
        """Returns the new state if the move is valid. Otherwise returns the current state"""
        if state is None:
            state = self.state
        
        if self.check_valid_move(action, dev, sim, state):
            return self._transition(action, dev, sim, state)
        else:
            return state

    def _get_new_state_vars(self, action, p0, fa0, k, dev, sim):
        """Gets new pressure and tension values 
            based on previous values and action taken"""
        P = copy.copy(p0)
        fa = copy.copy(fa0)
        K = copy.copy(k)
        actions = list(self.actions.keys())

        # update pressure and stiffness based on action taken
        if action in actions[0]:
            # increase or decrease p1 accordingly
            P[0] = P[0] + self.actions[action]
            K[0] = getStiffness(P[0], dev, sim)
        elif action in actions[1]:
            # increase or decrease p2 accordingly
            P[1] = P[1] + self.actions[action]
            K[1] = getStiffness(P[1], dev, sim)
        elif action in actions[2]:
            # increase or decrease p3 accordingly
            P[2] = P[2] + self.actions[action]
            K[2] = getStiffness(P[2], dev, sim)
        elif action in actions[3]:
            # increase or decrease fa accordingly
            fa = fa + self.actions[action]

        return P, fa, K
    #
    # def _get_new_stiffness(self, P, dev, sim):
    #     """Gets new stiffness based on pressure mapping"""
    #     K = []
    #     for pressure in P:
    #         K.append(getStiffness(pressure, dev, sim))
    #     return K

    def _get_new_theta(self, fa, K):
        """Uses quasistatic equations to set the joint angles 
            based on tendon tension and knuckle stiffness"""
        self.quasi_converter.update_state(fa, K[0], K[1], K[2])
        self.quasi_converter.find_joint_angles()
        dT = self.quasi_converter.get_angles()
        T = dT
        # T[0] = dT[0] + np.deg2rad(45)
        T[0] = dT[0] + self.start_pos[0]

        return T, dT

    def _transition(self, action, dev=2, sim=False, state=None):
        """Returns the new state given the previous state and action
            Args - action taken (str), noise (stdev), 
                sim (bool, adds noise if not in sim), state (State())"""
        
        # initialize state, action, and state vars
        if state is None:
            state = self.state

        new_state = State()
        p0, fa0 = state.get_controls()
        k = state.get_stiffness()
        # calculate new state variables
        P, fa, K = self._get_new_state_vars(action, p0, fa0, k, dev, sim)
        # K = self._get_new_stiffness(P, dev, sim)
        T, dT = self._get_new_theta(fa, K)

        # update new state variables
        new_state.set_controls(P, fa)
        new_state.set_stiffness(K)
        new_state.set_theta(T)
        new_state.set_delta_theta(dT)

        return new_state

    def check_valid_move(self, action, dev=2, sim=False, state=None):
        """Returns True if move is valid, else returns False
            Args - action (str), state (State())"""
        if state is None:
            state = self.state

        upper_bound = 5  # psi
        lower_bound = 0 
        counter = True
        p0, fa0 = state.get_controls()
        k = state.get_stiffness()
        P, fa, K = self._get_new_state_vars(action, p0, fa0, k, dev, sim)

        # if any pressure values are outside the bounds, 
            # the move in invalid
        if any(x < lower_bound for x in P):
            counter = False
        elif any(x > upper_bound for x in P):
            counter = False
        # if the tension value is negative, the move is invalid
        elif fa < lower_bound:
            counter = False

        return counter

    def get_neighbors(self, state=None):
        """Returns all valid neighbor positions of the current state"""
        if state is None:
            state = self.state

        neighbors = []
        for action in self.actions:
            neighbor = self._transition(action, sim=True, state=state)
            if self.check_valid_move(action, 0, True, state):
                neighbors.append([neighbor])

        return neighbors
            
    def get_valid_actions(self, state=None):
        """Returns all valid actions from the current state"""
        if state is None:
            state = self.state

        valid_actions = []
        for action in self.actions:
            if self.check_valid_move(action, 0, True, state):
                valid_actions.append(action)

        return valid_actions
    
    def get_random_action(self, state=None):
        """Returns a random valid action"""
        if state is None:
            state = self.state

        action = None
        while action is None:
            actions = list(self.actions.keys())
            action = random.choice(actions)
            # If it is not a valid move, reset
            if not self.check_valid_move(action, 0, True, state):
                action = None

        return action


if __name__ == "__main__":

    s = State()
    s.set_controls([5, 0, 0], 0)
    s.initialise()
    ss = StateSpace(s)
    print(f"parent: {ss.state}")
    print(f"angles: {np.rad2deg(ss.state.get_theta())}")
    print(f"neighbors: {ss.get_neighbors()}")
    print(f"valid actions: {ss.get_valid_actions()}")
    ss.update_state("fa_increase")
    print(f"new_state: {ss.state}")
    print(f"new_angles: {np.rad2deg(ss.state.get_theta())}")

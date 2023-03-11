import random
import numpy as np
from mapping_pressure_to_stiffness import getStiffness
from quasistatics import Quasistatics
from state import State


class StateSpace:
    def __init__(self, state, start_pos, goal_pos):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.state = state
        step_size = 0.25
        self.quasi_converter = Quasistatics()
        self.actions = {"p1_increase": step_size, 
                        "p1_decrease": -step_size,
                        "p2_increase": step_size, 
                        "p2_decrease": -step_size,
                        "p3_increase": step_size, 
                        "p3_decrease": -step_size,
                        "fa_increase": step_size, 
                        "fa_decrease": -step_size}

    def update_state(self, action=None, dev=2, sim=False):
        if action is None:
            action = self.get_random_action()
        new_state = self._transition(action, dev, sim)
        self.state = new_state

    def move_with_checks(self, action, dev=2, sim=False, state=None):
        """Returns the move, if valid. Otherwise returns the current state"""
        if state is None:
            state = self.state
        
        if self.check_valid_move(action, state):
            return self._transition(action, dev, sim, state)
        else:
            return state

    def _transition(self, action, dev=2, sim=False, state=None):
        """Returns the new state given the previous state and action"""
        if state is None:
            state = self.state 

        actions = list(self.actions.keys())
        new_state = State()
        P, fa = state.get_controls()
        K = state.get_controls()

        if action in actions[0:2]:
            P[0] = P[0] + self.actions[action]
            K[0] = getStiffness(P[0], dev, sim)
        elif action in actions[2:4]:
            P[1] = P[1] + self.actions[action]
            K[1] = getStiffness(P[1], dev, sim)
        elif action in actions[4:6]:
            P[2] = P[2] + self.actions[action]
            K[2] = getStiffness(P[2], dev, sim)
        elif action in actions[6:8]:
            fa = fa + self.actions[action]

        self.quasi_converter.update_state(fa, K[0], K[1], K[2])
        self.quasi_converter.find_pulley_angle()
        dT = self.quasi_converter.get_angles()
        T = list(np.array(dT) + np.deg2rad(45))
        new_state.set_controls(P, fa)
        new_state.set_stiffness(K)
        new_state.set_theta(T)
        new_state.set_delta_theta(dT)

        return new_state

    def check_valid_move(self, action, state=None):
        if state is None:
            state = self.state

        upper_bound = 5  # psi
        lower_bound = 0  # psi
        counter = True
        actions = list(self.actions.keys())
        P, fa = state.get_controls()

        if action in actions[0:1]:
            P[0] = P[0] + self.actions[action]
            if P[0] > upper_bound or P[0] < lower_bound:
                counter = False

        elif action in actions[2:3]:
            P[1] = P[1] + self.actions[action]
            if P[1] > upper_bound or P[1] < lower_bound:
                counter = False

        elif action in actions[4:5]:
            P[2] = P[2] + self.actions[action]
            if P[2] > upper_bound or P[2] < lower_bound:
                counter = False

        return counter

    def get_neighbors(self, state=None):
        if state is None:
            state = self.state

        neighbors = []
        for action in self.actions:
            neighbor = self._transition(action, state)
            if self.check_valid_move(action, state):
                neighbors.append([neighbor])

            return neighbors
            
    def get_random_action(self):
        action = None
        while action is None:
            actions = list(self.actions.keys())
            action = random.choice(actions)
            # If it is not a valid move, reset
            if not self.check_valid_move(action):
                action = None
        return action
    
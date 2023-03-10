import numpy as np
from mapping_pressure_to_stiffness import getStiffness
from quasistatics import Quasistatics

class StateSpace:
    def __init__(self, state, start_pos, goal_pos):
        self.start_pos = start_pos
        self.goal_pos = goal_pos

        self.state = state

        step_size = 0.25
        self.actions = {"p1_increase": step_size, 
                        "p1_decrease": -step_size,
                        "p2_increase": step_size, 
                        "p2_decrease": -step_size,
                        "p3_increase": step_size, 
                        "p3_decrease": -step_size,
                        "fa_increase": step_size, 
                        "fa_decrease": -step_size,}
        
    def move_with_checks(self, action, state=None):
        """Returns the move, if valid. 
            Otherwise returns the current state"""
        if state is None:
            state = self.state
        
        for action in self.actions:
            new_state = self._transition(action, state)
            # see where we are
            # if invalid, don't move

        pass

    def _transition(self, action, state = None):
        """Returns the new state given the previous state and action"""
        if state is None:
            state = self.state 

        actions = self.actions.keys()

        if action in actions[0:1]:
            var_to_update = state.p1
            update_param = [self.actions[action], 0, 0, 0]
        elif action in actions[2:3]:
            var_to_update = state.p2
            update_param = [0, self.actions[action], 0, 0]
        elif action in actions[4:5]:
            var_to_update = state.p3
            update_param = [0, 0, self.actions[action], 0]
        elif action in actions[6:7]:
            var_to_update = state.fa
            update_param = [0, 0, 0, self.actions[action]]

        new_state = state.get_state() + np.array(update_param)
        return new_state

    def check_valid_move(self, action, state=None):
        if state is None:
            state = self.state

        pressure_upper_bound = 5  # psi
        pressure_lower_bound = 0  # psi

        new_pos = self._transition(action, state)
        new_pressure_vals = [new_pos[0], new_pos[1], new_pos[2]]

        if any(x > y for x, y in zip(new_pressure_vals, pressure_upper_bound)):
            return False
        elif any(x < y for x, y in zip(new_pressure_vals, pressure_lower_bound)):
            return False
        else:
            return True

    def get_neighbors(self, state=None):
        if state is None:
            state == self.state

        neighbors = []
        for action in self.actions:
            neighbor = self._transition(action, state)
            if self.check_valid_move(action, state):
                neighbors.append([neighbor])

            return neighbors
            
    def random_action():
        pass
    
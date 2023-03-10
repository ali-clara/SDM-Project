import numpy as np

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
        
    def move_with_checks(self, action, state):
        """Returns the move, if valid. 
            Otherwise returns the current state"""
        pressure_upper_bound = 5 # psi
        pressure_lower_pound = 0 # psi
        
        for action in self.actions:
            new_state = self._transition(action, state)
            # see where we are
            # if invalid, don't move

        pass

    def _transition(self, action, state = None):
        """Moves between states given action"""
        pass

    def check_valid_move(self, action):
        if position is None:
            position = self.pos

        pressure_upper_bound = 5  # psi
        pressure_lower_bound = 0  # psi

        new_pos = self._transition(action, position)
        new_pressure_vals = new_pos[0:2]

        if any(x > y for x, y in zip(new_pos, pressure_upper_bound)):
            return False
        elif any(x < y for x, y in zip(new_pos, pressure_lower_bound)):
            return False
        else:
            return True

    def get_neighbors():
        pass

    def random_action():
        pass
    
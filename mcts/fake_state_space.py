from random import randint
import numpy as np

class FakeStateSpace:
    def __init__(self, start_pos=(0,0), goal_pos=(10,10)):
        self.pos = np.array(start_pos)
        self.start_pos = np.array(start_pos)
        self.goal_pos = np.array(goal_pos)
        self.bounds = goal_pos[0]
        self.cardinal_directions = ["left", "right", "up", "down"]
        self.directions = {"left":[-1,0], "right":[1,0], "up":[0,-1], "down":[0,1]}

    def update_position(self, action=None):
        if action == None:
            action = self.get_action()
        new_pos = self._transition(action)
        self.pos = new_pos
        return new_pos
    
    def move_with_checks(self, action, position=None):
        """Returns the move, if valid. Otherwise returns the current position"""
        if position is None:
            position = self.pos
        
        if self.check_valid_move(action, position):
            return self._transition(action, position)
        else:
            return position

    
    def _transition(self, action, position=None):
        """Moves from position given action"""
        if position is None:
            position = self.pos

        new_pos = np.array(position) + self.directions[action]
        return new_pos
    
    def get_action(self, position=None):
        return self.random_action(position)
    
    def random_action(self, position=None):
        action = None
        while action is None:
            rands = randint(0, 3)
            action = self.cardinal_directions[rands]
            # If it is not a valid move, reset
            if not self.check_valid_move(action, position):
                action = None
        return action
    
    def check_valid_move(self, action, position=None):
        if position is None:
            position = self.pos

        new_pos = self._transition(action, position)

        if any(x > y for x, y in zip(new_pos, self.goal_pos)):
            return False
        elif any(x < y for x, y in zip(new_pos, self.start_pos)):
            return False
        else:
            return True
        
    def get_neighbors(self, position=None):
        neighbors = []
        for action in self.cardinal_directions:
            neighbor = self._transition(action, position)
            if self.check_valid_move(action, position):
                neighbors.append([neighbor, action])
        
        return neighbors

if __name__ == "__main__":

    ss = FakeStateSpace()

    # print(ss.random_action((0,1)))

    print(ss.move_with_checks("up", (2,0)))


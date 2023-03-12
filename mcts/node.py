from state_space import StateSpace
from state import State


class Node:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.parent_action = parent_action
        self.number_of_visits = 1

        if self.parent is None:
            self.min_cost = 0
        else:
            self.min_cost = self.parent.min_cost + 1
        
        self.max_cost = 1000

        ss = StateSpace(state)
        self.untried_actions = ss.get_valid_actions(self.state)

    def __repr__(self):
        return str(self.state)
    
    def total_cost(self):
        return self.max_cost + self.min_cost 
    
    def count(self):
        return self.number_of_visits
    
    def parent_node_count(self):
        return self.parent.number_of_visits
    
    def is_fully_expanded(self):
        """Returns True if a node has been fully expanded"""
        return len(self.untried_actions) == 0


if __name__ == "__main__":
    s = State()
    s.set_controls([1, 2, 3], 4)
    node = Node(s)
    print(node)
    print(node.state.get_controls())
    print(node.state.get_theta())


from collections import deque
import numpy as np
from fake_state_space import FakeStateSpace
ss = FakeStateSpace()

class State:
    def __init__(self):
        self.k1 = 0
        self.k2 = 0
        self.k3 = 0

        self.p1 = 0
        self.p2 = 0
        self.p3 = 0

        self.t1_0 = np.deg2rad(45)
        self.t2_0 = np.deg2rad(45)
        self.t3_0 = np.deg2rad(45)

        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        
        self.fa = 0

    def get_state(self):
        """Represents the state variables as a list"""
        state = [self.p1, self.p2, self.p3, self.fa]
        return state
    
    def update_state(self, fa, k1, k2, k3):
        self.fa = fa
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3

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
        
        self.max_cost = 100
        self.possible_actions = ["left", "right", "up", "down"]
        self.untried_actions = self.get_valid_actions()

    def __repr__(self):
        return str(self.state)
    
    def total_cost(self):
        return self.max_cost + self.min_cost 
    
    def count(self):
        return self.number_of_visits
    
    def parent_node_count(self):
        return self.parent.number_of_visits
    
    def get_valid_actions(self):
        valid_actions = []
        for action in self.possible_actions:
            if ss.check_valid_move(action, self.state):
                valid_actions.append(action)

        return valid_actions
    
    def is_fully_expanded(self):
        """Returns True if a node has been fully expanded"""
        return len(self.untried_actions) == 0


class Tree:
    def __init__(self, root_node):
        """Instantiates the linked list given nodes"""
        self.root = root_node
        self.current_node = None
    
    def transverse_tree(self, node):
        """Transverses from child to parent starting at node
            and returns the node data"""
        states = deque([])
        actions = deque([])
        while node is not None:
            states.appendleft(node.state)
            actions.appendleft(node.parent_action)
            node = node.parent
        return states, actions
    
    def add_child(self, parent_node, child_node):
        parent_node.children.append(child_node)
        child_node.parent = parent_node

    def remove_child(self, parent_node, child_node):
        parent_node.children = [child for child in self.children if child is not child_node]
        child_node.parent = parent_node

if __name__ == "__main__":
    node = Node((0,0), None)
    print(node)

    tree = Tree(node)
    print(tree.root)

    node_2 = Node((1,0), node, "right")
    node_3 = Node((0,1), node, "down")
    
    tree.add_child(node, node_2)
    tree.add_child(node, node_3)

    print(tree.transverse_tree(node_2))




    
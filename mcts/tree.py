from collections import deque
import numpy as np
from node import Node
from fake_state_space import FakeStateSpace
from state_space import StateSpace
ss = StateSpace()

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




    
from state import State


class Node:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.parent_action = parent_action
        self.number_of_visits = 0
        self.cost = 0


    def __repr__(self):
        return str(self.state)

    def count(self):
        return self.number_of_visits
    
    def parent_node_count(self):
        return self.parent.number_of_visits


if __name__ == "__main__":
    s = State()
    s.set_controls([1, 2, 3], 4)
    s.initialise()
    node = Node(s)
    print(node)
    print(node.state.get_controls())
    print(node.state.get_theta())


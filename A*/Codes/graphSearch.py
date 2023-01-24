import numpy as np

map = np.genfromtxt('Map_upd.csv', names=True, delimiter=',')
graph = np.genfromtxt('Graph.csv', delimiter=',')


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.weight = 0
        self.heuristic = 0
        self.total = 0


def get_distance(pos_1, pos_2):
    return graph[pos_1][pos_2]


def get_neighbours(position):
    neighbours = []
    for i in range(0, len(map)):
        if graph[position][i] != 0:
            neighbours.append(i)
    return neighbours


def node_position(t):
    for i in range(0, len(map)):
        if map[i][3] == t[0] and map[i][4] == t[1] and map[i][5] == t[2]:
            return i


def graph_search(start, end):
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.total < current_node.total:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)


        # Found the goal
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        neighbours = get_neighbours(current_node.position)
        for new_position in neighbours:
            # Create new node
            new_node = Node(current_node, new_position)
            # Append
            children.append(new_node)

        # Loop through children

        for child in children:

            counter1 = True
            counter2 = True
            # Child is on the closed list
            for closed_child in closed_list:
                if child.position == closed_child.position:
                    counter1 = False
                    break
            if counter1 == True:
                child.weight = current_node.weight + get_distance(current_node.position, child.position)
                child.heuristic = get_distance(child.position, end_node.position)
                child.total = child.weight + child.heuristic

                # Child is already in the open list
                for open_index, open_node in enumerate(open_list):
                    if child.position == open_node.position:
                        counter2 = False
                        if child.weight < open_node.weight:
                            counter2 = True
                            open_list.pop(open_index)
                            break

                # Add the child to the open list
                if counter2 == True:
                    open_list.append(child)

def print_path(path):
    for i in path:
        print(map[i])

if __name__ == '__main__':
    start_configuration = [1, 1, 1]
    start_position = node_position(start_configuration)
    end_configuration = [90, 15, 30]
    end_position = node_position(end_configuration)
    path = graph_search(start_position, end_position)
    print_path(path)



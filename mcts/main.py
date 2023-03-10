from tree import Node, Tree
from fake_state_space import FakeStateSpace
from collections import deque
import numpy as np

class MCTS:
    def __init__(self, start_pos=(0,0), goal_pos=(10,10)):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.start_node = Node(start_pos)
        self.tree = Tree(self.start_node)
        self.ss = FakeStateSpace(start_pos, self.goal_pos)

        self.current_node = self.start_node
        self.tree.current_node = self.current_node
        self.possible_actions = ["left", "right", "up", "down"]
        self.policy = deque([])
    
    #### ------------- MAIN MCTS FUNCTIONS ------------- ####
    def select_uct(self, node):
        """Choses the best child of node based on the highest UCT score
            WOULD NEED MODIFICATION TO WORK, total_cost IS A COST NOT A REWARD
            Args - node (type Node())"""
        child_weights = []
        c = np.sqrt(2)
        for child in node.children:
            uct_value = (child.total_cost() / child.count() + c*(np.log(node.count()) / child.count()))
            child_weights.append(uct_value)

        return node.children[np.argmax(child_weights)]
    
    def select(self, node):
        """Choses the best child of the node based on the lowest cost"""
        child_costs = [child.total_cost() for child in node.children]
        return node.children[np.argmin(child_costs)]

    def expand(self, node):
        """Expands the given node once. Returns the new child node"""
        child_node = None
        # creates a node from an action we haven't tried before
        while child_node is None:
            action = node.untried_actions.pop()
            # makes sure the move is valid
            if self.ss.check_valid_move(action, node.state):
                next_state = self.ss.move_with_checks(action=action, position=node.state)
                child_node = Node(state=next_state, parent=node, parent_action=action)
                node.children.append(child_node)
        
        return child_node

    def select_and_expand(self):
        """Performs the selection and expansion phase. Moves down the tree
            per the best child nodes until a leaf node is found. Expands
            the leaf node once """
        reward = 0
        current_node = self.current_node
        # while we haven't reached the goal
        while not self.reached_goal(current_node.state):
            # if we've fully expanded the node, move to the best child and update the reward
            if current_node.is_fully_expanded():
                child = self.select(current_node)
                current_node = child
                reward += self.reward(None, None, current_node.state)
            # otherwise, expand the node and return a child to begin simulation
            else:
                child = self.expand(current_node)
                return child, reward
            
        return current_node, reward
    
    def simulate(self, node, reward, sim_number=5):
        """Does 'sim_number' complete simulations from the given node. 
            Returns the cost of the best simulation
            (The one that took the smallest number of steps)"""
        num_step_history = []
        for i in range(sim_number):  
            current_hallucinated_state = node.state
            # keep track of the cost
            num_steps = 0
            # run a bunch of simulations, each capped at the simulation_limit
            simulation_limit = 100
            for _ in range(simulation_limit):
                new_state, action = self.random_simulation(current_hallucinated_state)
                current_hallucinated_state = new_state
                num_steps += 1
                if self.reached_goal(current_hallucinated_state):
                    break
            num_step_history.append(num_steps)
        
        # find the shortest number of steps it took this node to reach the goal
        simulation_cost = np.min(num_step_history)
        return simulation_cost
            
    def backpropagate(self, node, cost):
        """Updates the tree based on the best simulation cost"""
        while node is not None:
            # if we've found a shorter path to the goal, update the node cost
            if node.max_cost > cost:
                node.max_cost = cost
            node.number_of_visits += 1
            node = node.parent
    
   #### ------------- HELPER FUNCTIONS ------------- ####
   
    def reached_goal(self, state):
        """Returns true if the given state is the goal"""
        if all(x == y for x, y in zip(state, self.goal_pos)):
            return True
        else:
            return False

    def euclidian_distance(self, state_1, state_2):
        """Calculates the euclidian distance between two states"""
        state_1 = np.array(state_1)
        state_2 = np.array(state_2)
        return np.linalg.norm(state_1 - state_2)
    
    def reward(self, old_state, action, new_state):
        """Calculates the reward as the current distance to the goal 
            normalized by the total distance to the goal. Increases as you get closer to the goal"""
        current_to_goal = self.euclidian_distance(self.goal_pos, new_state)
        start_to_goal = self.euclidian_distance(self.goal_pos, self.start_pos)
        adj_dist_to_goal = 1 - current_to_goal / start_to_goal

        # prevents a special case of ln(0) somewhere down the line
        if adj_dist_to_goal == 0:
            adj_dist_to_goal = 0.001

        return adj_dist_to_goal

    def get_best_action(self, node):
        best_child = self.select(node)
        best_action = best_child.parent_action
        return best_action

    def random_simulation(self, state):
        random_action = self.ss.random_action(state)
        new_state = self.ss.move_with_checks(random_action, state)
        return new_state, random_action

    def greedy_simulation(self, state):
        neighbors = self.ss.get_neighbors(state)
        distances = []
        actions = []
        for neighbor, action in neighbors:
            distance = self.euclidian_distance(self.goal_pos, neighbor) 
            distances.append(distance)
            actions.append(action)

        greedy_action = actions[np.argmin(distances)]
        new_state = self.ss.move_with_checks(greedy_action, state)
        return new_state, greedy_action
    
    def node_from_state_and_parent(self, state, parent):
        for child in parent.children:
            if all(x == y for x, y in zip(child.state, state)):
                return child
            
        print(f"Did not find a child of {parent.state} with state {state}")

    #### ------------- FLIGHT CODE ------------- #### 
    
    def main(self):
        """Executes the algorithm"""
        while not self.reached_goal(self.current_node.state):
        # for i in range(3):
            run_param = 10
            for _ in range(run_param):
            # run MCTS to find the best action to take
                # print("expand")
                expanded_node, reward = self.select_and_expand()
                # returns how many steps
                # print("simulate")
                cost_to_go = self.simulate(expanded_node, reward)
                # print(f"simulated, got {cost_to_go}")
                # print("backprop")
                self.backpropagate(expanded_node, cost_to_go)

            # print("find best action")
            best_action = self.get_best_action(self.current_node)
            self.policy.append([self.current_node.state, best_action])

            # take that action
            next_state = self.ss.move_with_checks(best_action, self.current_node.state)
            print(f"Should move {best_action} from {self.current_node.state} to {next_state}")
            print(f"children: {self.current_node.children}")
            child_scores = [child.total_cost() for child in self.current_node.children]
            print(f"children costs: {child_scores}")
            child_adj_costs = [child.count() for child in self.current_node.children]
            print(f"children counts: {child_adj_costs}")
            print("-----")

            next_node = self.node_from_state_and_parent(next_state, self.current_node)
            self.current_node = next_node

if __name__ == "__main__":
    mcts = MCTS()
    mcts.main()

from node import Node
from state import State
from state_space import StateSpace
from collections import deque
import numpy as np
from cost import getCost

class MCTS:
    def __init__(self, start_pos=(np.deg2rad(45), 0, 0), goal_pos=(np.deg2rad(90), np.deg2rad(30), np.deg2rad(30))):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        
        start_state = State()
        self.start_node = Node(start_state)

        self.ss = StateSpace(state=start_state, start_pos=start_pos, goal_pos=goal_pos)

        self.current_node = self.start_node
        # self.tree.current_node = self.current_node
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
            uct_value = (child.max_cost / child.count() + c*(np.log(node.count()) / child.count()))
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
                ############### do we grow the tree with noise or not?? ####################
                next_state = self.ss.move_with_checks(action=action, state=node.state)
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
                # reward += self.reward(None, None, current_node.state)
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
        cost_history = []
        for i in range(sim_number):  
            current_hallucinated_state = node.state
            # keep track of the cost
            num_steps = 0
            cost = 0
            # run a bunch of simulations, each capped at the simulation_limit
            simulation_limit = 100
            for _ in range(simulation_limit):
                new_state, action = self.random_simulation(current_hallucinated_state)
                cost += self.get_cost(current_hallucinated_state, new_state)
                num_steps += 1
                current_hallucinated_state = new_state

                if self.reached_goal(current_hallucinated_state):
                    print("reached goal")
                    cost -= 5
                    break

            cost_history.append(cost)
            num_step_history.append(num_steps)
        
        # find the shortest number of steps it took this node to reach the goal
        # simulation_cost = np.min(num_step_history)
        simulation_cost = np.min(cost_history)
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
        if all(np.isclose(x,y, atol=0.05) for x, y in zip(state.get_theta(), self.goal_pos)):
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
        random_action = self.ss.get_random_action(state)
        new_state = self.ss.move_with_checks(random_action, sim=True, state=state)
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
            if all(x == y for x, y in zip(child.state.list_state_vars(), state.list_state_vars())):
                return child
            
        print(f"Did not find a child of {parent.state} with state {state}")

    def get_cost(self, current_state, next_state, gamma=20):
        """
        T - theta angles
        K - stiffness values
        P - pressure values"""
        K = np.diag(current_state.get_stiffness())
        dt0 = np.array(current_state.dT)
        dt1 = np.array(next_state.dT)
        ddt = dt0 - dt1
        P0 = np.array(current_state.P)
        P1 = np.array(next_state.P)
        dP = P0 - P1

        cost = ddt@K@dt0 + gamma * P0@dP
        return cost

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
            next_state = self.ss.move_with_checks(best_action, state=self.current_node.state)
            print(f"Should move {best_action} from {self.current_node.state} to {next_state}")
            # print(f"children: {self.current_node.children}")
            child_scores = [child.total_cost() for child in self.current_node.children]
            print(f"children costs: {child_scores}")
            # child_adj_costs = [child.count() for child in self.current_node.children]
            # print(f"children counts: {child_adj_costs}")
            # print("-----")

            print(f"angles: {np.rad2deg(self.current_node.state.get_theta())}")

            next_node = self.node_from_state_and_parent(next_state, self.current_node)
            self.current_node = next_node

if __name__ == "__main__":
    # mcts = MCTS()
    # mcts.main()
    s = State()
    ss = StateSpace(s)

    s.set_controls([0, 2, 5], 10)
    s.initialise()
    for i in range(100):
        new_state = ss.move_with_checks("fa_increase")
        print(f"new_state: {new_state}")
        print(f"new_angles: {np.rad2deg(new_state.get_theta())}")
        print(getCost(s, new_state))
        s = new_state

    

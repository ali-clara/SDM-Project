from node import Node
from state import State
from state_space import StateSpace
from collections import deque
import numpy as np
import time


class MCTS:
    def __init__(self, start_pos=(np.deg2rad(45), 0, 0), goal_pos=(np.deg2rad(90), np.deg2rad(60), np.deg2rad(60)), starting_P=[0, 0, 0], starting_fa=2):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        
        start_state = State(start_pos=start_pos)
        start_state.set_controls(starting_P, starting_fa)
        start_state.initialise()
        self.start_node = Node(start_state)

        self.ss = StateSpace(state=start_state, start_pos=start_pos, goal_pos=goal_pos)

        self.policy = deque([])
        self.angle_path = deque([])
        self.control_path = deque([])
        self.cost_path = deque([])
    
    #### ------------- MAIN MCTS FUNCTIONS ------------- ####

    def select_uct(self, node):

        child_weights = []
        c = 2
        for child in node.children:
            if child.count() == 0:
                return child
            else:
                uct_value = (child.cost / child.count() - c*(np.log(node.count()) / child.count()))  # minimization
                child_weights.append(uct_value)

        return node.children[np.argmin(child_weights)]
    
    def select(self, node):
        """Choses the best child of the node based on the lowest cost"""
        child_costs = [child.cost / child.count() for child in node.children]
        return node.children[np.argmin(child_costs)]

    def expand(self, node, dev=2):
        actions = self.ss.get_valid_actions(node.state)
        for action in actions:
            if self.ss.check_valid_move(action, state=node.state):
                next_state = self.ss.move_with_checks(action=action, state=node.state, dev=dev)
                real_cost = self.get_cost(node.state, next_state)
                child_node = Node(state=next_state, parent=node, parent_action=action, real_cost=real_cost)
                node.children.append(child_node)

        return node.children[0]

    def select_and_expand(self, dev=2):

        current_node = self.start_node
        while True:
            if current_node.count() == 0:
                return current_node
            elif current_node.count() == 1:
                return self.expand(current_node, dev)
            current_node = self.select_uct(current_node)

    
    def simulate(self, node):

        current_hallucinated_state = node.state
        cost = 0
        simulation_limit = 100
        steps = 0
        while self.reached_goal(current_hallucinated_state) is False and steps <= simulation_limit:
            new_state = self.greedy_simulation(current_hallucinated_state)
            cost += self.get_cost(current_hallucinated_state, new_state)
            current_hallucinated_state = new_state
            steps += 1
        if steps > simulation_limit:
            return cost + 5
        else:
            return cost

    def backpropagate(self, node, cost):
        """Updates the tree based on the best simulation cost"""
        while node is not None:
            node.cost += cost
            node.number_of_visits += 1
            node = node.parent
    
   #### ------------- HELPER FUNCTIONS ------------- ####
   
    def reached_goal(self, state):
        """Returns true if the given state is the goal"""
        if all(np.isclose(x, y, atol=0.03) for x, y in zip(state.get_theta(), self.goal_pos)):
            return True
        else:
            return False

    def euclidian_distance(self, state_1, state_2):
        """Calculates the euclidian distance between two states"""
        state_1 = np.array(state_1)
        state_2 = np.array(state_2)
        return np.linalg.norm(state_1 - state_2)

    def get_best_action(self, node):
        best_child = self.select(node)
        best_action = best_child.parent_action
        return best_action, best_child

    def random_simulation(self, state):
        random_action = self.ss.get_random_action(state)
        new_state = self.ss.move_with_checks(random_action, sim=True, state=state)
        return new_state

    def greedy_simulation(self, state):
        neighbors = self.ss.get_neighbors(state)
        distances = []
        for neighbor in neighbors:
            distance = self.euclidian_distance(self.goal_pos, neighbor[0].get_theta())
            distances.append(distance)

        new_state = neighbors[np.argmin(distances)][0]
        return new_state


    def get_cost(self, current_state, next_state, gamma=20):
        """
        T - theta angles
        K - stiffness values
        P - pressure values"""
        K = np.diag(current_state.get_stiffness())
        dt0 = np.array(current_state.dT)
        dt1 = np.array(next_state.dT)
        ddt = dt1 - dt0
        P0 = np.array(current_state.P)
        P1 = np.array(next_state.P)
        dP = P1 - P0
        a = ddt@K@dt0
        if a > 0:
            cost = a + gamma * P0@dP
        else:
            cost = gamma * P0@dP
        return cost

    #### ------------- FLIGHT CODE ------------- #### 
    
    def main(self, dev=2):
        """Executes the algorithm"""
        # print(np.rad2deg(self.goal_pos))

        start = time.time()
        while not self.reached_goal(self.start_node.state):
            # print(self.start_node, self.start_node.real_cost, np.rad2deg(self.start_node.state.get_theta()))
            run_param = 10
            for _ in range(run_param):
                expanded_node = self.select_and_expand(dev)
                cost_to_go = self.simulate(expanded_node)
                self.backpropagate(expanded_node, cost_to_go)

            best_action, best_child = self.get_best_action(self.start_node)
            self.policy.append([self.start_node.state, best_action])
            self.control_path.append(self.start_node.state.list_state_vars())
            self.angle_path.append(np.rad2deg(self.start_node.state.get_theta()))
            self.cost_path.append(self.start_node.real_cost)

            self.start_node = best_child
            runtime = time.time() - start
            if runtime > 100:
                # print(f"failed to reached goal after {runtime} sec")
                return False, runtime, self.start_node.real_cost

        # print(f"reached goal")
        return True, runtime, self.start_node.real_cost


if __name__ == "__main__":

    goals = [(np.deg2rad(85), np.deg2rad(25), np.deg2rad(20)), (np.deg2rad(60), np.deg2rad(40), np.deg2rad(25))]

    for goal in goals:
        print(np.rad2deg(goal))
        cost_list = []
        runtime_list = []
        deviation_list = []
        for deviation in range(0, 11):
            mcts = MCTS(goal_pos=goal)
            completed, runtime, cost = mcts.main(deviation)
            if completed:
                runtime_list.append(runtime)
                cost_list.append(cost)
                deviation_list.append(deviation)

        print(deviation_list)
        print(runtime_list)
        print(cost_list)

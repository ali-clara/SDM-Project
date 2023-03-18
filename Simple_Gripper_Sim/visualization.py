import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import copy
import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\SDM-Project\\mcts")

from main import MCTS
from gripper import Gripper

# helper functions to plot gripper geometry
def plot_one_link(ax, link):
    x = link[0]
    y = link[1]
    ax.plot(x, y)
    
def plot_gripper(ax, link_array):
    for link in link_array:
        plot_one_link(ax, link)


# initialize varying values of theta
pinch_start = (np.deg2rad(50), 0, 0)
pinch_goal = (np.deg2rad(85), np.deg2rad(25), np.deg2rad(20))
wrap_start = (np.deg2rad(30), 0, 0)
wrap_goal = (np.deg2rad(60), np.deg2rad(40), np.deg2rad(25))

##### ----------------------- Plotting performance at different neutral positions ----------------------- #####
"""  
# initialize test starting positions
starting_proximal_pos = [(np.deg2rad(25)), (np.deg2rad(30)), (np.deg2rad(35)), (np.deg2rad(40)),
                               (np.deg2rad(45)), (np.deg2rad(50)), (np.deg2rad(55)), (np.deg2rad(60))]

starting_posns = [(np.deg2rad(25), 0, 0), (np.deg2rad(30), 0, 0), (np.deg2rad(35), 0, 0), (np.deg2rad(40), 0, 0), 
                      (np.deg2rad(45), 0, 0), (np.deg2rad(50), 0, 0), (np.deg2rad(55), 0, 0), (np.deg2rad(60), 0, 0)]


# plotting time and cost vs proximal joint starting position
pinch_times = []
pinch_costs = []
wrap_times = []
wrap_costs = []

for start_pos in starting_posns:
    # pinch grasp
    print(f"Pinch grasp, start {np.rad2deg(start_pos)}, end goal {np.rad2deg(pinch_goal)}")
    print("Running mcts...")
    start = time.time()
    mcts = MCTS(start_pos=start_pos, goal_pos=pinch_goal)
    mcts.main()
    end = time.time()
    
    pinch_times.append(end-start)
    cost = mcts.start_node.real_cost
    pinch_costs.append(cost)

    # wrap grasp
    print(f"Wrap grasp, start {np.rad2deg(start_pos)}, end goal {np.rad2deg(wrap_goal)}")
    print("Running mcts...")
    start = time.time()
    mcts = MCTS(start_pos=start_pos, goal_pos=wrap_goal)
    mcts.main()
    end = time.time()
    
    wrap_times.append(end-start)
    cost = mcts.start_node.real_cost
    wrap_costs.append(cost)

# remove vals above the cap
pinch_pos = copy.copy(starting_proximal_pos)
for i, val in enumerate(pinch_times):
    if val >= 100:
        pinch_times[i] = np.nan
        pinch_costs[i] = np.nan
        pinch_pos[i] = np.nan

wrap_pos = copy.copy(starting_proximal_pos)
for i, val in enumerate(wrap_times):
    if val >= 100:
        wrap_times[i] = np.nan
        wrap_costs[i] = np.nan
        wrap_pos[i] = np.nan


plt.style.use('seaborn')
fig, ax = plt.subplots(1,2)

ax[0].plot(np.rad2deg(pinch_pos), pinch_times, '-o', label="Pinch")
ax[0].plot(np.rad2deg(wrap_pos), wrap_times, '--o', label="Wrap")
ax[0].set_title("Simulation Time")
ax[0].set_xlabel("Neutral Proximal Knuckle Position (degrees)")
ax[0].set_ylabel("Simulation Time (sec)")

ax[1].plot(np.rad2deg(pinch_pos), pinch_costs, '-o')
ax[1].plot(np.rad2deg(wrap_pos), wrap_costs, '--o')
ax[1].set_title("Simulation Cost")
ax[1].set_xlabel("Neutral Proximal Knuckle Position (degrees)")
ax[1].set_ylabel("Simulation Cost (N-mm)")

fig.legend()
plt.suptitle("MCTS Performance at Varying Neutral Proximal Knuckle Positions")
plt.show()
"""


##### ----------------------- plotting gripper animation and control variables ----------------------- #####

print("Running mcts...")
start = time.time()
mcts = MCTS(start_pos=pinch_start, goal_pos=pinch_goal)                ##### adjust grasp type here
mcts.main()
end = time.time()
print(f"Found goal in {end-start} seconds")

angles = mcts.angle_path
controls = mcts.control_path
cost = mcts.cost_path

theta_1 = []
theta_2 = []
theta_3 = []
for angle_set in angles:
    theta_1.append(angle_set[0])
    theta_2.append(angle_set[1])
    theta_3.append(angle_set[2])

# for _ in range(10):
#     theta_1.append(theta_1[-1])
#     theta_2.append(theta_2[-1])
#     theta_3.append(theta_3[-1])

# fig, ax = plt.subplots()
# # function that draws each frame of the animation
# def animate(i):
#     ax.clear()
#     grp = Gripper(angles=[theta_1[i], theta_2[i], theta_3[i]])
#     grp.create_gripper()
#     plot_gripper(ax, grp.link_array)
#     ax.set_xlim(-8,8)
#     ax.set_ylim(-1,7)
#     ax.set_aspect('equal')
#     goal_display = np.round(np.rad2deg(pinch_goal))                    ##### adjust grasp type here             
#     ax.set_title(f"Pinch Grasp: Goal Pos {goal_display} deg")          ##### adjust grasp type here

# # run the animation
# ani = FuncAnimation(fig, animate, len(theta_1))
# plt.show()
# ani.save('gifs/pinch_wide2.gif', writer='imagemagick', fps=60)         ##### adjust grasp type here

# plot the control vars

p1 = []
p2 = []
p3 = []
fa = []
for control_var in controls:
    p1.append(control_var[0])
    p2.append(control_var[1])
    p3.append(control_var[2])
    fa.append(control_var[3])

iterations = np.arange(0, len(p1), 1)

plt.style.use('seaborn')
fig, ax = plt.subplots(1,4)

ax[0].plot(iterations, p1)
ax[0].set_xlabel("Step")
ax[0].set_ylabel("Pressure (PSI)")
ax[0].set_title("Proximal Joint Pressure")

ax[1].plot(iterations, p2)
ax[1].set_xlabel("Step")
ax[1].set_ylabel("Pressure (PSI)")
ax[1].set_title("Middle Joint Pressure")

ax[2].plot(iterations, p3)
ax[2].set_xlabel("Step")
ax[2].set_ylabel("Pressure (PSI)")
ax[2].set_title("Distal Joint Pressure")

ax[3].plot(iterations, fa)
ax[3].set_xlabel("Step")
ax[3].set_ylabel("Tendion Tension (10^-1 N)")
ax[3].set_title("Tendon Tension")

plt.suptitle("MCTS-Generated Control Variables for Pinch Grasp")        ##### adjust grasp type here

plt.tight_layout()
plt.show()

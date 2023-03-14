import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
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
# theta_1 = np.linspace(0, np.deg2rad(30), 10)
# theta_2 = np.linspace(0, np.deg2rad(30), 10)
# theta_3 = np.linspace(0, np.deg2rad(60), 10)

pinch_start = (np.deg2rad(65), 0, 0)
pinch_goal = (np.deg2rad(85), np.deg2rad(12), np.deg2rad(5.5))
wrap_start = (np.deg2rad(30), 0, 0)
wrap_goal = (np.deg2rad(90), np.deg2rad(30), np.deg2rad(40))
print("Running mcts...")
start = time.time
mcts = MCTS(start_pos=pinch_start, goal_pos=pinch_goal)
mcts.main()
end = time.time
print(f"Found goal in {end-start} seconds")
angles = mcts.angle_path


theta_1 = []
theta_2 = []
theta_3 = []
for angle_set in angles:
    theta_1.append(angle_set[0])
    theta_2.append(angle_set[1])
    theta_3.append(angle_set[2])

fig, ax = plt.subplots()

# function that draws each frame of the animation
def animate(i):
    ax.clear()
    grp = Gripper(angles=[theta_1[i], theta_2[i], theta_3[i]])
    grp.create_gripper()
    plot_gripper(ax, grp.link_array)
    ax.set_xlim(-8,8)
    ax.set_ylim(-1,7)
    ax.set_aspect('equal')

# run the animation
ani = FuncAnimation(fig, animate, frames=20, interval=200, repeat=False)

plt.show()

ani.save('gifs/pinch_wide1.gif', writer='imagemagick', fps=60)
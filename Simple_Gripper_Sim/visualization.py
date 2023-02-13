import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
theta_1 = np.linspace(0, np.deg2rad(30), 10)
theta_2 = np.linspace(0, np.deg2rad(30), 10)
theta_3 = np.linspace(0, np.deg2rad(60), 10)

fig, ax = plt.subplots()

# function that draws each frame of the animation
def animate(i):
    ax.clear()
    grp = Gripper(angles=[theta_1[i], theta_2[i], theta_3[i]])
    grp.create_gripper()
    plot_gripper(ax, grp.link_array)
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_aspect('equal')

# run the animation
ani = FuncAnimation(fig, animate, frames=20, interval=200, repeat=False)
ani.save('animation.gif', writer='imagemagick', fps=60)

plt.show()
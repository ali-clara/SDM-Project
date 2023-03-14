#!/usr/bin/env python3

# The usual imports
import numpy as np
import matplotlib.pyplot as plt
import matrix_transforms as mt

def get_pts_as_numpy_array(pts_list):
        """ Get the points out as a 3xn array, last row 1'x (i.e., homogenous points)
        @return numpy array of XYs"""
        pts = np.ones((3, len(pts_list)))
        for i in range(len(pts_list)):
            pt = pts_list[i]
            for j in range(len(pt)):
                pts[j,i] = pt[j]
        return pts

def plot_multi_links_one_graph(ax, link_array):
      for link in link_array:
        x = link[0]
        y = link[1]
        ax.plot(x, y)

class Link():
    def __init__(self, length, height, angle, points):
        
        self.points = points
        self.link_length = length
        self.link_height = height

        self.matrix = None
        self.link = None
        self.angle = angle
    
    def create_link(self):
        ''' scale - (x,y) tuple of scaling factors to resize link
            position - (x,y) coordinates of link anchor
            angle - angle of link in radians '''

        matrix_seq = []
        scale_mat = {"type": "scale", "sx": self.link_length, "sy": self.link_height}
        trans_mat = {"type": "translate", "dx": self.link_length/2, "dy": 0}
        rot_mat = {"type": "rotate", "theta": self.angle}

        matrix_seq.append(scale_mat)
        matrix_seq.append(trans_mat)
        matrix_seq.append(rot_mat)
        
        self.matrix = mt.make_matrix_from_sequence(matrix_seq)
        self.link = self.matrix@self.points

    def translate_link(self, dx):
        trans_mat = {"type": "translate", "dx": dx, "dy": 0}
        matrix = mt.make_matrix_from_sequence([trans_mat])

        # self.matrix = matrix@self.matrix
        self.link = matrix@self.link

    def attach_and_rotate_second_link(self, link_0, offset):
        '''connects this link to the end of link_0 at the angle of link_0'''
        
        # where the x-axis has been rotated to (e.g where the point of attachment now is)
        x_trans = mt.get_axes_from_matrix(link_0.matrix)[0]
        trans_mat = mt.make_translation_matrix(x_trans[0]+offset, x_trans[1])
        rot_mat = mt.make_rotation_matrix(link_0.angle)

        transformation_matrix = trans_mat@rot_mat

        self.matrix = transformation_matrix@self.matrix
        self.link = self.matrix@self.points

    def attach_and_rotate_third_link(self, link_0, link_1, offset):
        # where the x-axis has been rotated to (e.g where the point of attachment now is)
        x_trans_0 = mt.get_axes_from_matrix(link_0.matrix)[0]
        trans_mat_0 = mt.make_translation_matrix(x_trans_0[0]+offset, x_trans_0[1])
        rot_mat_0 = mt.make_rotation_matrix(link_0.angle)

        x_trans_1 = mt.get_axes_from_matrix(link_1.matrix)[0]
        trans_mat_1 = mt.make_translation_matrix(x_trans_1[0], x_trans_1[1])
        rot_mat_1 = mt.make_rotation_matrix(link_1.angle)

        # translations and rotataions
        rot_mat = rot_mat_1@rot_mat_0
        trans_mat = trans_mat_1@trans_mat_0

        transformation_matrix = trans_mat@rot_mat

        self.matrix = transformation_matrix@self.matrix
        self.link = self.matrix@self.points

class Gripper():
    """Creates a 2-finger gripper, each link with 3 joints """
    def __init__(self, link_length=2, link_height=0.5, angles=[0, np.pi/6, np.pi/4]):
        self.length = link_length
        self.height = link_height
        self.angles = angles
        self.square = get_pts_as_numpy_array([[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5]])
        self.link_array = None

    def first_links(self):
        link_1_right = Link(self.length, self.height, self.angles[0], self.square)
        link_1_right.create_link()
        link_1_right.translate_link(2.0)

        link_1_left = Link(self.length, self.height, np.pi-self.angles[0], self.square)
        link_1_left.create_link()
        link_1_left.translate_link(-2.0)

        return link_1_right, link_1_left

    def second_links(self, link_1_right, link_1_left):
        link_2_right = Link(self.length, self.height, self.angles[1], self.square)
        link_2_right.create_link()
        link_2_right.attach_and_rotate_second_link(link_1_right, 2.0)

        link_2_left = Link(-self.length, self.height, np.pi-self.angles[1], self.square)
        link_2_left.create_link()
        link_2_left.attach_and_rotate_second_link(link_1_left, -2.0)

        return link_2_right, link_2_left

    def third_links(self, link_1_right, link_1_left, link_2_right, link_2_left):
        link_3_right = Link(self.length, self.height, self.angles[2], self.square)
        link_3_right.create_link()
        link_3_right.attach_and_rotate_third_link(link_1_right, link_2_right, 2.0)

        link_3_left = Link(self.length, self.height, np.pi-self.angles[2], self.square)
        link_3_left.create_link()
        link_3_left.attach_and_rotate_third_link(link_1_left, link_2_left, -2.0)

        return link_3_right, link_3_left

    def create_gripper(self):
        link_1_right, link_1_left = self.first_links()

        # trans_mat = {"type": "translate", "dx": 2.0, "dy": 0}
        # matrix = mt.make_matrix_from_sequence([trans_mat])
        # link_1_right.link = matrix@link_1_right.link

        link_2_right, link_2_left = self.second_links(link_1_right, link_1_left)
        link_3_right, link_3_left = self.third_links(link_1_right, link_1_left, link_2_right, link_2_left)

        self.link_array = [link_1_right.link, link_1_left.link, 
                            link_2_right.link, link_2_left.link, 
                            link_3_right.link, link_3_left.link]

    def plot_gripper(self):
        fig, ax = plt.subplots(1,1)
        ax.set_xlim(-8,8)
        ax.set_ylim(-5,5)
        ax.set_aspect('equal')
        plot_multi_links_one_graph(ax, self.link_array)
        plt.show()

if __name__ == "__main__":
    gripper = Gripper()
    gripper.create_gripper()
    gripper.plot_gripper()
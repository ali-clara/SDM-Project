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

def plot_one_link(ax, link):
        x = link[0]
        y = link[1]
        ax.plot(x, y)
        # ax.plot(x[0], (y[-2]+y[0])/2, 'o', fillstyle='full', color='black')

def plot_multi_links_one_graph(ax, link_array):
      for link in link_array:
        plot_one_link(ax, link)

class Link(object):
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

    def attach_and_rotate_first_link(self, link_0):
        '''connects this link to the end of link_0 at the angle of link_0'''
        
        # where the x-axis has been rotated to (e.g where the point of attachment now is)
        x_trans = mt.get_axes_from_matrix(link_0.matrix)[0]
        trans_mat = mt.make_translation_matrix(x_trans[0], x_trans[1])
        rot_mat = mt.make_rotation_matrix(link_0.angle)

        transformation_matrix = trans_mat@rot_mat

        self.matrix = transformation_matrix@self.matrix
        self.link = self.matrix@self.points

    def attach_and_rotate_second_link(self, link_0, link_1):
        # where the x-axis has been rotated to (e.g where the point of attachment now is)
        x_trans_0 = mt.get_axes_from_matrix(link_0.matrix)[0]
        trans_mat_0 = mt.make_translation_matrix(x_trans_0[0], x_trans_0[1])
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

if __name__ == "__main__":
    ##### set these parameters #####
    length = 2
    height = 1
    angles = [np.pi/6, np.pi/6, np.pi/4]
    ##### set these parameters #####

    square = get_pts_as_numpy_array([[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5]])
    
    link_1 = Link(length, height, angles[0], square)
    link_1.create_link()

    link_2 = Link(length, height, angles[1], square)
    link_2.create_link()
    link_2.attach_and_rotate_first_link(link_1)

    link_3 = Link(length, height, angles[2], square)
    link_3.create_link()
    link_3.attach_and_rotate_second_link(link_1, link_2)

    link_4 = Link(length, height, np.pi - angles[0], square)
    link_4.create_link()

    link_5 = Link(-length, height, np.pi - angles[1], square)
    link_5.create_link()
    link_5.attach_and_rotate_first_link(link_4)

    link_6 = Link(length, height, np.pi - angles[2], square)
    link_6.create_link()
    link_6.attach_and_rotate_second_link(link_4, link_5)

    fig, ax = plt.subplots(1,1)
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_aspect('equal')
    plot_multi_links_one_graph(ax, [link_1.link, link_2.link, link_3.link, link_4.link, link_5.link, link_6.link])
    plt.show()

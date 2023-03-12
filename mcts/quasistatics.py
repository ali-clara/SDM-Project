import numpy as np


class Quasistatics():
    def __init__(self, fa=0, k1=0, k2=0, k3=0):
        # knuckle radius values
        self.r1 = 1
        self.r2 = 1
        self.r3 = 1
        # knuckle stiffnesses
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        # tendon and pulley values
        self.fa = fa
        self.theta_a = 0
        self.ra = 1
        # joint angles
        self.theta_1 = 0
        self.theta_2 = 0
        self.theta_3 = 0

    def find_joint_angles(self):
        """Calculates theta 1, 2, and 3 (joint angles)
            based off knuckle stiffness, tendon radius, and tendon tension"""
        # set up the matrices
        k_mat = np.diag([self.k1, self.k2, self.k3])
        k_inv = np.linalg.inv(k_mat)
        r_vec = np.array([self.r1, self.r2, self.r3])
        f_vec = np.array([self.fa, self.fa, self.fa])
        # compute
        theta_vec = k_inv@r_vec*f_vec
        self.theta_1 = theta_vec[0]
        self.theta_2 = theta_vec[1]
        self.theta_3 = theta_vec[2]

    def find_pulley_angle(self):
        """Calculates theta_a based on joint angles and tendon radius"""
        # set up the vectors
        r_vec = np.array([self.r1, self.r2, self.r3])
        theta_vec = np.array([self.theta_1, self.theta_2, self.theta_3])
        # compute
        self.theta_a = (r_vec@theta_vec) / self.ra

    def update_state(self, fa, k1, k2, k3):
        self.fa = fa
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3

    def get_angles(self):
        return [self.theta_1, self.theta_2, self.theta_3]


if __name__ == "__main__":
    qs = Quasistatics(2, 2, 2, 2)
    qs.find_joint_angles()
    qs.find_pulley_angle()

    print(qs.theta_1, qs.theta_2, qs.theta_3)
    print(qs.theta_a)


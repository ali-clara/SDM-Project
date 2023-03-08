import numpy as np
import sympy as sp

# fa = sp.Symbol('fa')
# ra, r1, r2, r3 = sp.symbols('ra, r1, r2, r3')
# theta_a, theta_1, theta_2, theta_3 = sp.symbols('θa, θ1, θ2, θ3')
# k1, k2, k3 = sp.symbols('k1, k2, k3')

# # all column vectors by default
# fa_vec = sp.Matrix([fa])
# r_vec = sp.Matrix([r1, r2, r3])
# theta_vec = sp.Matrix([theta_1, theta_2, theta_3])
# k_mat = sp.diag(k1, k2, k3)

# print(r_vec.T@theta_vec)
# print(k_mat@theta_vec + r_vec@fa_vec)


class Quasistatics():
    def __init__(self, fa, k1, k2, k3):
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

if __name__ == "__main__":
    qs = Quasistatics(2, 2, 2, 2)
    qs.find_joint_angles()
    qs.find_pulley_angle()

    print(qs.theta_1, qs.theta_2, qs.theta_3)
    print(qs.theta_a)


import numpy as np
from mapping_pressure_to_stiffness import getStiffness
from quasistatics import Quasistatics


class State:
    def __init__(self, start_pos=[np.deg2rad(45),0,0]):
        self.K = [0, 0, 0]  # Joint stiffnesses [k1, k2, k3]
        self.P = [0, 0, 0]  # Knuckle pressures [p1, p2, p3]
        self.T = [0, 0, 0]  # Joint angles, initially set to neutral position
        self.dT = [0, 0, 0]  # Change in joint angles from neutral positions
        self.fa = 0  # Tendon tension
        self.start_pos = start_pos

    def __repr__(self) -> str:
        return str((self.P[0], self.P[1], self.P[2], self.fa))

    def list_state_vars(self):
        """Returns pressure and tension as one list"""
        return [self.P[0], self.P[1], self.P[2], self.fa]
    
    def get_controls(self):
        """Gives list of knuckle pressures and tendon tension."""
        return self.P, self.fa

    def set_controls(self, P, fa):
        """Sets knuckle pressures and tendon tension."""
        self.P = P
        self.fa = fa

    def get_stiffness(self):
        """Gives a list of joint stiffnesses."""
        return self.K

    def set_stiffness(self, K):
        """Sets joint stiffnesses."""
        self.K = K

    def get_theta(self):
        """Gives a list of joint angles."""
        return self.T

    def set_theta(self, T):
        """Sets joint angles."""
        self.T = T

    def get_delta_theta(self):
        """Gives a list of change in joint angles from neutral position."""
        return self.dT

    def set_delta_theta(self, dT):
        """Sets change in joint angles from neutral position."""
        self.dT = dT

    def initialise(self):
        """Initialises stiffness and joint angles after setting control inputs"""
        K = []
        for pressure in self.P:
            K.append(getStiffness(pressure, simulation=True))
        self.K = K

        quasi_converter = Quasistatics()
        quasi_converter.update_state(self.fa, self.K[0], self.K[1], self.K[2])
        quasi_converter.find_joint_angles()
        dT = quasi_converter.get_angles()
        T = dT
        # T[0] = dT[0] + np.deg2rad(45)
        T[0] = dT[0] + self.start_pos[0]
        self.T = T
        self.dT = T


if __name__ == "__main__":
    current_pos = [0, 0, 0, 0]
    state = State()
    print(state.get_controls())

    if all(x == y for x, y in zip(state.list_state_vars(), current_pos)):
        print("true")

    print(np.rad2deg(state.get_theta()))


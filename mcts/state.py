import numpy as np

class State:
    def __init__(self):
        self.k1 = 0
        self.k2 = 0
        self.k3 = 0

        self.p1 = 0
        self.p2 = 0
        self.p3 = 0

        self.t1_0 = np.deg2rad(45)
        self.t2_0 = np.deg2rad(45)
        self.t3_0 = np.deg2rad(45)

        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        
        self.fa = 0

    def get_state(self):
        """Represents the state variables as a list"""
        state = [self.p1, self.p2, self.p3, self.fa]
        return state
    
    def update_state(self, fa, k1, k2, k3):
        self.fa = fa
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
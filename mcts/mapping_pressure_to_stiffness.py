import numpy as np

pressure = np.array([0, 1, 2, 3, 4, 5])  # psi
stiffness = np.array([90, 120, 150, 180, 210, 240])  # Nmm/radians
slope, intercept = np.polyfit(pressure, stiffness, 1)

# deviation entered as percentage


def getStiffness(pressure, deviation=2, simulation=False):
    ideal = slope * pressure + intercept
    measurement_noise = np.random.normal(loc=0, scale=(deviation * ideal/100))
    if simulation is False:
        return ideal + measurement_noise
    else:
        return ideal

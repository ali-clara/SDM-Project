import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF


# Define input data (pressure and stiffness)
pressure = np.array([0, 1, 2, 3, 4, 5])
stiffness = np.array([90, 120, 150, 180, 210, 240])

# Define input pressure range
pressure_range = np.arange(0, 5, 0.25)

# Get ideal mapping parameters
slope, intercept = np.polyfit(pressure, stiffness, 1)

# Simulate noisy measurements of pressure-stiffness mapping
measurement_noise = np.random.normal(loc=0, scale=5, size=len(pressure_range))
noisy_stiffness = slope * pressure_range + intercept + measurement_noise
ideal_stiffness = slope * pressure_range + intercept
# Plot ideal and noisy mapping functions
plt.plot(pressure_range, ideal_stiffness, label='Ideal Mapping')
plt.plot(pressure_range, noisy_stiffness, label='Noisy Mapping')
plt.xlabel('Pressure')
plt.ylabel('Stiffness')
plt.legend()
plt.show()

pressure = pressure_range.reshape(-1, 1)
stiffness = noisy_stiffness
# Define GPR model with RBF kernel
kernel = RBF(length_scale=1.0)
model = GaussianProcessRegressor(kernel=kernel, alpha=0.1, n_restarts_optimizer=10)

# Fit GPR model to data
model.fit(pressure, stiffness)

# Calculate transition probabilities using GPR predictions and Gaussian noise
n = len(pressure)
transition_probs = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        pred_i, std_i = model.predict(pressure[i].reshape(1, -1), return_std=True)
        pred_j, std_j = model.predict(pressure[j].reshape(1, -1), return_std=True)
        transition_probs[i][j] = np.exp(-(pred_i - pred_j)**2 / (2*(std_i**2 + std_j**2)))

# Normalize transition probabilities
transition_probs /= np.sum(transition_probs, axis=1, keepdims=True)

print(np.round(transition_probs, 2))

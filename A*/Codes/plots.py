import matplotlib.pyplot as plt

pinch_K2 = [1.0, 1.0, 2.4, 1.33, 18.0, 9.0]
pinch_K3 = [1.0, 1.5, 1.5, 6.0, 6.0, 18.0]
pinch_T = [0.01745329, 0.78539816, 1.04719755, 1.04719755, 1.57079633, 1.57079633]
wrap_K2 = [1.0, 1.0, 2.0, 1.33, 6.0]
wrap_K3 = [1.0, 1.5, 1.5, 3.0, 3.0]
wrap_T = [0.01745329, 0.78539816, 1.04719755, 1.04719755, 1.57079633]

plt.figure(1)
plt.plot(pinch_K2, linewidth=4, label="Pinch")
plt.plot(wrap_K2, label="Wrap")
plt.title('Joint 2 Stiffness')
plt.ylabel('K2')
plt.grid(linestyle='--')
plt.legend()
plt.figure(2)
plt.plot(pinch_K3, linewidth=4, label="Pinch")
plt.plot(wrap_K3, label="Wrap")
plt.title('Joint 3 Stiffness')
plt.ylabel('K3')
plt.grid(linestyle='--')
plt.legend()
plt.figure(3)
plt.plot(pinch_T, linewidth=4, label="Pinch")
plt.plot(wrap_T, label="Wrap")
plt.title('Tendon Tension')
plt.ylabel('T')
plt.grid(linestyle='--')
plt.legend()
plt.show()

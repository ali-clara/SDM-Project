import numpy as np
import math

L1 = 10
L2 = 10
L3 = 10


def get_end_point(t1, t2, t3):
    t1, t2, t3 = get_radians(t1, t2, t3)
    x = L1 * np.cos(t1) + L2 * np.cos(t1 + t2) + L3 * np.cos(t1 + t2 + t3)
    y = L1 * np.sin(t1) + L2 * np.sin(t1 + t2) + L3 * np.sin(t1 + t2 + t3)
    return x, y


def get_distance(x1, y1, x2, y2):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance


def get_radians(t1, t2, t3):
    return math.radians(t1), math.radians(t2), math.radians(t3)


def get_values(x):
    return x[0], x[1], x[2], x[3], x[4], x[5]


if __name__ == '__main__':

    map = np.genfromtxt('Map_upd.csv', names=True, delimiter=',')

    graph = np.zeros((len(map), len(map)))
    for i in range(0, len(map)):
        for j in range(0, len(map)):
            if i is not j:
                K2i, K3i, Ti, t1i, t2i, t3i = get_values(map[i])
                K2j, K3j, Tj, t1j, t2j, t3j = get_values(map[j])
                if K2i == K2j or K3i == K3j or Ti == Tj:
                    xi, yi = get_end_point(t1i, t2i, t3i)
                    xj, yj = get_end_point(t1j, t2j, t3j)
                    graph[i][j] = get_distance(xi, yi, xj, yj)


    graph = np.around(graph, decimals=2)
    np.savetxt('Graph.csv', graph, delimiter=",")

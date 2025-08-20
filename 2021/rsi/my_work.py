import numpy as np
import matplotlib.pyplot as plt


winrate = [0.75, 0.67, 0.6, 0.5, 0.4, 0.33, 0.25]
odds = [0.33, 0.5, 0.67, 1, 1.5, 2, 3]


def TW(odd):
    return np.round(-np.log(0.99) / (np.log(1 + 0.01 * odd) - np.log(0.99)), 4)


def shortest_distance(odd, winrate, n=100000):
    lins = np.linspace(0, 10, n)
    y = TW(lins)
    least_distance = 1e100
    for i in range(n):
        dx = lins[i] - odd
        dy = y[i] - winrate
        distance = np.sqrt(dx**2 + dy**2)
        if distance < least_distance:
            least_distance = distance
    if winrate > TW(odd):
        return np.round(least_distance, 10)
    else:
        return -1 * np.round(least_distance, 10)


odd_linspace = np.linspace(0.1, 4, 10000)
plt.plot(odd_linspace, TW(odd_linspace))
plt.scatter(2.0, 0.55)
plt.scatter(1.5, 0.6)
plt.scatter(3.0, 0.4)

plt.show()

a = shortest_distance(2.0, 0.55)
b = shortest_distance(1.5, 0.6)
c = shortest_distance(2, 0.7)
d = shortest_distance(1, 0.4)
print(a, b, c, d)

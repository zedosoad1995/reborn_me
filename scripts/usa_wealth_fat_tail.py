import csv
import numpy as np
from scipy.linalg import solve

cs = [1, 1/8.8, 0.1/8.8, 0.01/8.8, 0.001/8.8, 100 / (8.8 * 578508)]
usa_wealth_stats = [(0.088, 1e6, 1), (1/100, 3.5e6, 1/8.8), (1/1000, 17.2e6, 0.1/8.8), (1/10000,
                                                                                        77.8e6, 0.01/8.8), (1/100000, 362e6, 0.001/8.8), (1/578508, 1e9), (1/500_000_000, 250e9)]

params = []
for i in range(len(usa_wealth_stats) - 1):
    row1 = usa_wealth_stats[i]
    row2 = usa_wealth_stats[i + 1]

    A = np.array([[row1[1], 1], [row2[1], 1]])
    b = np.array([np.log(row1[0]), np.log(row2[0])])
    a, b = solve(A, b)

    params.append((a, b, cs[i]))

with open('data/usa_fat_tail.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(params)

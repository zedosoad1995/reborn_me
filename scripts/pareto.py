import csv
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm
from math import exp, log, sqrt


def pareto(x, a, b):
    return 1 - (x / a)**(-b)


x_data = np.array([3.5e6*2, 17e6*2, 78e6*2, 362e6*2])
y_data = np.array([0.99, 0.999, 0.9999, 0.99999])

params, _ = curve_fit(pareto, x_data, y_data)

print(params)


def inverse_pareto(alpha, a, b):
    return a * ((1 - alpha)**(-1/b) - 1)


top_1_percent = inverse_pareto(
    1 - 1/300_000_000, float(params[0]), float(params[1]))

print("Top 1%:", top_1_percent)


def log_normal_percentile(mu, sigma, percentile):
    z_score = norm.ppf(percentile)
    value = exp(mu + sigma * z_score)
    return value


with open('data/wealth_params_simple.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    rows = [row for row in csvreader]

ratios_1perc = []
for row in rows:
    # print(row[0])
    # print(log_normal_percentile(float(row[1]), float(row[2]), 0.99))
    ratios_1perc.append((row[0], log_normal_percentile(
        float(row[1]), float(row[2]), 0.99) / 6979481))

with open('data/1perc_ration.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(ratios_1perc)

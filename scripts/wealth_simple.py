import csv
import math
import numpy as np
import pickle
from scipy.linalg import solve
from scipy.stats import expon, lognorm, pareto
from scipy.optimize import minimize
from scipy.interpolate import interp1d
from math import exp, log, sqrt
from scipy.stats import norm


def log_normal_params(mean, median):
    mu = log(median)
    sigma = sqrt(2 * (log(mean) - log(median)))
    return mu, sigma


def log_normal_percentile(mu, sigma, percentile):
    z_score = norm.ppf(percentile)
    value = exp(mu + sigma * z_score)
    return value


with open('data/country_wealth.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    countries = [row for row in csvreader]

usa_wealth_stats = [(0.088, 1e6), (1/100, 3.5e6), (1/1000, 17.2e6), (1/10000,
                                                                     77.8e6), (1/100000, 362e6), (1/578508, 1e9), (1/500_000_000, 250e9)]

params = []
for row in usa_wealth_stats:
    A = np.array([[1e6, 1], [3.5e6, 1]])
    b = np.array([np.log(0.088), np.log(1/100)])
    a, b = solve(A, b)

    params.append((a, b))

n = 10000
params_save = []

for country in countries[1:]:
    print(country[0])

    mean = float(country[1])
    median = float(country[2])

    weights = [float(c) for c in country[3:]]
    last_w = next((val for val in reversed(weights) if val != 0), None)

    mu, sigma = log_normal_params(mean, median)

    params_save.append([country[0], mu, sigma])

    # Function to find wealth at a given percentile
    def wealth_at_percentile(percentile):
        return np.percentile(mixture_data, 100 - percentile)

    ''' # Test function: get wealth at top 1%
    print("Wealth at top 1%:", wealth_at_percentile(0.000001)) '''

    # overall_mean = np.mean(mixture_data)
    # overall_median = np.median(mixture_data)

    # print(f"Overall Mean: {overall_mean}, Overall Median: {overall_median}")

    def get_percentile(percentile):
        c = (0.088 / last_w)
        rev_per = 1 - percentile

        if rev_per < last_w / 8.8 * 100/578508:
            return (math.log(c * rev_per) - b_usa_6) / alpha_usa_6
        elif rev_per < last_w / 8.8 * 0.001:
            return (math.log(c * rev_per) - b_usa_5) / alpha_usa_5
        elif rev_per < last_w / 8.8 * 0.01:
            return (math.log(c * rev_per) - b_usa_4) / alpha_usa_4
        elif rev_per < last_w / 8.8 * 0.1:
            return (math.log(c * rev_per) - b_usa_3) / alpha_usa_3
        elif rev_per < last_w / 8.8:
            return (math.log(c * rev_per) - b_usa_2) / alpha_usa_2
        elif rev_per < last_w:
            return (math.log(c * rev_per) - b_usa_1) / alpha_usa_1
        else:
            return ppf_interp(percentile)

    # print("Wealth at top 0.00001%:", get_percentile(1 - 1/10_000_000_000))

with open('data/wealth_params_simple.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(params_save)

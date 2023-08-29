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


with open('data/remaining_countries_wealth.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    countries = [row for row in csvreader]

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


with open('data/remaining_wealth_params_simple.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(params_save)

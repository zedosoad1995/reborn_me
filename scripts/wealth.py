import csv
import math
import numpy as np
import pickle
from scipy.linalg import solve
from scipy.stats import expon, lognorm, pareto
from scipy.optimize import minimize
from scipy.interpolate import interp1d

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

    observed_mean = float(country[1])
    observed_median = float(country[2])

    weights = [float(c) for c in country[3:]]

    last_w, last_idx = next(((val, i) for i, val in reversed(
        list(enumerate(weights))) if val != 0), (None, None))

    def objective(params):
        scale1, scale2, scale3, scale4, scale5, scale6, scale7 = params

        if scale1 <= 0 or scale2 <= 0 or scale3 <= 0 or scale4 <= 0 or scale5 <= 0 or scale6 <= 0 or scale7 <= 0:
            return np.inf

        bin1 = expon.rvs(scale=scale1, size=int(n * weights[0]))

        if last_idx == 1 and last_w < 5:
            bin2 = pareto.rvs(b=scale5, scale=scale2, size=int(n * weights[1]))
        else:
            bin2 = lognorm.rvs(s=scale5, scale=scale2,
                               size=int(n * weights[1]))

        if last_idx == 2 and last_w < 5:
            bin3 = pareto.rvs(b=scale6, scale=scale3, size=int(n * weights[2]))
        else:
            bin3 = lognorm.rvs(s=scale6, scale=scale3,
                               size=int(n * weights[2]))

        if last_w < 0.05:
            bin4 = pareto.rvs(b=scale7, scale=scale4, size=int(n * weights[3]))
        else:
            bin4 = lognorm.rvs(s=scale7, scale=scale4,
                               size=int(n * weights[3]))

        mixture = np.concatenate([bin1, bin2, bin3, bin4])

        gen_mean = np.mean(mixture)
        gen_median = np.median(mixture)

        return abs(gen_mean - observed_mean) + abs(gen_median - observed_median)

    initial_scales = [5000, 50000, 500000, 1e6, 2.5 if last_idx == 1 and last_w < 5 else 0.5,
                      2.5 if last_idx == 2 and last_w < 5 else 0.5, 2.5 if last_w < 5 else 0.5]

    result = minimize(objective, initial_scales, method='nelder-mead',
                      options={'maxiter': 100})

    best_scale1, best_scale2, best_scale3, best_scale4, best_scale5, best_scale6, best_scale7 = result.x

    case = 0
    print(last_idx, last_w)
    if last_idx == 1 and last_w < 5:
        case = 1
    elif last_idx == 2 and last_w < 5:
        case = 2
    elif last_idx == 3 and last_w < 5:
        case = 3

    params_save.append([country[0], *result.x, case])

    """ bin1 = expon.rvs(scale=best_scale1, size=int(n * weights[0]))

    if last_idx == 1 and last_w < 0.05:
        bin2 = pareto.rvs(b=best_scale5, scale=best_scale2,
                          size=int(n * weights[1]))
    else:
        bin2 = lognorm.rvs(s=best_scale5, scale=best_scale2,
                           size=int(n * weights[1]))

    if last_idx == 2 and last_w < 0.05:
        bin3 = pareto.rvs(b=best_scale6, scale=best_scale3,
                          size=int(n * weights[2]))
    else:
        bin3 = lognorm.rvs(s=best_scale6, scale=best_scale3,
                           size=int(n * weights[2]))

    if last_w < 0.05:
        bin4 = pareto.rvs(b=best_scale7, scale=best_scale4,
                          size=int(n * weights[3]))
    else:
        bin4 = lognorm.rvs(s=best_scale7, scale=best_scale4,
                           size=int(n * weights[3]))

    # Combine bins to create new, more accurate mixture distribution
    mixture_data = np.concatenate([bin1, bin2, bin3, bin4]) """

    """ sorted_data = np.sort(mixture_data)

    # Generate the corresponding percentiles
    percentiles = np.linspace(0, 1, len(sorted_data))

    # Create the interpolation function
    ppf_interp = interp1d(percentiles, sorted_data,
                          kind='linear', fill_value='extrapolate')

    with open(f'data/wealth_funcs/{country[0]}.pkl', 'wb') as f_out:
        pickle.dump(ppf_interp, f_out) """

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

with open('data/wealth_params.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(params_save)

import numpy as np
from scipy.optimize import linprog
from scipy.cluster.vq import vq, kmeans, whiten
from pprint import pprint

# import matchup chart from csv file
with open("dumb_mu_chart.csv", "r", encoding="utf8") as f:
    header_row = f.readline()
    char_names = header_row.split(',')[1:]
    char_names = [name.strip() for name in char_names]
    mu_chart = np.zeros((len(char_names), len(char_names)))
    for i in range(len(char_names)):
        mu_row = f.readline()
        matchups = mu_row.split(',')[1:]
        for j in range(len(matchups)):
            mu_chart[i][j] = float(matchups[j])
            if j < i:
                if mu_chart[i][j] + mu_chart[j][i] != 0.0:
                    print(i)
                    print(j)
                    print(mu_chart[i][j])
                    print(mu_chart[j][i])

# set up linear program
midpoint = 0
obj_coeffs = np.zeros(len(char_names))
A_ub = mu_chart
b_ub = midpoint * np.ones((len(char_names),))
A_eq = np.ones((1, len(char_names)))
b_eq = np.ones((1,))
result = linprog(obj_coeffs, A_ub, b_ub, A_eq, b_eq, method="revised simplex")

# compute the nash equilibrium
nash_eq = result.x

# put characters in tier list
## put all characters with nonzero representation in S tier
    ## sorted by nash value
## for characters with zero representation, sort by
    ## performance vs nash

tier_list_mode = "brf" #"recursive"

s_tier = []
a_tier = []
for i in range(len(char_names)):
    k = char_names[i]
    if nash_eq[i] < 1e-6:
        a_tier.append(('A', k, round(midpoint - result.slack[i], 2)))
    else:
        s_tier.append(('S', k, round(nash_eq[i], 2)))

s_tier = list(reversed(sorted(s_tier, key=lambda x: x[2])))
if tier_list_mode == "brf":
    a_values = [x[2] for x in a_tier]
    num_centroids = 3
    clusters = list(kmeans(a_values, num_centroids))[0]
    clusters = list(reversed(sorted(clusters)))
    non_s_tiers = [[] for _ in range(len(clusters))]
    for i in range(len(a_values)):
        argmin = min(enumerate(clusters), key = lambda x: abs(a_values[i] - x[1]))[0]
        updated_tuple = (chr(ord('A') + argmin), a_tier[i][1], a_tier[i][2])
        non_s_tiers[argmin].append(updated_tuple)

for i in range(len(non_s_tiers)):
    non_s_tiers[i] = list(reversed(sorted(non_s_tiers[i], key=lambda x:x[2])))

# print tier list
print()
pprint(s_tier)
for non_s_tier in non_s_tiers:
    print()
    pprint(non_s_tier)
print()


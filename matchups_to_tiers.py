import numpy as np
from scipy.optimize import linprog
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

# set up linear program
midpoint = 0
obj_coeffs = np.zeros(len(char_names))
A_ub = mu_chart
b_ub = midpoint * np.ones((len(char_names),))
A_eq = np.ones((1, len(char_names)))
b_eq = np.ones((1,))
result = linprog(obj_coeffs, A_ub, b_ub, A_eq, b_eq)

# compute the nash equilibrium
nash_eq = result.x

# put characters in tier list
## put all characters with nonzero representation in S tier
    ## sorted by nash value
## for characters with zero representation, sort by
    ## performance vs nash
char_scores = dict()
for i in range(len(char_names)):
    k = char_names[i]
    #print(char_scores)
    #print(result.slack)
    if nash_eq[i] < 1e-6:
        char_scores[k] = midpoint - result.slack[i]
    else:
        char_scores[k] = nash_eq[i] + 100.0
sorted_char_list = reversed(sorted(
    char_scores, key=lambda k:char_scores[k]))
tier_list = [('S' if char_scores[char] >= 1.0 else 'A', char, round(char_scores[char], 2)) for char in sorted_char_list]

# print tier list
pprint(tier_list)


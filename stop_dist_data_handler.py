from statistics import median
import numpy as np
from scipy.stats import skew
import json
import pdb


def json_extract(filename):
    data = []
    with open(filename, "r") as infile:
        raw = json.load(infile)
        for episode in raw:
            data.append(np.array(episode))

    return data


def print_stats(x):
    print(np.mean(x), median(x), skew(x))


# ex = np.loadtxt("/home/rfox/paavi_logs/eval_run_logs/stop_dist_None_data.csv")

ex5_42 = json_extract(
    "/home/rfox/paavi_logs/eval_run_logs/ped_distance_data/SD5_seed42.json"
)
for ex in ex5_42:
    print_stats(ex)
pdb.set_trace()

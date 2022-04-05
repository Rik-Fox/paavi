from statistics import median
import numpy as np
from scipy.stats import skew

x = np.loadtxt("/home/rawsys/mathgw/paavi_logs/eval_run_logs/stop_dist_None_data.csv")
x3 = np.loadtxt("/home/rawsys/mathgw/paavi_logs/eval_run_logs/stop_dist_3_data.csv")
x5 = np.loadtxt("/home/rawsys/mathgw/paavi_logs/eval_run_logs/stop_dist_5_data.csv")
x10 = np.loadtxt("/home/rawsys/mathgw/paavi_logs/eval_run_logs/stop_dist_10_data.csv")

print(np.mean(x), median(x), skew(x))
print(np.mean(x3), median(x3), skew(x3) )
print(np.mean(x5), median(x5), skew(x5) )
print(np.mean(x10), median(x10), skew(x10))


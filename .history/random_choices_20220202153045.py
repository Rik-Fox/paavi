import random
import matplotlib.pyplot as plt

x = [random.randint(1, 10) for i in range(5)]

samp = [random.choices(x, weights=x) for i in range(100)]
print(x)
print(samp)
plt.hist(samp, bins=10, density=True)
plt.show()
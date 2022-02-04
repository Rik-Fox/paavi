import random
import matplotlib.pyplot as plt

x = random.randint(5)

samp = [random.choices(x, weights=x) for i in range(100)]

plt.hist(samp)
plt.show()
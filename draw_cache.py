#!/usr/bin/python3

import matplotlib.pyplot as plt

input_file = open("data/lon.txt", "r")

values = [float(x) for x in input_file.readlines()]

t = [x for x in values if x < -90.0 or x > 90.0]

print(len(t), " / ", len(values), " = ", len(t) / len(values))

x = [x for x in values if x > 0.0]
y = [-x for x in values if x < 0.0]

x.sort()
y.sort()

print(len(x), ' ', len(y))

plt.hist(values, bins=500, histtype='step', color='red')
plt.hist([-x for x in values], bins=500, histtype='step', color='green')

plt.show()

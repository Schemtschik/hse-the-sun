#!/usr/bin/python3

import json
import matplotlib.pyplot as plt

import common

input_file = open("data/rgousfull.hsc.json", "r")
records = []
for line in input_file.readlines():
    records.append(common.Record())
    records[-1].__dict__.update(json.loads(line))

sunspots = common.getSunspotsFromRecords(records)

x = [sunspot.records[0].longtitude for sunspot in sunspots]

x.sort()

plt.hist(x, bins=500, histtype='step')
plt.show()


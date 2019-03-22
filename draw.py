#!/usr/bin/python3

import json
import matplotlib.pyplot as plt

import common

input_file = open("data/rgousfull.filtered.json", "r")
records = []
for line in input_file.readlines():
    records.append(common.Record())
    records[-1].__dict__.update(json.loads(line))

sunspots = common.getSunspotsFromRecords(records)
sunspots_count = len(sunspots)
sunspots.sort(key=lambda spot: spot.area)

step = [(180.0 * x / 14.0 - 90.0) for x in range(0, 15)]

x = [sunspot.records[0].longtitude for sunspot in sunspots]
x.sort()
plt.hist(x, bins=step, histtype='step')


def draw_percentile(a, b): # a/b - percentile
    area_limit = sunspots[sunspots_count * a // b].area
    x = [sunspot.records[0].longtitude for sunspot in sunspots if sunspot.area <= area_limit]
    x.sort()
    plt.hist(x, bins=step, histtype='step')


draw_percentile(3, 4)
draw_percentile(1, 2)
draw_percentile(1, 4)

plt.show()


#!/usr/bin/python3

from datetime import datetime
import json
import matplotlib.pyplot as plt

import common

def to_average(arr):
    N = 1461
    arr2 = []
    for i in range(N // 2, len(arr) - N // 2):
        arr2.append(sum(arr[i - N // 2 : i + N // 2 + 1]) / N)
    return arr2

input_file = open("data/rgousfull.marked.json", "r")
records = []
for line in input_file.readlines():
    records.append(common.Record())
    records[-1].__dict__.update(json.loads(line))

input_file2 = open("data/data.csv", "r")

numberByDate = dict()
for line in input_file2.readlines():
    (year, month, day, skip, number) = line.split(";")[:5]
    if int(year) <= 1975:
        continue
    numberByDate[year + "-" + month + "-" + day] = (int(number), 0)

sunspots = common.getSunspotsFromRecords(records)
for sunspot in sunspots:
    if not sunspot.old:
        continue
    for record in sunspot.records:
        date = datetime.utcfromtimestamp(record.time).strftime('%Y-%m-%d')
        numberByDate[date] = (numberByDate[date][0], numberByDate[date][1] + record.area)
plt.plot(to_average([i[1] for i in numberByDate.values()]))
plt.plot(to_average([i[0] for i in numberByDate.values()]))
plt.show()
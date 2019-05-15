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
    return [0] * (N // 2) + arr2

def compact(arr):
    arr2 = []
    for i in range(len(arr)):
        if i % 5 == 0:
            arr2.append(arr[i])
    return arr2

input_file2 = open("data/data.csv", "r")
numberByDate = dict()
for line in input_file2.readlines():
    (year, month, day, skip, number) = line.split(";")[:5]
    if int(year) > 2013 or int(year) < 1900:
        continue
    numberByDate[year + "-" + month + "-" + day] = (int(number), 0, 0)
plt.plot(to_average([i[0] for i in numberByDate.values()]), label='Daily total sunspot number')

input_file = open("data/rgofull.marked.json", "r")
records = []
for line in input_file.readlines():
    records.append(common.Record())
    records[-1].__dict__.update(json.loads(line))
sunspots = common.getSunspotsFromRecords(records)
for sunspot in sunspots:
    if not sunspot.old:
        continue
    for record in sunspot.records:
        date = datetime.utcfromtimestamp(record.time).strftime('%Y-%m-%d')
        if record.latitude >= 0:
            numberByDate[date] = (numberByDate[date][0], numberByDate[date][1] + record.area, numberByDate[date][2])
        else:
            numberByDate[date] = (numberByDate[date][0], numberByDate[date][1], numberByDate[date][2] + record.area)

input_file = open("data/rgousfull.marked.json", "r")
records = []
for line in input_file.readlines():
    records.append(common.Record())
    records[-1].__dict__.update(json.loads(line))
sunspots = common.getSunspotsFromRecords(records)
for sunspot in sunspots:
    if not sunspot.old:
        continue
    for record in sunspot.records:
        date = datetime.utcfromtimestamp(record.time).strftime('%Y-%m-%d')
        if record.latitude >= 0:
            numberByDate[date] = (numberByDate[date][0], numberByDate[date][1] + record.area, numberByDate[date][2])
        else:
            numberByDate[date] = (numberByDate[date][0], numberByDate[date][1], numberByDate[date][2] + record.area)
plt.plot(to_average([i[1] for i in numberByDate.values()]), 'orange', label='NH total sunspots area')
plt.plot(to_average([i[2] for i in numberByDate.values()]), 'green', label='SH total sunspots area')

x = len([i for i in numberByDate.keys() if i < '1976-01-01'])
plt.plot([x, x], [0, 250], 'red')

ticksPerYear = []
for year in range(1900, 2016):
    cnt = 0
    for i in numberByDate.keys():
        if int(i[:4]) < year:
            cnt += 1
    ticksPerYear.append(cnt)

plt.xticks(compact(ticksPerYear), compact(range(1900, 2016)), rotation=-45)
plt.grid()
plt.legend()
plt.show()
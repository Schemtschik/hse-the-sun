#!/usr/bin/python3

import json
import random

import common

ANGLE_STEP = 5
AREA_STEP = 20
AREA_LIMIT = 3600


def getFrame(arr, angle_limit, area_limit):
    return [x for x in arr if not x.filtered and not x.old and
            (abs(x.records[0].longtitude) >= angle_limit - ANGLE_STEP) and (abs(x.records[0].longtitude) < angle_limit) and
            (x.area >= area_limit - AREA_STEP) and (x.area < area_limit)]


input_file = open("data/rgousfull.marked.json", "r")
output_file = open("data/rgousfull.filtered.json", "w")

lines = input_file.readlines()
records = []

for i in range(len(lines)):
    record = common.Record()
    record.__dict__.update(json.loads(lines[i]))
    records.append(record)

sunspots = common.getSunspotsFromRecords(records)
sunspots_count = len(sunspots)

random.shuffle(sunspots)

left = [x for x in sunspots if x.records[0].longtitude <= 0]
right = [x for x in sunspots if x.records[0].longtitude > 0]


def apply_filter():
    for j in range(1, AREA_LIMIT // AREA_STEP + 1):
        area_limit = AREA_STEP * j
        for i in range(1, 90 // ANGLE_STEP + 1):
            angle_limit = i * ANGLE_STEP
            count = max(0, len(getFrame(left, angle_limit, area_limit)) - len(getFrame(right, angle_limit, area_limit)))
            print(len(getFrame(left, angle_limit, area_limit)), ' ', len(getFrame(right, angle_limit, area_limit)))
            for x in getFrame(left, angle_limit, area_limit)[:count]:
                x.filtered = True
            print(len(getFrame(left, angle_limit, area_limit)), ' ', len(getFrame(right, angle_limit, area_limit)))


apply_filter()
AREA_STEP = 1
AREA_LIMIT = 100
apply_filter()

print("Calculated")

for x in left:
    if not x.filtered:
        for y in x.records:
            output_file.write(json.dumps(y.__dict__) + "\n")

for x in right:
    for y in x.records:
        output_file.write(json.dumps(y.__dict__) + "\n")

print("Saved")

#x = [sunspot.area for sunspot in sunspots]
#x.sort()
#plt.hist(x, bins=200, histtype='step')

#plt.show()

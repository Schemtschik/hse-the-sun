#!/usr/bin/python3

import bisect
import json
import math
import time

from datetime import datetime

import common

PERIOD_IN_DAYS = 10
PERIOD_IN_SECONDS = PERIOD_IN_DAYS * 24 * 60 * 60
TIME_INTERVAL = 60 * 60 * 12 # 12h


def get_longtitude_after_period(long):
    return long + 180 * PERIOD_IN_DAYS / 14


input_file = open("data/rgousfull.hsc.json", "r")

lines = input_file.readlines()
records = []


def timestamp_from_date(date_s):
    return time.mktime(datetime.strptime(date_s, '%Y-%m-%d %H:%M:%S').timetuple())


for i in range(len(lines)):
    record = common.Record()
    record.__dict__.update(json.loads(lines[i]))
    record.time = timestamp_from_date(record.time)
    records.append(record)

records.sort(key=lambda record: record.time)
times = [x.time for x in records]
sunspots = common.getSunspotsFromRecords(records)

def mark_and_get_accuracy(long_interval, lat_interval):
    def is_same(first_record, second_record):
        long_diff = abs(get_longtitude_after_period(first_record.longtitude) - second_record.longtitude)
        lat_diff = abs(first_record.latitude - second_record.latitude)
        return long_diff < long_interval and lat_diff < lat_interval and \
               (long_diff / long_interval)**2 + (lat_diff / lat_interval)**2 <= 1

    def get_score(first_record, second_record):
        r = math.sqrt(second_record.area) / 2
        lat_l = max(second_record.latitude - r, first_record.latitude - lat_interval)
        lat_r = min(second_record.latitude + r, first_record.latitude + lat_interval)
        long_l = max(second_record.longtitude - r, get_longtitude_after_period(first_record.longtitude) - long_interval)
        long_r = min(second_record.longtitude + r, get_longtitude_after_period(first_record.longtitude) + long_interval)
        return max(0, (lat_r - lat_l)) * max(0, (long_r - long_l))

    for record in records:
        record.marked = False

    long_live_sunspots = [sunspot for sunspot in sunspots if sunspot.records[-1].time - sunspot.records[0].time >= PERIOD_IN_SECONDS]

    score = 0
    count = 0
    for spot in long_live_sunspots:
        record = spot.records[0]
        left = bisect.bisect_left(times, record.time + PERIOD_IN_SECONDS - TIME_INTERVAL)
        right = bisect.bisect_left(times, record.time + PERIOD_IN_SECONDS + TIME_INTERVAL)
        for record2 in records[left:right]:
            if not record2.marked and is_same(record, record2):
                record2.marked = True
                score += get_score(record, record2)
                count += 1
                break

    return score / (lat_interval * long_interval)

temp = []
for i in range(1, 21):
    t = 1 + (i - 10) / 10
    long_interval = t * 15
    lat_interval = t * 8
    temp.append(mark_and_get_accuracy(long_interval, lat_interval))

import matplotlib.pyplot as plt
plt.plot(temp)
plt.show()
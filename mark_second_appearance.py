#!/usr/bin/python3

import bisect
import json
import time

from datetime import datetime

import common

LONG_INTERVAL = 15
LAT_INTERVAL = 8
PERIOD_IN_DAYS = 15
PERIOD_IN_SECONDS = PERIOD_IN_DAYS * 24 * 60 * 60
TIME_INTERVAL = 60 * 60 * 12 # 12h


def get_longtitude_after_period(long):
    return long + 180 * PERIOD_IN_DAYS / 14 - 360


input_file = open("data/rgousfull.hsc.json", "r")
output_file = open("data/rgousfull.marked.json", "w")

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

def is_same(first_record, second_record):
    long_diff = abs(get_longtitude_after_period(first_record.longtitude) - second_record.longtitude)
    lat_diff = abs(first_record.latitude - second_record.latitude)
    return long_diff < LONG_INTERVAL and lat_diff < LAT_INTERVAL and \
           (long_diff / LONG_INTERVAL)**2 + (lat_diff / LAT_INTERVAL)**2 <= 1

spots_to_check = [sunspot for sunspot in sunspots if sunspot.records[-1].longtitude <= (90 - 180 / 14)]

for spot in spots_to_check:
    record = spot.records[-1]
    left = bisect.bisect_left(times, record.time + PERIOD_IN_SECONDS - TIME_INTERVAL)
    right = bisect.bisect_left(times, record.time + PERIOD_IN_SECONDS + TIME_INTERVAL)
    for record2 in records[left:right]:
        if not record2.old and is_same(record, record2):
            record2.old = True
            record2.previous_id = record.group_id
            break

for record in records:
    output_file.write(json.dumps(record.__dict__) + "\n")

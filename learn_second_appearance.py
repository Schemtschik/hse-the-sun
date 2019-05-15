#!/usr/bin/python3

from datetime import datetime

import click
import bisect
import json
import math
import time
import common

import matplotlib.pyplot as plt

@click.command(help='Draws the graph of accuracy by ellipse size')
@click.argument('input_file', type=click.File('r'))
@click.option('--long', type=int, default=8, help='searching ellipse longitude semi-axis in degrees (8 by default)')
@click.option('--lat', type=int, default=5, help='searching ellipse latitude semi-axis in degrees (5 by default)')
@click.option('--time-interval', type=int, default=12, help='searching time semi-range in hours (12 by default)')
def run(input_file, long, lat, time_interval):
    TIME_INTERVAL = 60 * 60 * time_interval

    def get_longtitude_after_period(long):
        return long + 180 * PERIOD_IN_DAYS / 14

    def timestamp_from_date(date_s):
        return time.mktime(datetime.strptime(date_s, '%Y-%m-%d %H:%M:%S').timetuple())

    lines = input_file.readlines()
    records = []

    for i in range(len(lines)):
        record = common.Record()
        record.__dict__.update(json.loads(lines[i]))
        try:
            record.time = timestamp_from_date(record.time)
        except:
            continue
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


    for j in range(7, 14):
        PERIOD_IN_DAYS = j
        PERIOD_IN_SECONDS = PERIOD_IN_DAYS * 24 * 60 * 60
        temp = []
        for i in range(1, 21):
            t = 1 + (i - 10) / 10
            long_interval = t * long
            lat_interval = t * lat
            temp.append(mark_and_get_accuracy(long_interval, lat_interval))
        plt.plot(temp, label=str(j) + ' days')
        plt.legend()
    plt.xlabel('ellipse linear size coefficient')
    plt.ylabel('accuracy score')
    plt.xticks([i for i in range(20)], [str(1.15 + (i - 10) / 10)[:3] for i in range(20)], rotation=-45)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    run()
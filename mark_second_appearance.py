#!/usr/bin/python3

from datetime import datetime

import click
import bisect
import json
import time
import common

@click.command(help='Marks long live sunspots')
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
@click.option('--raw', is_flag=True, help='print just pairs "[old group id] [new group id]"')
@click.option('--long', type=int, default=8, help='searching ellipse longitude semi-axis in degrees (8 by default)')
@click.option('--lat', type=int, default=5, help='searching ellipse latitude semi-axis in degrees (5 by default)')
@click.option('--time-interval', type=int, default=12, help='searching time semi-range in hours (12 by default)')
@click.option('--period', type=int, default=15, help='searching period in days (15 by default)')
@click.option('--area-limit', type=int, default=200, help='minimal area of sunspot before disappearance (200 by default)')
def run(input_file, output_file, raw, long, lat, time_interval, period, area_limit):
    PERIOD_IN_SECONDS = period * 24 * 60 * 60
    TIME_INTERVAL = 60 * 60 * time_interval

    lines = input_file.readlines()
    records = []

    def get_longtitude_after_period(long):
        return long + 180 * period / 14 - 360

    def timestamp_from_date(date_s):
        return time.mktime(datetime.strptime(date_s, '%Y-%m-%d %H:%M:%S').timetuple())


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

    def is_same(first_record, second_record):
        long_diff = abs(get_longtitude_after_period(first_record.longtitude) - second_record.longtitude)
        lat_diff = abs(first_record.latitude - second_record.latitude)
        return long_diff < long and lat_diff < lat and \
               (long_diff / long) ** 2 + (lat_diff / lat) ** 2 <= 1

    spots_to_check = [sunspot for sunspot in sunspots if sunspot.records[-1].longtitude >= (90 - 180 / 14) and sunspot.area >= area_limit]

    for spot in spots_to_check:
        record = spot.records[-1]
        left = bisect.bisect_left(times, record.time + PERIOD_IN_SECONDS - TIME_INTERVAL)
        right = bisect.bisect_left(times, record.time + PERIOD_IN_SECONDS + TIME_INTERVAL)
        for record2 in records[left:right]:
            if not record2.old and is_same(record, record2):
                if raw:
                    output_file.write(str(record.group_id) + ' ' + str(record2.group_id) + '\n')
                record2.old = True
                record2.previous_id = record.group_id
                break

    if not raw:
        for record in records:
            output_file.write(json.dumps(record.__dict__) + "\n")


if __name__ == '__main__':
    run()
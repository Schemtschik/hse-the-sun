#!/usr/bin/python3

import json
import random
import click
import common


@click.command(help='Filters extra sunspots on the left, taking care of long live sunspots')
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
@click.option('--raw', is_flag=True, help='print ids of not filtered groups')
@click.option('--angle-step', type=int, default=5, help='angle frame size in degrees (5 by default)')
@click.option('--area-step-low', type=int, default=1, help='area frame size low (1 by default)')
@click.option('--area-limit-low', type=int, default=100, help='max area to process with low frame size (100 by default)')
@click.option('--area-step-high', type=int, default=20, help='area frame size high (20 by default)')
@click.option('--area-limit-high', type=int, default=3600, help='max area to process with high frame size (3600 by default)')
def run(input_file, output_file, raw, angle_step, area_step_low, area_limit_low, area_step_high, area_limit_high):
    AREA_STEP = area_step_high
    AREA_LIMIT = area_limit_high

    def getFrame(arr, angle_limit, area_limit):
        return [x for x in arr if not x.filtered and not x.old and
                (abs(x.records[0].longtitude) >= angle_limit - angle_step) and (abs(x.records[0].longtitude) < angle_limit) and
                (x.area >= area_limit - AREA_STEP) and (x.area < area_limit)]

    lines = input_file.readlines()
    records = []

    for i in range(len(lines)):
        record = common.Record()
        record.__dict__.update(json.loads(lines[i]))
        records.append(record)

    sunspots = common.getSunspotsFromRecords(records)

    random.shuffle(sunspots)

    left = [x for x in sunspots if x.records[0].longtitude <= 0]
    right = [x for x in sunspots if x.records[0].longtitude > 0]

    def apply_filter():
        for j in range(1, AREA_LIMIT // AREA_STEP + 1):
            area_limit = AREA_STEP * j
            for i in range(1, 90 // angle_step + 1):
                angle_limit = i * angle_step
                count = max(0, len(getFrame(left, angle_limit, area_limit)) - len(getFrame(right, angle_limit, area_limit)))
                for x in getFrame(left, angle_limit, area_limit)[:count]:
                    x.filtered = True

    apply_filter()
    AREA_STEP = area_step_low
    AREA_LIMIT = area_limit_low
    apply_filter()

    for x in left:
        if not x.filtered:
            if raw:
                output_file.write(str(x.id) + "\n")
            else:
                for y in x.records:
                    output_file.write(json.dumps(y.__dict__) + "\n")

    for x in right:
        if raw:
            output_file.write(str(x.id) + "\n")
        else:
            for y in x.records:
                output_file.write(json.dumps(y.__dict__) + "\n")


if __name__ == '__main__':
    run()
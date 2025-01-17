#!/usr/bin/python3

import click
import json
import common

def correct_len(string):
    string = str(int(string))
    return string if len(string) >= 2 else "0" + string


#"2013-09-21 16:00:00"
def formatDate(year, month, day, time):
    t = round(24 * float(time) / 1000.0)
    t = t if t < 24 else 0
    return year + '-' + correct_len(month) + '-' + correct_len(day) + ' ' + correct_len(str(t)) + ':00:00'

@click.command(help='Transforms raw data (format: data/rulesrgo.txt) to json structures implemented in common.py')
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
def run(input_file, output_file):
    for line in input_file.readlines():
        if len(line) < 74: continue

        record = common.Record()

        record.group_id = line[12:20]

        try:
            record.group_id = int(record.group_id)
        except:
            continue

        record.latiitude = float(line[63:68])
        record.longtitude = float(line[57:62])
        record.time = formatDate(line[:4], line[4:6], line[6:8], line[9:12])
        record.area = int(line[40:44])

        output_file.write(json.dumps(record.__dict__) + '\n')


if __name__ == '__main__':
    run()
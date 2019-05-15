#!/usr/bin/python3

import json

import common

main_file = open("data/rgofull.json", "r")
merging_file = open("data/rgofull.hsc.json", "r")

lines = main_file.readlines()
records = []

for i in range(len(lines)):
    record = common.Record()
    record.__dict__.update(json.loads(lines[i]))
    records.append(record)

lines = merging_file.readlines()

for i in range(len(lines)):
    record = common.Record()
    record.__dict__.update(json.loads(lines[i]))
    records[i].longtitude = record.longtitude

main_file.close()
output_file = open("data/rgofull.hsc.json", "w")

for record in records:
    output_file.write(json.dumps(record.__dict__) + '\n')

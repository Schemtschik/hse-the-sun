#!/usr/bin/python3

import json

import common

input_file = open("data/rgousfull.hsc.json", "r")
output_file = open("data/rgousfull.marked.json", "w")

lines = input_file.readlines()
records = []

for i in range(len(lines)):
    record = common.Record()
    record.__dict__.update(json.loads(lines[i]))
    records.append(record)

sunspots = common.getSunspotsFromRecords(records)
sunspots_count = len(sunspots)


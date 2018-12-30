#!/usr/bin/python3

import json

import common

input_file = open("data/rgofull.hcs.json", "r")
output_file = open("data/rgofull.filtered.json", "w")

lines = input_file.readlines()
records = []

for i in range(len(lines)):
    record = common.Record()
    record.__dict__.update(json.loads(lines[i]))
    records.append(record)






#!/usr/bin/python3

import json
import astropy.units as u
from astropy.coordinates import SkyCoord
from sunpy.coordinates import frames

import common


input_file = open("data/rgousfull.json", "r")
output_file = open("data/rgousfull.hsc.json", "w")

lines = input_file.readlines()

last_time = ""

for i in range(len(lines)):
    record = common.Record()
    record.__dict__.update(json.loads(lines[i]))

    coord = SkyCoord(lat=record.latitude * u.deg, lon=record.longtitude * u.deg, obstime=record.time, frame=frames.HeliographicCarrington)
    record.longtitude = coord.transform_to(frames.HeliographicStonyhurst).lon.deg

    if record.time[:7] != last_time:
        last_time = record.time[:7]
        print(last_time)

    output_file.write(json.dumps(record.__dict__) + "\n")



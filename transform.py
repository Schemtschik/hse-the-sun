#!/usr/bin/python3

import json
import astropy.units as u
import click
import common

from astropy.coordinates import SkyCoord
from sunpy.coordinates import frames

@click.command(help='Transforms heliocentric coordinates to geocentric ones')
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
def run(input_file, output_file):
    lines = input_file.readlines()

    progress = 0

    for i in range(len(lines)):
        record = common.Record()
        record.__dict__.update(json.loads(lines[i]))

        coord = SkyCoord(
            lat=record.latitude * u.deg,
            lon=record.longtitude * u.deg,
            obstime=record.time,
            frame=frames.HeliographicCarrington)

        record.longtitude = coord.transform_to(frames.HeliographicStonyhurst).lon.deg

        percents_completed = i * 1000 // len(lines)
        if percents_completed != progress:
            progress = percents_completed
            print("Processing: " + str(progress / 10) + "%")

        output_file.write(json.dumps(record.__dict__) + "\n")

if __name__ == '__main__':
    run()
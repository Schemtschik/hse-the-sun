#!/usr/bin/python3

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
from sunpy.coordinates import frames, get_sunearth_distance
import astropy.units as u


def correct_len(string):
    string = str(int(string))
    return string if len(string) >= 2 else "0" + string


#"2013-09-21 16:00:00"
def formatDate(year, month, day, time):
    t = round(24 * float(time) / 1000.0)
    t = t if t < 24 else 0
    return year + '-' + correct_len(month) + '-' + correct_len(day) + ' ' + correct_len(str(t)) + ':00:00'

def parseLongtitude(line):
    lat_car = float(line[63:68])
    long_car = float(line[57:62])
    time = formatDate(line[:4], line[4:6], line[6:8], line[9:12])
    coord = SkyCoord(lat=lat_car*u.deg, lon=long_car*u.deg, obstime=time, frame=frames.HeliographicCarrington)
    return coord.transform_to(frames.HeliographicStonyhurst).lon.deg

input_file = open("data/rgofull.txt", "r")
cache_file = open("data/lat.txt", "w")

longtitudes = []
last_date = ''
for line in input_file.readlines():
    if len(line) < 74: continue
    if int(line[:4]) < 1900: continue

    if line[:6] != last_date:
        last_date = line[:6]
        print(last_date)

    new_long = parseLongtitude(line)
    cache_file.write(str(new_long) + '\n')
    longtitudes.append(parseLongtitude(line))


#x = [x for x in longtitudes]

#x.sort()
#plt.hist(x, bins=x, histtype='step')
#plt.show()

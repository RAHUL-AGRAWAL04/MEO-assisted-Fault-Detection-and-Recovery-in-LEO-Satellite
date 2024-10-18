from skyfield.api import EarthSatellite, load
from pytz import timezone
import math
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def get_xyz(name,line1,line2,date):
    ts = load.timescale()
    sat_name = name.split()
    # print(sat_name)
    satellite = EarthSatellite(line1, line2, name=sat_name[0])

    tz = timezone('Asia/Kolkata')
    time = tz.localize(datetime(date[0], date[1], date[2]))
    time = ts.utc(time)

    position = satellite.at(time)
    subpoint = position.subpoint()

    lon = subpoint.longitude.degrees
    lat = subpoint.latitude.degrees
    alt = subpoint.elevation.km

    return (lon,lat,alt,sat_name[-1])


def points_within_circle(center, points):
    within_circle = []
    for point in points:
        if point == center: continue
        distance = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2 + (point[2] - center[2])**2)
        within_circle.append([point[3],distance])
    
    within_circle.sort(key=lambda x:x[1])
    return [within_circle[0][0],within_circle[1][0],within_circle[2][0],within_circle[3][0]]

points = []
with open('input_tle.txt','r') as file:
    lines = file.readlines()


for i in range(1,len(lines),3):
    points.append(get_xyz(lines[i],lines[i+1],lines[i+2],[2024,10,18]))


isls = {}
for i in range(len(points)):
    links = points_within_circle(points[i],points) 
    isls[i] = links
    # print(isls)
    # break


isl_lines = []
for i in isls:
    isl_lines.append(f'{i} {isls[i][0]}\n')
    isl_lines.append(f'{i} {isls[i][1]}\n')
    isl_lines.append(f'{i} {isls[i][2]}\n')
    isl_lines.append(f'{i} {isls[i][3]}\n')


with open('output/isl.txt','w') as file:
    file.writelines(isl_lines)
        
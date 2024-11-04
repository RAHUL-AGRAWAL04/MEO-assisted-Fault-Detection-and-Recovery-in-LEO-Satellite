from skyfield.api import EarthSatellite, load
from pytz import timezone
import math
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def compute_geo_angle(A, B, center):
    # Translate points based on custom center (center_lat, center_lon)
    v1x, v1y = A[0] - center[o], A[1] - center[1]
    v2x, v2y = B[0] - center[o], B[1] - center[1]
    
    # Calculate dot product and magnitudes of vectors
    dot_product = v1x * v2x + v1y * v2y
    magnitude_v1 = math.sqrt(v1x**2 + v1y**2)
    magnitude_v2 = math.sqrt(v2x**2 + v2y**2)
    
    # Calculate the cosine of the angle
    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
    
    # Ensure cos_angle is within the valid range due to potential floating-point precision errors
    cos_angle = min(1, max(-1, cos_angle))
    
    # Compute the angle in radians and convert to degrees
    angle_radians = math.acos(cos_angle)
    angle_degrees = math.degrees(angle_radians)
    
    return angle_degrees

def compute_angle_with_x_axis(lat, lon, center_lat, center_lon):
    # Translate point based on custom center (center_lat, center_lon)
    # print(type(lat),type(center_lat),type(lon), type(center_lon))
    dx = lon - center_lon  # Change in longitude (X-axis direction)
    dy = lat - center_lat  # Change in latitude (Y-axis direction)

    
    # Calculate the angle in radians between the point and the X-axis (longitude)
    angle_radians = math.atan2(dy, dx)  # atan2 considers the sign of both dx and dy to determine the quadrant
    angle_degrees = math.degrees(angle_radians)  # Convert to degrees
    
    # Ensure the angle is within the range [0, 360] degrees
    if angle_degrees < 0:
        angle_degrees += 360
    
    return angle_degrees




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
    # print(sat_name[-1], 'sat name') #all ok
    return (lon,lat,alt,sat_name[-1])


def points_within_circle(center, points, isls_count):
    within_circle = []
    for point in points:
        if point == center: continue
        distance = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2  + (point[2] - center[2])**2)
        within_circle.append([point,distance])
    
    within_circle.sort(key=lambda x:x[1])

    # isl = [within_circle[0][0],within_circle[1][0],within_circle[2][0],within_circle[3][0]]
    isl = isls_count[center[3]]

    e,w,n,s = False,False,False,False
    if isl[0] != -1: e = True
    if isl[1] != -1: w = True
    if isl[2] != -1: n = True
    if isl[3] != -1: s = True
    # print(e,w,n,s)
    for i in  range(len(within_circle)):
        angle = compute_angle_with_x_axis(within_circle[i][0][0],within_circle[i][0][1],center[0],center[1])
        # print('angle = ',angle,'node=',within_circle[i][0][3])

        #east
        if ((angle>=0 and angle <45) or (angle>=315 and angle <=360)) and e == False: 
            if isls_count[within_circle[i][0][3]][1] != -1 and center[3] != isls_count[within_circle[i][0][3]][1]: continue
            e = True
            # print(within_circle[i][0][3], 'east')
            isl[0] = within_circle[i][0][3]
        
        #west
        if (angle>=135 and angle <225) and w == False: 
            if isls_count[within_circle[i][0][3]][0] != -1 and center[3] != isls_count[within_circle[i][0][3]][0]: continue
            w = True
            # print(within_circle[i][0][3], 'west')
            isl[1] = within_circle[i][0][3]
        
        #north
        if (angle>=45 and angle <135) and n == False: 
            # print(isls_count[within_circle[i][0][3]][3])
            if isls_count[within_circle[i][0][3]][3] != -1 and center[3] != isls_count[within_circle[i][0][3]][3]: continue
            n = True
            # print(within_circle[i][0][3], 'north')
            isl[2] = within_circle[i][0][3]
        
        #south
        if (angle>=225 and angle <315) and s == False: 
            if isls_count[within_circle[i][0][3]][2] != -1 and center[3] != isls_count[within_circle[i][0][3]][2]: continue
            s = True
            # print(within_circle[i][0][3], 'south')
            isl[3] = within_circle[i][0][3]
        
        if e==True and w==True and n==True and s==True: break

    # print(isl)

    return isl

def get_east(center, points, isls_count):
    within_circle = []
    for point in points:
        if point == center: continue
        distance = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2  + (point[2] - center[2])**2)
        within_circle.append([point,distance])
    
    within_circle.sort(key=lambda x:x[1])

    isl = isls_count[center[3]]
    e=False
    if isl[0] != -1: e = True

    # print(e,w,n,s)
    for j in range(4):
        for i in  range(len(within_circle)):
            angle = compute_angle_with_x_axis(within_circle[i][0][0],within_circle[i][0][1],center[0],center[1])
            #east
            if ((angle>=0 and angle <45+45*j) or (angle>=315 - 45*j and angle <=360)) and e == False: 
                if (isls_count[within_circle[i][0][3]][1] != -1 and center[3] != isls_count[within_circle[i][0][3]][1]) or (within_circle[i][0][3] in isl): continue
                e = True
                # print(within_circle[i][0][3], 'get_east')
                isl[0] = within_circle[i][0][3]
                break
    return isl


def get_west(center, points, isls_count):
    within_circle = []
    for point in points:
        if point == center: continue
        distance = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2  + (point[2] - center[2])**2)
        within_circle.append([point,distance])
    
    within_circle.sort(key=lambda x:x[1])

    isl = isls_count[center[3]]
    w = False
    if isl[1] != -1: w = True
    # print(e,w,n,s)
    for j in range(4):
        for i in  range(len(within_circle)):
            angle = compute_angle_with_x_axis(within_circle[i][0][0],within_circle[i][0][1],center[0],center[1])
            #west
            if (angle>=135 - 45*j  and angle <225 + 45*j) and w == False: 
                if (isls_count[within_circle[i][0][3]][0] != -1 and center[3] != isls_count[within_circle[i][0][3]][0]) or (within_circle[i][0][3] in isl): continue
                w = True
                # print(within_circle[i][0][3], 'get_west')
                isl[1] = within_circle[i][0][3]
                break
    return isl

def get_north(center, points, isls_count):
    within_circle = []
    for point in points:
        if point == center: continue
        distance = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2  + (point[2] - center[2])**2)
        within_circle.append([point,distance])
    
    within_circle.sort(key=lambda x:x[1])

    isl = isls_count[center[3]]
    n = False
    if isl[2] != -1: n = True
    # print(e,w,n,s)
    for j in range(4):
        for i in  range(len(within_circle)):
            angle = compute_angle_with_x_axis(within_circle[i][0][0],within_circle[i][0][1],center[0],center[1])
                    
            #north
            if (angle>=(360-45*j)%360 and angle <180 + 45*j) and n == False: 
                # print(isls_count[within_circle[i][0][3]][3])
                if (isls_count[within_circle[i][0][3]][3] != -1 and center[3] != isls_count[within_circle[i][0][3]][3]) or (within_circle[i][0][3] in isl): continue
                n = True
                # print(within_circle[i][0][3], 'get_north')
                isl[2] = within_circle[i][0][3]
                break

    return isl


def get_south(center, points, isls_count):
    within_circle = []
    for point in points:
        if point == center: continue
        distance = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2  + (point[2] - center[2])**2)
        within_circle.append([point,distance])
    
    within_circle.sort(key=lambda x:x[1])
    isl = isls_count[center[3]]

    s = False
    if isl[3] != -1: s = True
    # print(e,w,n,s)
    for i in  range(len(within_circle)):
        angle = compute_angle_with_x_axis(within_circle[i][0][0],within_circle[i][0][1],center[0],center[1])
        #south
        if (angle<=(360+45*j)%360 and angle > 180-45*j) and s == False: 
            if (isls_count[within_circle[i][0][3]][2] != -1 and center[3] != isls_count[within_circle[i][0][3]][2]) or (within_circle[i][0][3] in isl): continue
            s = True
            # print(within_circle[i][0][3], 'get_south')
            isl[3] = within_circle[i][0][3]

    # print(isl)
    return isl





points = []
with open('output/MEO-annotted.txt','r') as file:
    lines = file.readlines()


for i in range(1,len(lines),3):
    points.append(get_xyz(lines[i],lines[i+1],lines[i+2],[2024,10,18]))


isls_count = {}
flags = []
for i in range(len(points)):
    isls_count[str(i+636)] = [-1,-1,-1,-1] # 636 is total LEO sate count. modify accordingly. if processing LEO keep it as 0

# print(isls_count.keys())
for i in range(len(points)):
    print(i)
    links = points_within_circle(points[i],points,isls_count)

    # print(links[0][3])
    # print(isls_count[links[0][3]])
    # print(isls_count[links[0][3]][1])

    #east Link
    try:
        isls_count[links[0]][1] =  str(i+636)
        isls_count[str(i)][0] = links[0]
    except:pass
    
    #west link
    try:
        isls_count[links[1]][0] = str(i+636)
        isls_count[str(i)][1] = links[1]
    except:pass
    
    #north link
    try:
        isls_count[links[2]][3] = str(i+636)
        isls_count[str(i)][2] = links[2]
    except:pass
    
    
    #south link
    try:
        isls_count[links[3]][2] = str(i+636)
        isls_count[str(i)][3] = links[3]
    except:pass
    


isl_lines = []
for i in isls_count:
    for j in range(4):
        if isls_count[i][j] == -1 and j==0: 
            e = get_east(points[int(i)-636],points,isls_count)
            isls_count[i][j] = e[0]
            isls_count[e[j]][1] =  i

        if isls_count[i][j] == -1 and j==1: 
            e = get_west(points[int(i)-636],points,isls_count)
            # print('e= ',e)
            isls_count[i][j] = e[1]
            isls_count[e[j]][0] =  i

        if isls_count[i][j] == -1 and j==2: 
            e = get_north(points[int(i)-636],points,isls_count)
            isls_count[i][j] = e[2]
            isls_count[e[j]][3] =  i

        if isls_count[i][j] == -1 and j==3: 
            e = get_south(points[int(i)-636],points,isls_count)
            isls_count[i][j] = e[3]
            isls_count[e[j]][2] =  i

        if f'{i} {isls_count[i][j]}\n' in isl_lines or f'{isls_count[i][j]} {i}\n' in isl_lines: continue
        isl_lines.append(f'{i} {isls_count[i][j]}\n')

isl_lines.insert(0,str(len(isl_lines))+'\n')
with open('output/isl-meo.txt','w') as file:
    file.writelines(isl_lines)
        
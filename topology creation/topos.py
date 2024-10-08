import numpy as np
import pandas as pd
from skyfield.api import Topos, load, EarthSatellite
from skyfield.api import wgs84
from datetime import datetime
import math

# Constants
GRAVITATIONAL_CONSTANT = 398600.4418  # Earth's gravitational parameter in km^3/s^2
EARTH_RADIUS = 6378.1  # Earth's radius in kilometers

# Generate TLE for Satellites
def generate_tle(satellite_name, satellite_id, epoch, inclination, raan, ecc, arg_per, mean_anomaly, altitude_km):
    # Calculate the semi-major axis
    semi_major_axis = EARTH_RADIUS + altitude_km  # in km
    
    # Compute mean motion (radians per second)
    mean_motion_rad_sec = math.sqrt(GRAVITATIONAL_CONSTANT / semi_major_axis**3)
    
    # Convert mean motion to revolutions per day
    mean_motion_rev_day = mean_motion_rad_sec * 86400 / (2 * np.pi)
    
    tle1 = f'1 {satellite_id:05d}U {epoch.strftime("%Y%m%d")} 00000A   0.00000000  00000-0  00000-0 0  9999'
    tle2 = f"2 {satellite_id:05d} {inclination:.4f} {raan:.4f} {ecc:.7f} {arg_per:.4f} {mean_anomaly:.4f} {mean_motion_rev_day:.8f}00000"
    return tle1, tle2

# Save TLE file
def save_tle_file(tle_data, filename):
    with open(filename, 'w') as f:
        for tle in tle_data:
            f.write(tle[0] + '\n')
            f.write(tle[1] + '\n')

# Generate User Terminal Positions
def generate_user_terminal_positions(num_users, lat_range, lon_range):
    lats = np.random.uniform(lat_range[0], lat_range[1], num_users)
    lons = np.random.uniform(lon_range[0], lon_range[1], num_users)
    return pd.DataFrame({'Latitude': lats, 'Longitude': lons})

# Generate Gateway Positions
def generate_gateway_positions(num_gateways, lat_range, lon_range):
    lats = np.random.uniform(lat_range[0], lat_range[1], num_gateways)
    lons = np.random.uniform(lon_range[0], lon_range[1], num_gateways)
    return pd.DataFrame({'Latitude': lats, 'Longitude': lons})

# Generate Inter-Satellite Links (ISL)
def generate_isl_links(satellites, range_threshold_km):
    isl_links = []
    for i, sat1 in enumerate(satellites):
        for j, sat2 in enumerate(satellites):
            if i < j:
                distance = np.linalg.norm(np.array([satellites['x'][i], satellites['y'][i], satellites['z'][i]]) - np.array([satellites['x'][j], satellites['y'][j], satellites['z'][j]]))
                if distance < range_threshold_km * 1000:
                    isl_links.append((sat1['id'], sat2['id']))
    return pd.DataFrame(isl_links, columns=['Satellite1', 'Satellite2'])

# Main function to generate LEO and MEO constellation
def generate_leo_meo_constellation(num_leo, num_meo, num_users, num_gateways, filename_prefix):
    ts = load.timescale()

    # Satellite Parameters for LEO and MEO
    epoch = datetime.utcnow()
    leo_inclination = 53.0  # Example inclination for LEO
    meo_inclination = 10.0  # Example inclination for MEO
    ecc = 0.0001  # Eccentricity (almost circular orbit)
    arg_per = 0.0  # Argument of Perigee
    mean_anomaly = 0.0

    # Altitudes for LEO and MEO
    leo_altitude_km = 1200  # Example LEO altitude in km
    meo_altitude_km = 20000  # Example MEO altitude in km

    # Generate LEO Satellite TLEs
    leo_tle_data = []
    leo_satellites = []
    for i in range(num_leo):
        tle1, tle2 = generate_tle(f"LEO_Sat_{i}", 10000 + i, epoch, leo_inclination, i * 5, ecc, arg_per, mean_anomaly, leo_altitude_km)
        leo_tle_data.append((tle1, tle2))
        sat = EarthSatellite(tle1, tle2, f"LEO_Sat_{i}", ts)
        leo_satellites.append(sat)

    # Save LEO TLE file
    save_tle_file(leo_tle_data, f'{filename_prefix}_leo_satellites.tle')

    # Generate MEO Satellite TLEs
    meo_tle_data = []
    meo_satellites = []
    for i in range(num_meo):
        tle1, tle2 = generate_tle(f"MEO_Sat_{i}", 20000 + i, epoch, meo_inclination, i * 10, ecc, arg_per, mean_anomaly, meo_altitude_km)
        meo_tle_data.append((tle1, tle2))
        sat = EarthSatellite(tle1, tle2, f"MEO_Sat_{i}", ts)
        meo_satellites.append(sat)

    # Save MEO TLE file
    save_tle_file(meo_tle_data, f'{filename_prefix}_meo_satellites.tle')

    # Generate User Terminal Positions (Shared by LEO and MEO)
    user_terminal_positions = generate_user_terminal_positions(num_users, lat_range=(-60, 60), lon_range=(-180, 180))
    user_terminal_positions.to_csv(f'{filename_prefix}_user_terminals.csv', index=False)

    # Generate Gateway Positions (Shared by LEO and MEO)
    gateway_positions = generate_gateway_positions(num_gateways, lat_range=(-60, 60), lon_range=(-180, 180))
    gateway_positions.to_csv(f'{filename_prefix}_gateways.csv', index=False)

    # Generate ISL Links for LEO and MEO
    all_satellites = []
    for sat in leo_satellites + meo_satellites:
        geocentric = sat.at(ts.now())
        lat, lon = wgs84.latlon_of(geocentric)
        all_satellites.append({
            'id': sat.name,
            'x': geocentric.position.m[0],
            'y': geocentric.position.m[1],
            'z': geocentric.position.m[2],
            'lat': lat.degrees,
            'lon': lon.degrees
        })

    satellite_positions = pd.DataFrame(all_satellites)
    # print(satellite_positions['x'][0])
    isl_links = generate_isl_links(satellite_positions, range_threshold_km=1000)  # 1000 km ISL range threshold
    isl_links.to_csv(f'{filename_prefix}_isl_links.csv', index=False)

    print(f"LEO and MEO constellation generated. Files saved with prefix '{filename_prefix}'.")

# Example usage
generate_leo_meo_constellation(num_leo=10, num_meo=5, num_users=100, num_gateways=10, filename_prefix='leo_meo_constellation')

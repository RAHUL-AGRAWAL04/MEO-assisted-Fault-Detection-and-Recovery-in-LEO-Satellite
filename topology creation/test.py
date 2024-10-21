# import math

# '''
# A = lat1,lon1
# B = lat2,lon2
# C = Clat,Clon
# '''
# def compute_geo_angle(A, B, center):
#     # Translate points based on custom center (center_lat, center_lon)
#     v1x, v1y = A[0] - center[o], A[1] - center[1]
#     v2x, v2y = B[0] - center[o], B[1] - center[1]
    
#     # Calculate dot product and magnitudes of vectors
#     dot_product = v1x * v2x + v1y * v2y
#     magnitude_v1 = math.sqrt(v1x**2 + v1y**2)
#     magnitude_v2 = math.sqrt(v2x**2 + v2y**2)
    
#     # Calculate the cosine of the angle
#     cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
    
#     # Ensure cos_angle is within the valid range due to potential floating-point precision errors
#     cos_angle = min(1, max(-1, cos_angle))
    
#     # Compute the angle in radians and convert to degrees
#     angle_radians = math.acos(cos_angle)
#     angle_degrees = math.degrees(angle_radians)
    
#     return angle_degrees

# # Example usage (geographic coordinates)
# A = [51.5074, -0.1278]  # London (Latitude, Longitude)
# B = [40.7128, -74.0060] # New York (Latitude, Longitude)
# center = [0, 0]  # Custom center at the Equator and Prime Meridian

# angle = compute_geo_angle(lat1, lon1, lat2, lon2, center_lat, center_lon)
# print(f"The angle between the geographic coordinates is {angle:.2f} degrees.")




import math

def compute_angle_with_x_axis(lat, lon, center_lat, center_lon):
    # Translate point based on custom center (center_lat, center_lon)
    dx = lon - center_lon  # Change in longitude (X-axis direction)
    dy = lat - center_lat  # Change in latitude (Y-axis direction)
    
    # Calculate the angle in radians between the point and the X-axis (longitude)
    angle_radians = math.atan2(dy, dx)  # atan2 considers the sign of both dx and dy to determine the quadrant
    angle_degrees = math.degrees(angle_radians)  # Convert to degrees
    
    # Ensure the angle is within the range [0, 360] degrees
    if angle_degrees < 0:
        angle_degrees += 360
    
    return angle_degrees

# Example usage (geographic coordinates)
lat, lon = 51.5074, -0.1278  # London (Latitude, Longitude)
center_lat, center_lon = 0, 0  # Custom center at the Equator and Prime Meridian

angle = compute_angle_with_x_axis(lat, lon, center_lat, center_lon)
print(f"The angle between the geographic point and the X-axis is {angle:.2f} degrees.")

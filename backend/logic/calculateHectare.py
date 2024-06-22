# Calculate the area in square meters (assuming the coordinates are in degrees and on a spherical earth model)
# Using the approximate value for radius of the Earth in meters
from shapely.geometry import shape
from pyproj import Proj, transform
from shapely.geometry import Polygon

def calculate_hectares_from_coordinates(coordinates):
    # Create a polygon from the coordinates
    polygon = Polygon(coordinates)
    
    
    # Define the projection: WGS84 to UTM
    proj_wgs84 = Proj(init='epsg:4326')
    proj_utm = Proj(proj='utm', zone=33, ellps='WGS84')

    # Transform coordinates to UTM
    utm_polygon = Polygon([transform(proj_wgs84, proj_utm, x, y) for x, y in polygon.exterior.coords])
    
    # Calculate area in square meters
    area_sq_meters = utm_polygon.area
    
    # Convert to hectares (1 hectare = 10,000 square meters)
    area_hectares = area_sq_meters / 10000
    
    return area_hectares

# # Example usage:
# coordinates = [
#     (34.0, -118.2), 
#     (34.0, -118.0), 
#     (34.2, -118.0), 
#     (34.2, -118.2), 
#     (34.0, -118.2)
# ]

# area_hectares = calculate_hectares_from_coordinates(coordinates)
# print(f"Area in hectares: {area_hectares}")

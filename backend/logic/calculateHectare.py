from shapely.geometry import Polygon
from shapely.ops import transform as shapely_transform
from pyproj import Proj, Transformer

def calculate_hectares_from_coordinates(coordinates):
    try:
        # Create a polygon from the coordinates
        polygon = Polygon(coordinates)
        
        # Ensure the polygon is valid
        if not polygon.is_valid:
            raise ValueError("Invalid polygon geometry.")
        
        # Determine the UTM zone based on the longitude of the first point
        lon = coordinates[0][0]
        zone = int((lon + 180) // 6) + 1
        
        # Define the projection: WGS84 to UTM
        proj_wgs84 = Proj('epsg:4326')
        proj_utm = Proj(proj='utm', zone=zone, ellps='WGS84')

        # Use Transformer instead of transform function
        transformer = Transformer.from_proj(proj_wgs84, proj_utm)

        # Transform coordinates to UTM using the transformer
        utm_polygon = shapely_transform(transformer.transform, polygon)
        
        # Calculate area in square meters
        area_sq_meters = utm_polygon.area
        
        # Convert to hectares (1 hectare = 10,000 square meters)
        area_hectares = area_sq_meters / 10000
        
        return area_hectares
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return float('nan')

import rasterio
from rasterio.windows import from_bounds
import numpy as np

# Load the real satellite raster ONCE when server starts
# We open it in read mode. We will read windows from it later.
raster = rasterio.open(r"data/data.tif")


def get_radiance(lat: float, lon: float):
    """Returns radiance for given coordinates."""
    try:
        row, col = raster.index(lon, lat)
        # Read a 1x1 window
        window = rasterio.windows.Window(col, row, 1, 1)
        value = raster.read(1, window=window)
        return float(value[0, 0])
    except Exception:
        return None


def find_nearest_dark_spot(lat: float, lon: float, search_km=200, num_spots=5):
    """
    Searches within a square grid around the user for the lowest radiance pixels.
    Returns a list of the top `num_spots` distinct dark spots.
    """

    print(f"🔍 Searching for {num_spots} dark spots around {lat}, {lon} with radius {search_km}km...")

    degree_offset = search_km / 111.0
    
    left = lon - degree_offset
    bottom = lat - degree_offset
    right = lon + degree_offset
    top = lat + degree_offset

    try:
        window = from_bounds(left, bottom, right, top, raster.transform)
        data = raster.read(1, window=window)
        
        if data.size == 0:
            return []

        # Mask invalid data
        masked_data = np.ma.masked_less(data, 0)
        
        if masked_data.count() == 0:
             return []

        found_spots = []
        
        # Calculate mask radius in pixels to ensure separation relative to search radius
        # We want separation to be roughly 25% of the search radius.
        separation_km = search_km / 4.0
        
        # Resolution is in degrees per pixel.
        # raster.res[0] is width of pixel in degrees (assuming WGS84)
        # 1 degree ~ 111 km.
        pixel_res_deg = raster.res[0]
        separation_deg = separation_km / 111.0
        mask_radius = int(separation_deg / pixel_res_deg)
        
        # Ensure at least 1 pixel mask
        mask_radius = max(1, mask_radius)
        
        print(f"📏 Calculated mask radius: {mask_radius} pixels ({separation_km:.1f}km) for search radius {search_km}km")

        # Copy the masked data so we can modify the mask
        working_data = masked_data.copy()

        for _ in range(num_spots):
            if working_data.count() == 0:
                break
                
            min_val = working_data.min()
            min_idx = np.unravel_index(np.argmin(working_data), working_data.shape)
            row_rel, col_rel = min_idx
            
            # Convert to global coords
            row_global = window.row_off + row_rel
            col_global = window.col_off + col_rel
            lon_res, lat_res = raster.xy(row_global, col_global)
            
            found_spots.append({
                "lat": float(lat_res),
                "lon": float(lon_res),
                "value": float(min_val)
            })
            
            # Mask out the area around this spot in working_data
            r_min = max(0, row_rel - mask_radius)
            r_max = min(working_data.shape[0], row_rel + mask_radius + 1)
            c_min = max(0, col_rel - mask_radius)
            c_max = min(working_data.shape[1], col_rel + mask_radius + 1)
            
            working_data[r_min:r_max, c_min:c_max] = np.ma.masked

        print(f"➡️ Found {len(found_spots)} spots.")
        return found_spots

    except Exception as e:
        print(f"❌ Error searching for dark spot: {e}")
        return []

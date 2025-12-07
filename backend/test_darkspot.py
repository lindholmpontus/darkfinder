from darkspot import find_nearest_dark_spot
import time

def test_find_nearest_dark_spot():
    # Stockholm coordinates roughly
    lat = 59.3293
    lon = 18.0686
    
    print(f"Testing find_nearest_dark_spot for {lat}, {lon}...")
    
    start_time = time.time()
    result = find_nearest_dark_spot(lat, lon, search_km=50)
    end_time = time.time()
    
    print(f"Result: {result}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    if result and isinstance(result, list) and len(result) > 0:
        print(f"✅ Test Passed: Found {len(result)} dark spots.")
        for i, spot in enumerate(result):
            print(f"  Spot {i+1}: {spot}")
    else:
        print("⚠️ Test Result: No spots found or invalid format.")

if __name__ == "__main__":
    test_find_nearest_dark_spot()

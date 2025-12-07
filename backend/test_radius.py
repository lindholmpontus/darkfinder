from darkspot import find_nearest_dark_spot
import time

def test_radius_logic():
    # Stockholm coordinates
    lat = 59.3293
    lon = 18.0686
    
    print("--- Testing Small Radius (10km) ---")
    start_time = time.time()
    spots_small = find_nearest_dark_spot(lat, lon, search_km=10)
    print(f"Time: {time.time() - start_time:.4f}s")
    if spots_small:
        print(f"Found {len(spots_small)} spots.")
        print(f"First spot: {spots_small[0]}")
    else:
        print("No spots found (expected if area is too bright or small).")

    print("\n--- Testing Large Radius (200km) ---")
    start_time = time.time()
    spots_large = find_nearest_dark_spot(lat, lon, search_km=200)
    print(f"Time: {time.time() - start_time:.4f}s")
    if spots_large:
        print(f"Found {len(spots_large)} spots.")
        print(f"First spot: {spots_large[0]}")
    else:
        print("No spots found.")

    # Basic check: Large radius should likely find 'better' (lower value) or different spots
    if spots_small and spots_large:
        val_small = spots_small[0]['value']
        val_large = spots_large[0]['value']
        print(f"\nComparison: Small Radius Best Value: {val_small}, Large Radius Best Value: {val_large}")
        if val_large <= val_small:
             print("✅ Logic check passed: Larger radius found equal or better dark spot.")
        else:
             print("⚠️ Logic check: Larger radius found worse spot? (Unlikely but possible if small radius hit a local minimum).")

if __name__ == "__main__":
    test_radius_logic()

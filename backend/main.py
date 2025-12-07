from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from darkspot import find_nearest_dark_spot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Location(BaseModel):
    lat: float
    lon: float
    radius: int = 200


@app.post("/nearest-dark-spot")
def nearest_spot(location: Location):
    print("📩 Incoming request:", location)
    spots = find_nearest_dark_spot(location.lat, location.lon, search_km=location.radius)
    
    if not spots:
        print("❌ No dark spots found or error occurred.")
        raise HTTPException(status_code=404, detail="Could not find any dark spots nearby. You might be out of the map coverage.")
        
    print(f"📤 Sending response: {len(spots)} spots found")
    return spots

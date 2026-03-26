import pandas as pd
import googlemaps
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from get_coords import get_coords_for_address
from math import radians, sin, cos, sqrt, atan2


gmaps_api_key = os.getenv("Maps_API_KEY")
gmaps = googlemaps.Client(key=gmaps_api_key)



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app---1149b54e.base44.app",  
        "http://localhost:3000",              
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



shelters_file = r"shelters_ptk_with_coords.xlsx"
shelters_df = pd.read_excel(shelters_file, dtype=str)



# Function to calculate straight-line distance (great-circle distance) between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))




# Function to find the closest shelters to a user address
def find_closest_shelters(user_address: str, travel_mode='walking'):
    user_lat, user_lng = get_coords_for_address(user_address, gmaps)

    # Step 1: Calculate haversine distance to all shelters
    shelters_with_air_distance = []
    for _, row in shelters_df.iterrows():
        shelter_lat = row['latitude']
        shelter_lng = row['longitude']
        air_distance = haversine(user_lat, user_lng, float(shelter_lat), float(shelter_lng))
        shelters_with_air_distance.append((air_distance, row))

    # Step 2: Sort and keep the 15 closest by air distance
    shelters_with_air_distance.sort(key=lambda x: x[0])

    # Step 3: Calculate real directions only for the 15 closest
    closest_shelters = []
    for air_distance, row in shelters_with_air_distance:
        if len(closest_shelters) == 15:
            break
        shelter_lat = row['latitude']
        shelter_lng = row['longitude']

        directions_from_user_address = gmaps.directions(
            (user_lat, user_lng),
            (shelter_lat, shelter_lng),
            mode=travel_mode
        )

        distance_m = directions_from_user_address[0]['legs'][0]['distance']['value']
        duration_sec = directions_from_user_address[0]['legs'][0]['duration']['value']

        shelter_info = {
            "כתובת": row.get('כתובת'),
            "סוג מקלט": row.get('סוג מקלט'),
            "שם מקום": row.get('שם מקום'),
            "latitude": shelter_lat,
            "longitude": shelter_lng,
            "מרחק_קמ": round(distance_m / 1000, 2),
            "משך_דקות": round(duration_sec / 60, 2)
        }

        closest_shelters.append(shelter_info)

    # Step 4: Sort final list by real walking time
    sorted_shelters = sorted(closest_shelters, key=lambda x: x['משך_דקות'])
    return sorted_shelters




# API endpoint to find the closest shelters on the list page
@app.get("/shelters/find_closest/")
async def find_closest_shelters_api(
    user_address: str,
    travel_mode: str 
):
    
    """
    Find the closest shelters to the user address.
    
    Parameters:
    - user_address: The address of the user.
    - travel_mode: The mode of travel (default is 'walking').
    
    Returns:
    A list of the shelters sorted by proximity to the users address with their details.
    """

    try:
        shelters_sorted_by_proximity = find_closest_shelters(user_address, travel_mode)
        return shelters_sorted_by_proximity
    
    # using to raise massege with specific details if something goes wrong 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
"""if __name__ == "__main__":
    user_address = "זאב ברנדה 4, פתח תקווה"
    travel_mode = "walking"
    closest_shelters = find_closest_shelters(user_address, travel_mode)
    print(closest_shelters)"""
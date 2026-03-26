import pandas as pd
import googlemaps
import os
from dotenv import load_dotenv
load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("google_maps_api"))



def get_coords_for_address(address: str) -> tuple[float, float]:
    
    full_address = f"{address}, פתח תקווה, ישראל" 
    geocode_address = gmaps.geocode(full_address)

    location = geocode_address[0]['geometry']['location']
    return location['lat'], location['lng']



def add_coords_to_csv(input_file: str, output_file: str):

    try:
        df = pd.read_excel(input_file)

        #adding new columns for latitude and longitude
        df['latitude'] = None
        df['longitude'] = None

        for index, row in df.iterrows():
            address_to_geocode = row['כתובת']
            lat, lng = get_coords_for_address(address_to_geocode)
            if lat is not None and lng is not None:
                df.loc[index, 'latitude'] = lat
                df.loc[index, 'longitude'] = lng

        df.to_excel(output_file, index=False)

    except Exception as e:
        print(f"An error occurred: {e}")




if __name__ == "__main__":
    input_csv = r"C:\Users\מוטי\Desktop\מקלט עכשיו\יצירת האקסלים\shelters_ptk_with_coords1.xlsx"
    output_csv = r"C:\Users\מוטי\Desktop\מקלט עכשיו\יצירת האקסלים\shelters_ptk_with_coords.xlsx"
    add_coords_to_csv(input_csv, output_csv)
import pandas as pd
import googlemaps



def get_coords_for_address(address: str, gmaps_client) -> tuple[float, float]:
    
    full_address = f"{address}, פתח תקווה, ישראל" 
    geocode_address = gmaps_client.geocode(full_address)

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

        df.to_csv(output_file, encoding='utf-8-sig')

    except Exception as e:
        print(f"An error occurred: {e}")
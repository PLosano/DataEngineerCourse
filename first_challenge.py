import psycopg2
import requests
import json
from dotenv import dotenv_values
from datetime import datetime

# Function to obtain the data
def obtain_data(config, start_date, end_date):
    try:
        # Define the request parameters, including the API key and dates
        params = {'api_key': config["api_key"], 
                  'start_date': start_date,
                  'end_date': end_date}

        # Make the request to the API with the parameters
        api_response = requests.get(config["url_api"], params=params)

        if api_response.status_code == 200:
            return api_response.json()
        else:
            print(f"Request failed. Status code: {api_response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def insert_data_to_redshift(data, config):
    try:
        # Connect to Redshift
        conn = psycopg2.connect(
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"]
        )
        cur = conn.cursor()

        # Insert data into Redshift
        for entry in data["near_earth_objects"]:
            for asteroid in data["near_earth_objects"][entry]:
                # timestamp
                current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                cur.execute("""
                    INSERT INTO asteroid (id, neo_reference_id, name, nasa_jpl_url,
                                        absolute_magnitude_h, estimated_diameter_km_min,
                                        estimated_diameter_km_max, is_potentially_hazardous_asteroid,
                                        is_sentry_object, time_stamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (asteroid["id"], asteroid["neo_reference_id"], asteroid["name"],
                    asteroid["nasa_jpl_url"], asteroid["absolute_magnitude_h"],
                    asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                    asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                    asteroid["is_potentially_hazardous_asteroid"], asteroid["is_sentry_object"],
                    current_timestamp))
        conn.commit()
        print("Data inserted successfully.")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error inserting data: {e}")

# Load configuration from .env file
config = dotenv_values(".env")
start_date = '2024-03-07'
end_date = '2024-03-14'

# Obtain data from API
data = obtain_data(config, start_date, end_date)

if data:
    print("API Data:")
    print(json.dumps(data, indent=4))
    
    # Insert data into Redshift
    insert_data_to_redshift(data, config)
else:
    print("Could not get data from API.")

import requests
from dotenv import load_dotenv
from dotenv import dotenv_values

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

config = dotenv_values(".env")
start_date = '2023-02-20'
end_date = '2023-02-27'

data = obtain_data(config, start_date, end_date)

if data:
    print("API Data:")
    print(data)
else:
    print("Could not get data from API.")



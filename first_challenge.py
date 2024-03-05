import requests

# Function to obtain the data
def obtain_data(url, api_key, start_date, end_date):
    try:
        # Define the request parameters, including the API key and dates
        params = {'api_key': api_key, 
                  'start_date': start_date,
                  'end_date': end_date}

        # Make the request to the API with the parameters
        api_response = requests.get(url, params=params)

        if api_response.status_code == 200:
            return api_response.json()
        else:
            print(f"Request failed. Status code: {api_response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

url_api = "https://api.nasa.gov/neo/rest/v1/feed"
api_key = "Vf6Ex970rHCGrFjWtJffcRXHXWm8IHOaxwrythDm"
start_date = '2023-01-01'
end_date = '2023-01-07'

data = obtain_data(url_api, api_key, start_date, end_date)

if data:
    print("API Data:")
    print(data)
else:
    print("Could not get data from API.")



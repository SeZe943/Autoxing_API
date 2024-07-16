import requests

# Base URL for the API
base_url = 'http://192.168.2.145:8090'

# Endpoint to get the list of maps
mapss = f'{base_url}/maps'

# Fetch the list of maps
response = requests.get(mapss)

if response.status_code == 200:
    maps = response.json()
    if maps:
        # Assuming the first map in the list is the current map
        current_map_id = maps[0]['id']

        # Endpoint to get details of the current map
        map_details_endpoint = f'{base_url}/maps/{current_map_id}'

        # Fetch the details of the current map
        map_response = requests.get(map_details_endpoint)

        if map_response.status_code == 200:
            map_details = map_response.json()

            # Display the map details
            print("Map Name:", map_details['map_name'])
            print("Created Time:", map_details['create_time'])
            print("Image URL:", map_details['image_url'])
        else:
            print(f"Failed to get map details. Status code: {map_response.status_code}")
    else:
        print("No maps available.")
else:
    print(f"Failed to get maps list. Status code: {response.status_code}")

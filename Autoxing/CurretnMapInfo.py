import requests
import json


# Function to list maps
def Current_Map(base_url):
    url = f"{base_url}/chassis/current-map"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        MapDetail = response.json()
        return MapDetail
    else:
        print(f"Failed to retrieve maps. Status code: {response.status_code}")
        return []


# Base URL for the API
base_url = "http://192.168.2.148:8090"

# Retrieve and print maps
MapDetail = Current_Map(base_url)
print("Move Detail:", MapDetail)

if MapDetail:
    id = MapDetail.get('id')
    uid = MapDetail.get('uid')
    map_name = MapDetail.get('map_name')
    print("id:", id)
    print("uid:", uid)
    print("map name", map_name)
else:
    print("Move details could not be retrieved.")

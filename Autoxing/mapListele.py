import requests
import json


# Function to list maps
def list_maps(base_url):
    url = f"{base_url}/maps"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        maps = response.json()
        return maps
    else:
        print(f"Failed to retrieve maps. Status code: {response.status_code}")
        return []


# Base URL for the API
base_url = "http://192.168.2.148:8090//"


# Retrieve and print maps
maps = list_maps(base_url)
id = maps.post("id")
print("Maps:", maps)
print ("id", id)


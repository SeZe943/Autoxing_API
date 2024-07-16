import requests
import json


# Function to list maps
def Hostname(base_url):
    data = {"ip": "192.168.2.148"}
    data_json = json.dumps(data)
    url = f"{base_url}/hostnames/local.autoxing.com"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers, data=data_json)

    if response.status_code == 200:
        Host = response.json()
        return Host
    else:
        print(f"Failed to retrieve maps. Status code: {response.status_code}")
        return []


# Base URL for the API
base_url = "http://192.168.2.148:8090/"


# Retrieve and print maps
Host = Hostname(base_url)
print("Maps:", Host)

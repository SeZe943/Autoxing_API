import requests
import json


# Function to list maps
def Device_Info(base_url):
    url = f"{base_url}/device/info"

    response = requests.get(url)

    if response.status_code == 200:
        DeviceInfo = response.json()
        return DeviceInfo
    else:
        print(f"Failed to retrieve maps. Status code: {response.status_code}")
        return []


# Base URL for the API
base_url = "http://192.168.2.148:8090"
# Retrieve and print maps
DeviceInfo = Device_Info(base_url)
print("Device Info:", DeviceInfo)

if DeviceInfo:
    rosversion = DeviceInfo.get('rosversion')
    rosdistro = DeviceInfo.get('rosdistro')
    axbot_version = DeviceInfo.get('axbot_version')
    print("rosversion:", rosversion)
    print("rosdistro:", rosdistro)
    print("map axbot_version",axbot_version)
else:
    print("Move details could not be retrieved.")

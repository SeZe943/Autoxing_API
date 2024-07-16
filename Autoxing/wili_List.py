import requests


# Function to list Wifi
def Wifi_List(base_url):
    url = f"{base_url}/device/available_wifi"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        WifiList = response.json()
        return WifiList
    else:
        print(f"Failed to retrieve Detail. Status code: {response.status_code}")
        return []


# Base URL for the API
base_url = "http://192.168.2.145:8090"

# Retrieve and print maps
WifiList = Wifi_List(base_url)
print("Wifi List:", WifiList)

if WifiList:
    id = WifiList.get('ssid')
    uid = WifiList.get('bss')
    map_name = WifiList.get('rssi')
    print("id:", id)
    print("uid:", uid)
    print("map name", map_name)
else:
    print("Move details could not be retrieved.")



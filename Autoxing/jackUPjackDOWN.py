import time
import requests
import json

BASE_URL = "http://192.168.2.145:8090"
global move_id
def move_to_target(target , BASE_URL="http://192.168.2.145:8090"):
    # Define the target point
    data = {
        "type": "standard",
        "target_x": target[0],
        "target_y": target[1],
        "target_z": 0.0,
        "target_ori": 1.5708,
    }
    data_json = json.dumps(data)
    url = f'{BASE_URL}/chassis/moves'
    headers = {'Content-Type': 'application/json'}

    # Create the move
    response = requests.post(url, headers=headers, data=data_json)

    # Check if the move was created successfully
    if response.status_code == 201:
        response_data = response.json()
        move_id = response_data.get("id")
    else:
        print("Failed to create move. Status code:", response.status_code)
        return

    # Monitor the move status
    url = f"{BASE_URL}/chassis/moves/{move_id}"
    print("Go to Point ---> Move ID:", move_id)
    old_state = None

    while True:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            state = data.get("state")
            if state is not None:
                if state != old_state:
                    print("State:", state)
                    old_state = state
                if state == "succeeded" or state == "failed":
                    break  # Move completed or failed, exit the loop
            else:
                print("State not found.")
        else:
            print("An error occurred. Status code:", response.status_code)
        time.sleep(1)  # Retry every second


def jack_up():
    url = f"{BASE_URL}/services/jack_up"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Jack up command successful")
        time.sleep(10)
    else:
        print("Failed to execute jack up command. Status code:", response.status_code)

def jack_down():
    url = f"{BASE_URL}/services/jack_down"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Jack down command successful")

    else:
        print("Failed to execute jack down command. Status code:", response.status_code)


def get_move_detail():
    url = f"{BASE_URL}/chassis/moves/{move_id}"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve maps. Status code: {response.status_code}")
        return {}


# Example usage
# Step 1: Align with rack

# # Step 2: Jack up
jack_up()
time.sleep(10)
# # Step 3: Monitor jack state (optional, if required)

target = (0.0, 0.0)
move_to_target(target)

# Step 5: Jack down
jack_down()
time.sleep(10)

target2 = (0.0, 0.0)
move_to_target(target2)

move_detail = get_move_detail()

if move_detail:
    move_type = move_detail.get('type')
    current_x = move_detail.get('target_x')
    current_y = move_detail.get('target_y')
    print("Move Detail:", move_detail)
    print(f"Current Position: X={current_x}, Y={current_y}")
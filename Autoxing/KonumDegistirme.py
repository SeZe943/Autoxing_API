import time
import requests
import json


def move_to_target(target,ori, base_url="http://192.60.2.173:8090"):
    # Define the target point
    if ori == "ileri":
        ori = 1.5078
    elif ori == "geri":
        ori = -1.5078
    elif ori == "sag":
        ori = 0
    elif ori == "sol":
        ori = 3.14
    else:
        print("integer deger ya da string olarak 'ileri', 'geri', 'sag','sol' verileri giriniz")
    data = {
        "type": "standard",
        "target_x": target[0],
        "target_y": target[1],
        "target_z": 0.0,
        "target_ori": ori,


    }
    data_json = json.dumps(data)
    url = f'{base_url}/chassis/moves'
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
    url = f"{base_url}/chassis/moves/{move_id}"
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
# ileri =1.5078
# geri =-1.5078
# sag = 0
# sol = 3.14
# Example usage
target = (0.0, 0.0)
move_to_target(target, "ileri")
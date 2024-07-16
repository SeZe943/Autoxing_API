import math
import time
import requests
import json
import asyncio
import websockets
import json
import math


BASE_URL = "http://192.168.2.173:8090"

global move_id
def Konum_Degistirme(target, ori, base_url=BASE_URL):
    # Define the target point
    if ori == "ileri":
        ori = 1.5078
    elif ori == "geri":
        ori = -1.5078
    elif ori == "sag":
        ori = 0
    elif ori == "sol":
        ori = 3.14
    elif ori < 180:
        ori = (ori / 180) * math.pi
        ori =ori
    else:
        print("integer olarak 0 ile +180 arasında bir deger ya da string olarak 'ileri','geri','sag','sol' verileri giriniz")
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


def Move_Detail(base_url):
    url = f"{base_url}/chassis/moves/1124"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        MoveDetail = response.json()
        return MoveDetail
    else:
        print(f"Failed to retrieve maps. Status code: {response.status_code}")
        return []


async def get_robot_pose(base_url):
    async with websockets.connect(base_url) as websocket:
        subscribe_message = json.dumps({"enable_topic": "/tracked_pose"})
        await websocket.send(subscribe_message)


        while True:
            response = await websocket.recv()
            data = json.loads(response)
            if data.get("topic") == "/tracked_pose":
                pos = data.get("pos", [])
                ori = data.get("ori")
                print(f"Position: X={pos[0]}, Y={pos[1]}, Orientation={ori},")  # Add comma
                break


async def get_2_robot_pose(BASE_URL, BASE_URL2):
    tasks = [get_robot_pose(BASE_URL), get_robot_pose(BASE_URL2)]
    await asyncio.gather(*tasks)  # Wait for both tasks to finish



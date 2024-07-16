# import time
# import requests
# import json
#
# BASE_URL = "http://192.168.2.148:8090"
#
# def move_backward(speed, duration, base_url=BASE_URL):
#     # Define the backward move command
#     data = {
#         "topic": "/twist",
#         "linear_velocity": -speed,  # Negative speed for backward movement
#         "angular_velocity": 0
#     }
#     data_json = json.dumps(data)
#     url = f'{base_url}/ws/v2/topics'
#     headers = {'Content-Type': 'application/json'}
#
#     # Open a WebSocket connection and send the command
#     response = requests.post(url, headers=headers, data=data_json)
#
#     if response.status_code == 200:
#         print("Command sent successfully")
#     else:
#         print("Failed to send command. Status code:", response.status_code)
#         return
#
#     # Wait for the specified duration
#     time.sleep(duration)
#
#     # Stop the movement
#     stop_data = {
#         "topic": "/twist",
#         "linear_velocity": 0,
#         "angular_velocity": 0
#     }
#     stop_data_json = json.dumps(stop_data)
#     response = requests.post(url, headers=headers, data=stop_data_json)
#
#     if response.status_code == 200:
#         print("Stop command sent successfully")
#     else:
#         print("Failed to send stop command. Status code:", response.status_code)
#
# # Example usage
# move_backward(speed=0.5, duration=5)  # Move backward at speed 0.5 for 5 seconds

import asyncio
import websockets
import json

BASE_URL = "ws://192.168.2.148:8090/ws/v2/topics"


async def get_robot_pose(base_url=BASE_URL):
    async with websockets.connect(base_url) as websocket:
        # Subscribe to the /tracked_pose topic
        subscribe_message = json.dumps({"enable_topic": "/tracked_pose"})
        await websocket.send(subscribe_message)

        while True:
            response = await websocket.recv()
            data = json.loads(response)
            if data.get("topic") == "/tracked_pose":
                pos = data.get("pos", [])
                ori = data.get("ori")
                print(f"Position: X={pos[0]}, Y={pos[1]}, Orientation={ori}")


# Run the function
asyncio.get_event_loop().run_until_complete(get_robot_pose())

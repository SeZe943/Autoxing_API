import asyncio
import websockets
import json


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



async def get_2_robot_pose(BASE_URL, BASE_URL2):
    tasks = [get_robot_pose(BASE_URL), get_robot_pose(BASE_URL2)]
    await asyncio.gather(*tasks)  # Wait for both tasks to finish


# Run the function
BASE_URL = "ws://192.168.2.173:8090/ws/v2/topics"
BASE_URL2 = "ws://192.168.2.131:8090/ws/v2/topics"
#asyncio.run(get_2_robot_pose(BASE_URL, BASE_URL2))
asyncio.get_event_loop().run_until_complete(get_robot_pose(BASE_URL2))
# asyncio.run(main(BASE_URL, BASE_URL2))

# asyncio.get_event_loop().run_until_complete(get_robot_pose(BASE_URL))
# time.sleep(1)
# asyncio.get_event_loop().run_until_complete(get_robot_pose(BASE_URL2))
# time.sleep(1)

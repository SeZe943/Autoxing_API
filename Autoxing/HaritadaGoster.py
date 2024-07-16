import json
import requests
import websockets
import asyncio
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

# Base URL for the API
base_url = 'http://192.168.2.173:8090'

def get_maps():
    maps_endpoint = f'{base_url}/maps'
    response = requests.get(maps_endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get maps list. Status code: {response.status_code}")
        return None

def get_map_details(map_id):
    map_details_endpoint = f'{base_url}/maps/{map_id}'
    response = requests.get(map_details_endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get map details. Status code: {response.status_code}")
        return None

# def get_tracked_pose():
#     pose_endpoint = f'{base_url}/tracked_pose'
#     response = requests.get(pose_endpoint)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Failed to get tracked pose. Status code: {response.status_code}")
#         return None

async def get_robot_pose(base_url="http://192.168.2.173:8090"):
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


class MapWidget(QWidget):
    def __init__(self, map_image, robot_pos):
        super().__init__()
        self.map_image = map_image
        self.robot_pos = robot_pos
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.plot_map()

    def plot_map(self):
        ax = self.canvas.figure.add_subplot(111)
        ax.imshow(self.map_image, cmap='gray')
        ax.plot(self.robot_pos[0], self.robot_pos[1], 'ro')  # Robot's position in red
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self, map_image, robot_pos):
        super().__init__()
        self.setWindowTitle('Robot Position on Map')
        self.setGeometry(100, 100, 800, 600)

        self.map_widget = MapWidget(map_image, robot_pos)
        self.setCentralWidget(self.map_widget)


async def main():
    maps = get_maps()
    if maps:
        current_map_id = maps[0]['id']  # Assuming the first map in the list is the current map
        map_details = get_map_details(current_map_id)
        if map_details:
            print("Map Name:", map_details['map_name'])
            print("Created Time:", map_details['create_time'])
            print("Image URL:", map_details['image_url'])
            # BASE_URL = "ws://192.168.2.173:8090/ws/v2/topics"
            # pose = asyncio.get_event_loop().run_until_complete(get_robot_pose(BASE_URL))
            # if pose:
            #     print("Current Position:", pose['pos'])
            #     print("Current Orientation:", pose['ori'])
        else:
            print("No map details available.")
    else:
        print("No maps available.")
    #     ---
    app = QApplication(sys.argv)

    # Fetch map detail and robot position
    map_url = get_map_details(current_map_id)
    if map_url:
        # Load the map image (assuming it's a grayscale image)

        robot_pos = await get_robot_pose("ws://192.168.2.173:8090/ws/v2/topics")
        map_image = plt.imread(map_url, format='pbstream')

        window = MainWindow(map_image, robot_pos)
        window.show()
        sys.exit(app.exec_())
    else:
        print("Failed to load map data")


if __name__ == "__main__":
    asyncio.run(main())

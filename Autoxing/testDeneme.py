import sys
import requests
import asyncio
import websockets
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt5.QtCore import Qt
from io import BytesIO
from PIL import Image


class MapWidget(QWidget):
    def __init__(self, map_image):
        super().__init__()
        self.map_image = map_image
        self.robot_pos = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.map_label = QLabel(self)
        self.map_label.setPixmap(QPixmap.fromImage(self.map_image))
        layout.addWidget(self.map_label)
        self.setLayout(layout)

    def update_robot_position(self, pos):
        self.robot_pos = pos
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.robot_pos:
            painter = QPainter(self.map_label.pixmap())
            painter.setPen(Qt.red)
            painter.setBrush(QColor(255, 0, 0))
            x = int(self.robot_pos[0] * self.map_label.width())
            y = int(self.robot_pos[1] * self.map_label.height())
            painter.drawEllipse(x, y, 10, 10)
            painter.end()
            self.map_label.update()


class MainWindow(QMainWindow):
    def __init__(self, map_image):
        super().__init__()
        self.setWindowTitle('Map Viewer with Robot Position')
        self.setGeometry(100, 100, 800, 600)
        self.map_widget = MapWidget(map_image)
        self.setCentralWidget(self.map_widget)

    def update_robot_position(self, pos):
        self.map_widget.update_robot_position(pos)


def download_map_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content)).convert('RGB')
    return QImage(image.tobytes(), image.size[0], image.size[1], QImage.Format_RGB888)


async def get_robot_pose(url, window):
    async with websockets.connect(url) as websocket:
        subscribe_message = json.dumps({"enable_topic": "/tracked_pose"})
        await websocket.send(subscribe_message)
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            if data.get("topic") == "/tracked_pose":
                pos = data.get("pos", [])
                window.update_robot_position(pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Harita URL'sini değiştirin
    map_image_url = 'https://www.example.com/path/to/map_image.png'
    map_image = download_map_image(map_image_url)

    window = MainWindow(map_image)
    window.show()

    # Websocket URL'sini değiştirin
    websocket_url = "ws://192.168.2.173:8090/ws/v2/topics"

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(get_robot_pose(websocket_url, window))
    loop.run_until_complete(app.exec_())

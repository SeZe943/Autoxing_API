import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import requests

# Import your custom functions
from Fonksiyon import Konum_Degistirme, jack_up, jack_down


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('main_window.ui', self)

        # Connect the button clicks to their respective functions
        self.pushButton1.clicked.connect(self.fonksiyon1)
        self.pushButton2.clicked.connect(self.fonksiyon2)
        self.pushButton.clicked.connect(self.fetch_data)

    def fonksiyon1(self):
        print("Fonksiyon 1 çalıştı!")
        # Example usage
        Konum_Degistirme((0.0, 10), "sag")
        Konum_Degistirme((0.0, 0.0), "sag")

    def fonksiyon2(self):
        print("Fonksiyon 2 çalıştı!")

    def fetch_data(self):
        # Example URL to fetch data
        url = 'https://api.example.com/data'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Assuming the data you need is in a field called 'value'
                value = data.get('value', 'No data found')
                self.label.setText(str(value))
            else:
                self.label.setText('Failed to retrieve data')
        except Exception as e:
            self.label.setText(f'Error: {str(e)}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

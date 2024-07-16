import requests
import json
import websocket
import time


# Kontrol modunu uzaktan (remote) olarak ayarlama
def set_control_mode():
    url = "http://192.168.2.173:8090/services/wheel_control/set_control_mode"
    headers = {'Content-Type': 'application/json'}
    data = {"control_mode": "remote"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Kontrol modu 'remote' olarak ayarlandı.")
    else:
        print(f"Kontrol modu ayarlanamadı. Durum kodu: {response.status_code}")
        print(response.text)  # Hata mesajını yazdır

set_control_mode()

# Websocket bağlantısını ve komut gönderme fonksiyonunu oluşturma
def send_twist_command(ws, linear_velocity, angular_velocity):
    ws.send(json.dumps({
        "topic": "/twist",
        "linear_velocity": linear_velocity,
        "angular_velocity": angular_velocity
    }))

# Klavye kontrolü için gerekli modülleri yükle
try:
    import keyboard
except ImportError:
    print("keyboard modülü yüklü değil. 'pip install keyboard' komutunu çalıştırın.")
    exit()

# Websocket bağlantısını oluştur
ws = websocket.create_connection("ws://192.168.2.173:8090/ws/v2/topics")
print("Websocket bağlantısı kuruldu.")

# Kontrol döngüsü
try:
    while True:
        if keyboard.is_pressed('up'):
            send_twist_command(ws, 0.5, 0)  # İleri
        elif keyboard.is_pressed('down'):
            send_twist_command(ws, -0.5, 0)  # Geri
        elif keyboard.is_pressed('left'):
            send_twist_command(ws, 0, 0.5)  # Sola
        elif keyboard.is_pressed('right'):
            send_twist_command(ws, 0, -0.5)  # Sağa

        # Geri bildirim bekleme
        result = ws.recv()
        data = json.loads(result)
        if data.get("topic") == "/twist_feedback":
            print("Komut geri bildirimi alındı.")
        time.sleep(0.1)  # Komutlar arasında kısa bir bekleme süresi

except KeyboardInterrupt:
    print("Kontrol durduruldu.")

finally:
    ws.close()
    print("Websocket bağlantısı kapatıldı.")

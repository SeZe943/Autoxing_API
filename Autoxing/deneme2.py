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
        print(response.text)

set_control_mode()

# Websocket bağlantısını ve komut gönderme fonksiyonunu oluşturma
def send_twist_command(ws, linear_x, linear_y):
    ws.send(json.dumps({
        "topic": "/twist",
        "linear_x": linear_x,
        "linear_y": linear_y,

    }))

# Kullanıcıdan x, y koordinatlarını al
x = float(input("Hedef X koordinatını girin: "))
y = float(input("Hedef Y koordinatını girin: "))

# Websocket bağlantısını oluştur
ws = websocket.create_connection("ws://192.168.2.173:8090/ws/v2/topics")
print("Websocket bağlantısı kuruldu.")

# Hedef noktaya gitme döngüsü
try:
    while True:
        # Mevcut konum ile hedef konum arasındaki farkları hesapla
        linear_x = x
        linear_y = y
        angular_z = 0

        # Komut gönder
        send_twist_command(ws, linear_x, linear_y)

        # Geri bildirim bekleme
        result = ws.recv()
        data = json.loads(result)
        if data.get("topic") == "/twist_feedback":
            print("Komut geri bildirimi alındı.")

        # Hedef noktaya ulaşıldı mı kontrol et
        if (linear_x) < 0.1 and (linear_y) < 0.1:
            print("Hedef noktaya ulaşıldı.")
            break

        time.sleep(0.1)  # Komutlar arasında kısa bir bekleme süresi

except KeyboardInterrupt:
    print("Kontrol durduruldu.")

finally:
    ws.close()
    print("Websocket bağlantısı kapatıldı.")
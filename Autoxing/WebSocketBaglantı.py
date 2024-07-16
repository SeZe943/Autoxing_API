## websocket hatalı robotu resetleyip bağlanmak gerekiyor.
import json
import time
from websocket import create_connection

# Websocket URL'si
websocket_url = "ws://192.168.12.1:8090/ws/v2/topics"


def get_robot_pose_for_10_seconds():
    try:
        # Websocket bağlantısını oluştur
        ws = create_connection(websocket_url)
        print("Websocket bağlantısı kuruldu.")

        # Konuları etkinleştir
        ws.send(json.dumps({"enable_topic": "/tracked_pose"}))

        start_time = time.time()

        while time.time() - start_time < 10:
            # Mesajları al
            result = ws.recv()
            data = json.loads(result)

            # Pozisyon verilerini kontrol et
            if data.get("topic") == "/tracked_pose":
                pos = data.get("pos")
                ori = data.get("ori")
                print(f"Robot Pozisyonu: {pos}, Yönelim: {ori}")

            time.sleep(1)  # Her saniye pozisyonu kontrol et

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        # Websocket bağlantısını kapat
        ws.close()
        print("Websocket bağlantısı kapatıldı.")


# Robotun pozisyonunu 10 saniye boyunca al
get_robot_pose_for_10_seconds()

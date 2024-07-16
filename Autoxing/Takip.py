import time
import requests
import json

BASE_URL = "http://192.168.12.145:8090"

def get_target_position():
    # Hedefin konumunu almak için gerçek yöntemi buraya ekleyin.
    # Örneğin, sensör veya kamera kullanarak hedefin konumunu alabilirsiniz.
    # Örnek olarak statik bir konum döndüren sahte bir fonksiyon kullanıyoruz.
    return (0.0, 0.0)

def create_move(target):
    url = f"{BASE_URL}/chassis/moves"
    headers = {'Content-Type': 'application/json'}
    data = {
        "type": "standard",
        "target_x": target[0],
        "target_y": target[1],
        "target_z": 0.0,
        "target_ori": 1.5708,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        response_data = response.json()
        return response_data.get("id")
    else:
        print("Hareket oluşturma başarısız oldu. Durum kodu:", response.status_code)
        return None

def monitor_move(move_id):
    url = f"{BASE_URL}/chassis/moves/{move_id}"
    old_state = None
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            state = data.get("state")
            if state is not None and state != old_state:
                print("Durum:", state)
                old_state = state
                if state in ["succeeded", "failed"]:
                    break
        else:
            print("Bir hata oluştu. Durum kodu:", response.status_code)
        time.sleep(1)

def follow_target():
    while True:
        target = get_target_position()
        print("Yeni hedef konumu:", target)
        move_id = create_move(target)
        if move_id:
            monitor_move(move_id)

# Örnek kullanım
follow_target()

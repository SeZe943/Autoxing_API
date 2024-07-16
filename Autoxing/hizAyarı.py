import requests
import json

def set_forward_velocity(base_url, velocity):
    """
    Belirtilen base_url kullanarak robotun ileri hareket hızını ayarlar.
    """
    url = f"{base_url}/robot-params"
    headers = {'Content-Type': 'application/json'}
    data = {
        "/wheel_control/max_backward_velocity": velocity  # İleri hareket maksimum hız değeri
    }
    data_json = json.dumps(data)

    try:
        response = requests.post(url, headers=headers, data=data_json)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Başarısız. Durum kodu: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Hata: {e}"

# Kullanım örneği:
base_url = "http://192.168.2.173:8090"
velocity = -0.2  # İleri hareket hızı

response_data = set_forward_velocity(base_url, velocity)
print("Yanıt:", response_data)

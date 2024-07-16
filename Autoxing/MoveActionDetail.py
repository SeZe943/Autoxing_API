# Aracın konumunu şarj olup olmadığını hareket id no'sunu gibi çeşitli bilgiler veriyor.
# url = f"{base_url}/chassis/moves/905" bu linkteki en son kısımda olan 905 sayısı sürekli güncellenmeli. yoksa eski ve hatalı değerleri gösterecektir.
import requests
import json


# Function to list maps
def Move_Detail(base_url):
    url = f"{base_url}/chassis/moves/1137"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        MoveDetail = response.json()
        # Movedetail = Move_Detail(base_url)
        # print("Move Detail:", Movedetail)
        return MoveDetail
    else:
        print(f"Failed to retrieve maps. Status code: {response.status_code}")
        return []



base_url = "http://192.168.2.148:8090"
# Retrieve and print maps
Movedetail = Move_Detail(base_url)
print("Move Detail:", Movedetail)

if Movedetail:
    move_type = Movedetail.get('type')
    Target_X = Movedetail.get('target_x')
    Target_Y = Movedetail.get('target_y')
    print("X:", Target_X)
    print("Y:", Target_Y)

    if move_type == 'charge':
        print("şarj")
    else:
        print("şarj olmuyor")
else:
    print("Move details could not be retrieved.")

from Fonksiyon import get_robot_pose, get_2_robot_pose, Konum_Degistirme, jack_up, jack_down
import asyncio

# Robotların IP adresleri
BASE_ws = "ws://192.168.2.173:8090/ws/v2/topics"
BASE_ws2 = "ws://192.168.2.60:8090/ws/v2/topics"
Base_URL = "http://192.168.2.173:8090"

# Robotların pozisyonlarını belirlemek için gerekli komut. # İki fonskiyon beraber çalışmıyor
asyncio.get_event_loop().run_until_complete(get_robot_pose(BASE_ws))  # Tek robottan veri alır
# asyncio.run(get_2_robot_pose(BASE_ws, BASE_ws2)) # 2 robottan veri alır.

target = (0.0, 1.0)
ori = "ileri"
Konum_Degistirme(target, ori, Base_URL)

jack_up()
jack_down()
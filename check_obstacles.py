import serial
import time
import json
import redis
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0)
DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)
print("Connected to " + DWM.name)
DWM.write("\r\r".encode())
print("Encode")
time.sleep(1)
DWM.write("lec\r".encode())
print("Encode")

print('Work area')
leftmost_x = 0
rightmost_x = 10
nearest_y = 0
furthest_y = 10

time.sleep(1)
try:
    while True:
        data = DWM.readline()
        if(data):
            print(data)
            if("POS" in data):
                pos = {"x": data[data.index("POS")+1],
                        "y": data[data.index("POS")+2]}
                print(pos)
                check_workarea((pos['x'],pos['y']))
                check_obstacles((pos['x'],pos['y']))

                pos = json.dumps(pos)

                r.set(f'{datetime.now().isoformat()} POS', pos)
                
        time.sleep(1)
    DWM.write("\r".encode())
    DWM.close()

except KeyboardInterrupt:
    print("Stop")
import serial
import time
import ezdxf as edf
import math
import pickle
import time

from datetime import datetime

from helpers.lines import *
from helpers.curves import *
from helpers.layers import *
from helpers.dxfConversion import *

doc = edf.readfile('./resources/dxfs/Drawing12 - office table test.dxf')
msp = doc.modelspace()
entities = getEntitiesInLayer(msp)
obstacles = entities['0']
WA = getWorkingArea(list(msp.query('LINE')))

methods = {
    'LWPOLYLINE' : is_point_in_polyline,
    'CIRCLE' : is_point_in_circ,
    'ELLIPSE' : is_point_in_ellipse,
    'SPLINE' : isInSPLine
}

discretisedWA = discretizeWorkingArea(WA)
obstaclePoints = []
counter =0
with open('/home/pi/cadpos/resources/obsPoints','rb') as obsPoints_file:
    obstaclePoints = pickle.load(obsPoints_file)

print(obstaclePoints[:20])


DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)
DWM.write("\r\r".encode())
print("Encode")
time.sleep(1)
DWM.write("lec\r".encode())

loc = {}

anchorXY = defineTagWorkingArea(['C','B','A'], WA)
with open('pos_log', 'w') as logfile:
    while True:
        time.sleep(1)
        data = DWM.readline().decode("utf-8") 
        fields = data.strip().split(',')
        if len(fields) < 6:
            continue
        #print(data)
        for idx, field in enumerate(fields):
            if field == 'AN1':
                loc['A'] = [float(i) for i in fields[idx+2:idx+6]]
            elif field == 'AN2':
                loc['B'] =  [float(i) for i in  fields[idx+2:idx+6]]
            elif field == 'AN0':
                loc['C'] =  [float(i) for i in  fields[idx+2:idx+6]]
            elif field == 'POS':
                loc['TAG'] =  [float(i) for i in fields[idx+1:idx+4]]
        
        my_loc_in_dxf = parseDeca(loc, anchorXY)
        msg = f'{datetime.now()}: loc deca:{loc["TAG"]};  log dxf = {my_loc_in_dxf}\n'
#         logfile.write(msg)
        print(msg)
        if my_loc_in_dxf in obstaclePoints:
            print('INSIDE OBS') 
    
import ezdxf as edf
import math

from helpers.lines import *
from helpers.curves import *
from helpers.layers import *

doc = edf.readfile('/Users/zoelim/cadpos/resources/dxfs/Drawing5- 2 squares(dimensions).dxf')
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
for point in discretisedWA:
    for entity in obstacles:
        if entity.dxftype() in methods.keys():
            labelPoint = methods[entity.dxftype()](point, entity)
            if labelPoint >= 0:
                obstaclePoints.append(point)
            counter += 1
            if counter %100000==0:
                print(counter)




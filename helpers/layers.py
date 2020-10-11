import numpy as np
import ezdxf as edf

def getEntitiesInLayer(msp):
    entitiesDict = dict()
    for e in msp.query():
        layer = e.dxf.layer
        if layer not in list(entitiesDict.keys()):
            entitiesDict.update({layer: [e]})
        else:
            entitiesDict[layer].append(e)
        
    return entitiesDict

def discretizeWorkingArea(workingArea):
    allX = [i[0] for i in workingArea]
    allY = [i[1] for i in workingArea]
    
    leftX = min(allX)
    rightX = max(allX)
    bottomY = min(allY)
    topY = max(allY)
    
    xyPairs = np.mgrid[leftX:rightX+0.01:0.01, bottomY:topY+0.01:0.01].reshape(2,-1).T
    discretePoints = [edf.math.Vec2(i[0], i[1]) for i in xyPairs]

    return discretePoints            
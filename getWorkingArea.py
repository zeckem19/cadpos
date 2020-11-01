for e in msp.query('LINE'):
    originalLines.append(e)
    originalVectorPoints.append((e.dxf.start[0], e.dxf.start[1]))
    originalVectorPoints.append((e.dxf.end[0], e.dxf.end[1]))
    originalPoints.append((e.dxf.start.x, e.dxf.start.y))
    originalPoints.append((e.dxf.end.x, e.dxf.end.y))
for e in msp.query('LWPOLYLINE'):
    vertices = list(e.vertices())
    for v in vertices:
        originalVectorPoints.append(v)

originalVectorPoints = [(round(i[0],2), round(i[1],2)) for i in originalVectorPoints]
def getWorkingArea(originalVectorPoints):
    sortedVectorPoints = sorted(originalVectorPoints, key=itemgetter(0,1))
    origin = sortedVectorPoints[0]
    topXY = sortedVectorPoints[-1]
    
    sortedVectorPointsLeft = [i for i in sortedVectorPoints if i[0]==origin[0]]
    sortedVectorPointsLeft = sorted(sortedVectorPointsLeft, key=itemgetter(0,1))
    
    topYLeft = sortedVectorPointsLeft[-1]
    
    sortedVectorPointsRight = [i for i in sortedVectorPoints if i[0]==topXY[0]]
    sortedVectorPointsLeft = sorted(sortedVectorPointsLeft, key=itemgetter(1,0))
    
    bottomYRight = sortedVectorPointsLeft[0]
    
    workingArea = ((origin[0], origin[1]), (topYLeft[0], topYLeft[1]), (topXY[0], topXY[1]), (bottomYRight[0], bottomYRight[1]))

    return workingArea    
    
workingArea = getWorkingArea(originalVectorPoints)
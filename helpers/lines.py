import math
import ezdxf as edf
from operator import itemgetter


def calculateLength(e):
    xy = e.dxf.end - e.dxf.start
    length = math.sqrt(xy[0]**2+xy[1]**2)

    return length

def print_entity(e):
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)
    print("length: %s\n" % calculateLength(e))

def getPoints(e):
    # originalLines.append((e.dxf.start, e.dxf.end))
    originalLines.append(e)
    originalPoints.append(e.dxf.start)
    originalPoints.append(e.dxf.end)
    originalPointsVector.append((e.dxf.start.x, e.dxf.start.y))
    originalPointsVector.append((e.dxf.end.x, e.dxf.end.y))


def getPointsInConvex(allPoints, convex):
    innerPoints = list()
    for e in allPoints:
        if edf.math.is_point_in_polygon_2d(e, convex):
            innerPoints.append(e)
    return innerPoints

def getWorkingAreaLines(workingArea, originalLines):
    workingLines = list()
    for point in workingArea:
        for line in originalLines:
            if edf.math.is_point_on_line_2d(point, (line.dxf.start.x, line.dxf.start.y), (line.dxf.end.x, line.dxf.end.y)):
                workingLines.append(line)
    return list(set(workingLines))
    

def constructPolygon(obstacleLines):
    obstaclePoints = list()
    for line in obstacleLines:
        obstaclePoints.append(line.dxf.start)
        obstaclePoints.append(line.dxf.end)
    
    polygon = edf.math.convex_hull_2d(obstaclePoints)
    
    print(polygon)
    return polygon
    
def getObstaclePolygons(innerLines, originalPoints):
    obstacles = list()
    for i in range(0, len(innerLines), 1):
        if i == len(innerLines)-1:
                break
        obstacle = list()
        firstLine = innerLines[i]
        if len(obstacles) > 0:
            start = firstLine.dxf.start
            end = firstLine.dxf.end
            convex = constructPolygon(obstacles[-1])
            if firstLine in obstacles[-1]:
                continue
            elif edf.math.is_point_in_polygon_2d(start, convex) in [0,1] and edf.math.is_point_in_polygon_2d(end, convex) in [0,1]:
                continue
            
            
        obstacle.append(firstLine)
        for j in range(1, len(innerLines), 1):
            secondLine = innerLines[j]
            intersection = edf.math.intersection_line_line_2d((firstLine.dxf.start, firstLine.dxf.end), \
                                                              (secondLine.dxf.start, secondLine.dxf.end))
        
            if intersection in originalPoints:
                obstacle.append(secondLine)
        
        if len(obstacle) > 0:
            obstacles.append(obstacle)
            
    return obstacles

def getWorkingArea(msp):
    originalVectorPoints = []
    for e in msp.query('LINE'):
        originalVectorPoints.append((e.dxf.start[0], e.dxf.start[1]))
        originalVectorPoints.append((e.dxf.end[0], e.dxf.end[1]))

    for e in msp.query('LWPOLYLINE'):
        vertices = list(e.vertices())
        for v in vertices:
            originalVectorPoints.append(v)

    originalVectorPoints = [(round(i[0],2), round(i[1],2)) for i in originalVectorPoints]

    sortedVectorPoints = sorted(originalVectorPoints, key=itemgetter(0,1))
    origin = sortedVectorPoints[0]
    topXY = sortedVectorPoints[-1]
    
    sortedVectorPointsLeft = [i for i in sortedVectorPoints if i[0]==origin[0]]
    sortedVectorPointsLeft = sorted(sortedVectorPointsLeft, key=itemgetter(0,1))
    
    topYLeft = sortedVectorPointsLeft[-1]
    
    sortedVectorPointsRight = [i for i in sortedVectorPoints if i[0]==topXY[0]]
    sortedVectorPointsRight = sorted(sortedVectorPointsRight, key=itemgetter(1,0))
    
    bottomYRight = sortedVectorPointsRight[0]
    
    workingArea = ((origin[0], origin[1]), (topYLeft[0], topYLeft[1]), (topXY[0], topXY[1]), (bottomYRight[0], bottomYRight[1]))

    return workingArea    
    

    
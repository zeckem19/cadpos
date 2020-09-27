import ezdxf as edf
import math

allPoints = list()

def calculateLength(e):
    xy = e.dxf.end - e.dxf.start
    length = math.sqrt(xy[0]**2+xy[1]**2)

    return length

def print_entity(e):
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)
    print("length: %s\n" % calculateLength(e))

def getPoints(e):
    allPoints.append(e.dxf.start)
    allPoints.append(e.dxf.end)

def getPointsInConvex(allPoints, convex):
    innerPoints = list()
    for e in allPoints:
        if edf.math.is_point_in_polygon_2d(e, convex):
            innerPoints.append(e)
    return innerPoints


if __name__ == '__main__':
    doc = edf.readfile('./resources/dxfs/Drawing5- 2 squares(dimensions).dxf')
    msp = doc.modelspace()
    for e in msp.query('LINE'):
        print_entity(e)
        getPoints(e)

    convex = edf.math.convex_hull_2d(allPoints)
    #offsetVertices = list(edf.math.offset_vertices_2d(convex,offset=0.01, closed=True))
    innerPoints = getPointsInConvex(allPoints, convex)

    innerConvex = edf.math.convex_hull_2d(innerPoints)


    for i in [convex,innerPoints,innerConvex]:
        print(f'Total: {len(i)}')
        for j in i:
            print(j)
        print('-'*20)
import math
import ezdxf as edf


def dist_between_pts(p1, p2):
    return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

def pythagoras(side1, side2):
    return math.sqrt(side1*side1 + side2*side2)

def is_point_in_circ(
                p1 : edf.entities.point.Vector,
                circ : edf.entities.circle):
    ''' Returns -1 if points is outside circle
        Returns 1 if point is inside circle
        
        tolerance is 1e5, returns 0 if point is on 
        boundary within tolerance level'''
    p2 = circ.dxf.center
    dist = dist_between_pts(p1, p2)
    diff = dist - circ.dxf.radius
    if diff > 1e5:
        return -1
    elif diff < -1e5:
        return 1
    else:
        return 0

def is_point_in_ellipse(
        p1 : edf.entities.point.Vector,
        ell : edf.entities.ellipse.Ellipse):
    ''' Returns -1 if points is outside circle
        Returns 1 if point is inside circle
        
        tolerance is 1e5, returns 0 if point is on 
        boundary within tolerance level.
        (𝑥−ℎ)2𝑟2𝑥+(𝑦−𝑘)2𝑟2𝑦≤1
        '''
    
    p2 = ell.dxf.center
    h = ell.dxf.center[0]
    k = ell.dxf.center[1]
    
    major = pythagoras(ell.dxf.major_axis[0], ell.dxf.major_axis[1])
    minor = pythagoras(ell.minor_axis[0], ell.minor_axis[1])
    
    x = p1[0]
    y = p1[1]
    
    test = ((x - h)**2/ (major**2)) + ((y - k)**2/ (minor**2)) 
    
    if test > 1.00001:
        return -1
    elif test < 0.99999:
        return 1
    else:
        return 0

def is_point_in_polyline(
                p1 : edf.entities.point.Vector,
                pline : edf.entities.polyline):
    convex2 = edf.math.convex_hull_2d(list(pline.lwpoints))
    return edf.math.is_point_in_polygon_2d(p1, convex2)



def convert_line_to_points(start_pt, end_pt):
    ''' 3 cases: horizontal, vertical and diagonal'''
    if start_pt['x'] > end_pt['x'] or start_pt['y'] > end_pt['y']:
        start_pt, end_pt = end_pt, start_pt

    # Vertical line
    if end_pt['x'] > start_pt['x'] and end_pt['y'] == start_pt['y']:
        vline_haul = [ Coordinate(pt, end_pt['y']) for pt in range(start_pt['x'], end_pt['x'])]
    # Horizontal
    if end_pt['y'] > start_pt['y'] and end_pt['x'] == start_pt['x']:
        hline_haul = [ Coordinate(pt, end_pt['x']) for pt in range(start_pt['y'], end_pt['y'])]
    # Diagonal 
    if end_pt['y']  > start_pt['y'] and end_pt['x'] > start_pt['x']:
        points_set = set()

def convert_block_to_points():
    pass


def getSPFitLines(spline):
    fitLines = list()
    spPoints = spline.fit_points
    for i in range(len(spPoints)):
        startPoint = spPoints[i]
        if i == len(spPoints)-1:
            endPoint = spPoints[0]
        else:
            endPoint = spPoints[i+1]
        fitLines.append((edf.math.Vec2(startPoint[0], startPoint[1]), edf.math.Vec2(endPoint[0], endPoint[1])))
    return fitLines

def isInSPLine(fitLines, testingPoint, spline):
    isIntersection = list()
    for point in spline.fit_points:
        cuttingLine = (testingPoint, edf.math.Vec2(point[0], point[1]))
        intersection = 0
        for lines in fitLines:
            intersectionPoint = edf.math.intersection_line_line_2d(cuttingLine, (lines[0], lines[1]))
            if intersectionPoint:
                intersection += 1
        if intersection % 2 == 1:
            isIntersection.append(True)
        
        if len([i for i in isIntersection if i == True]) == 3:
            return True
    
    return False


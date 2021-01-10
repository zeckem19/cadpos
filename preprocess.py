import sys
import ezdxf as edf
import math
import pickle

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from tqdm import tqdm
import shapely.geometry as sg

from helpers.lines import *
from helpers.curves import *
from helpers.layers import *



methods = {
        'LWPOLYLINE' : is_point_in_polyline,
        'CIRCLE' : is_point_in_circ,
        'ELLIPSE' : is_point_in_ellipse,
        'SPLINE' : isInSPLine
    }

def process_2d_polyline(polyline):
    xy = []
    
    for i, location in enumerate(polyline.vertices()): 
        xy.append([location[0], location[1]])

    if polyline.is_closed:    
        pl = sg.LinearRing(xy)
    else:
        pl = sg.LineString(xy)
    return pl


if __name__ == "__main__":
    inputs = sys.argv
    fil_path = inputs[1]

    doc = edf.readfile(fil_path)
    msp = doc.modelspace()
    entities = getEntitiesInLayer(msp)
    obstacles = entities['0']

    # Convert obstacles from ezdxf -> shapely
    shapely_obstacles = []
    for obstacle in obstacles:
        try:
            shapely_obstacles.append(process_2d_polyline(obstacle))
        except:
            print(str(obstacle))
            continue
        
    WA = getWorkingArea(msp)
    working_area_file = './resources/pickle/latest_working_area'
    with open(working_area_file,'wb') as waf:
        print(f"Saving working area")
        pickle.dump(WA, waf)

    min_x, max_x = min([pt[0] for pt in WA]), max([pt[0] for pt in WA])
    min_y, max_y = min([pt[1] for pt in WA]), max([pt[1] for pt in WA])
    iter_pts = [int(pt*100)  for pt in [min_x, max_x, min_y, max_y] ]

    # Draw (max_x - min_x)*100 lines along (min_y, max_y)
    lines = []
    for i in tqdm(range(iter_pts[0] - 1 ,iter_pts[1] + 1,1), desc='Generating lines along y', ncols=80, colour='green'):
        x = float(i)/100
        line = sg.LineString([[x,min_y],[x,max_y]])
        lines.append(line)

    # Draw (max_y - min_y)*100 lines along (min_x, max_x)
    for i in tqdm(range(iter_pts[2] - 1 ,iter_pts[3] + 1,1), desc='Generating lines along x', ncols=80, colour='green'):
        y = float(i)/100
        line = sg.LineString([[min_x,y],[max_x,y]])
        lines.append(line)

    shapely_obs_points = []
    # Intersect lines and obstacles
    for line in tqdm(lines, desc='Lines progress'):
        for so in shapely_obstacles:
            intersect_points = line.intersection(so)
            if isinstance(intersect_points, sg.point.Point):
                shapely_obs_points.append(intersect_points)
            elif isinstance(intersect_points, sg.multipoint.MultiPoint):
                shapely_obs_points.extend(intersect_points)

    ## Keep for future use with Spline ##
    # discretisedWA = discretizeWorkingArea(WA)
    # obstaclePoints = []
    
    # print(f"Calculating obstacle points...")
    # for point in tqdm(discretisedWA):
    #     for entity in obstacles:
    #         if entity.dxftype() in methods.keys():
    #             labelPoint = methods[entity.dxftype()](point, entity)
    #             if labelPoint >= 0:
    #                 obstaclePoints.append(point)
    

    print(f"Serialising {len(shapely_obs_points)} obstacle points...")
    if len(inputs) >= 3:
        output_path = inputs[2]
    else:
        fil = fil_path.split('/')[-1]
        output_path = f'./resources/pickle/{fil}_pickle_obstacles'

    with open(output_path,'wb') as obs_file:
        pickle.dump(shapely_obs_points, obs_file)
    
    print(f"Saving obstacle pickle file_path to run")
    with open('./resources/pickle/latest','w') as record:
        record.write(f'{output_path}')
    
    print('Pathfinding.. ')
    print('Adding obstacle points into Pathfinding matrix')
    pathfinding_matrix = getPathFindingWA(WA)
    for pt in shapely_obs_points:
        row = int((pt.y - WA[0][1])*100)
        col = int((pt.x - WA[0][0])*100)
        pathfinding_matrix[row][col] = 0
    
    with open('./resources/pickle/pathfinding_matrix','wb') as pf_matrix:
        pickle.dump(pathfinding_matrix, pf_matrix)

    print('Build graph')
    grid = Grid(pathfinding_matrix)

    # start = grid.node(, )
    # end = grid.node(2, 2)
import sys
import ezdxf as edf
import math
import pickle

from tqdm import tqdm
from helpers.lines import *
from helpers.curves import *
from helpers.layers import *

if __name__ == "__main__":
    inputs = sys.argv
    fil_path = inputs[1]

    doc = edf.readfile(fil_path)
    msp = doc.modelspace()
    entities = getEntitiesInLayer(msp)
    obstacles = entities['0']
    WA = getWorkingArea(msp)
    working_area_file = './resources/pickle/latest_wa'
    with open(working_area_file,'wb') as waf:
        print(f"Saving working area")
        pickle.dump(WA, waf)

    methods = {
        'LWPOLYLINE' : is_point_in_polyline,
        'CIRCLE' : is_point_in_circ,
        'ELLIPSE' : is_point_in_ellipse,
        'SPLINE' : isInSPLine
    }

    discretisedWA = discretizeWorkingArea(WA)
    obstaclePoints = []
    
    print(f"Calculating obstacle points...")
    for point in tqdm(discretisedWA):
        for entity in obstacles:
            if entity.dxftype() in methods.keys():
                labelPoint = methods[entity.dxftype()](point, entity)
                if labelPoint >= 0:
                    obstaclePoints.append(point)

    print(f"Serialising obstacle points...")
    if len(inputs) >= 3:
        output_path = inputs[2]
    else:
        fil = fil_path.split('/')[-1]
        output_path = f'./resources/pickle/{fil}_pickle'

    with open(output_path,'wb') as obs_file:
        pickle.dump(obstaclePoints, obs_file)
    
    print(f"Saving obstacle pickle file_path to run")
    with open('./resources/pickle/latest','w') as record:
        record.write(f'{output_path}')
    

    



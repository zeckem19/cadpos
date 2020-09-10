from coordinates import Coordinate


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


    


import math

def get_distance(p0, p1):
    return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)

def pos_in_board(x, y):
    '''Calculate the position of the chess on the board'''
    return x*30 + 25, y*30 + 25

def pos_in_qiju(x, y):
    '''Calculate the '''
    return int((x-25)/30), int((y-25)/30)

def pos_to_draw(*args):
    y, x = args
    return x-11, y-11, x+11, y+11

def click_in_board(x, y):
    '''Check whether click event is in the chess board'''
    return x > 10 and x < 460 and y > 10 and y < 460

def get_nearest_po(x, y): 
    _x = int(((x-25) / 15 + 1)/2)
    _y = int(((y-25) / 15 + 1)/2)
    return [_x, _y]
    


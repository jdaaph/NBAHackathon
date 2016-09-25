import scipy
import numpy as np
import pandas as pd
import math
from scipy.stats import entropy

'''
generates the 10 by 10 matrix of 5 foot square values representing the half
court
'''
def gen_position_values():
    values = [[0.0 for i in range(10)] for j in range(10)]
    #x vals are first(long way of court), y vals are second(sideline to sideline)
    values[0][0] = 58.5
    values[0][1] = 43.2
    values[0][2] = 39.0
    values[0][3] = 36.3
    values[0][4] = 54.7
    values[0][5] = 55.3
    values[0][6] = 41.2
    values[0][7] = 40.5
    values[0][8] = 43.0
    values[0][9] = 54.5

    values[1][0] = 55.3
    values[1][1] = 40.7
    values[1][2] = 39.1
    values[1][3] = 40.8
    values[1][4] = 60.7
    values[1][5] = 62.3
    values[1][6] = 41.3
    values[1][7] = 38.1
    values[1][8] = 39.5
    values[1][9] = 57.2

    values[2][0] = 50.9
    values[2][1] = 39.9
    values[2][2] = 40.3
    values[2][3] = 36.9
    values[2][4] = 47.9
    values[2][5] = 48.7
    values[2][6] = 36.7
    values[2][7] = 39.3
    values[2][8] = 40.8
    values[2][9] = 53.8

    values[3][0] = 55.9
    values[3][1] = 38.8
    values[3][2] = 40.6
    values[3][3] = 38.5
    values[3][4] = 41.6
    values[3][5] = 41.2
    values[3][6] = 38.4
    values[3][7] = 40.1
    values[3][8] = 40.5
    values[3][9] = 52.4

    values[4][1] = 52.2
    values[4][2] = 53.3
    values[4][3] = 41.4
    values[4][4] = 39.2
    values[4][5] = 46.0
    values[4][5] = 42.3
    values[4][6] = 42.5
    values[4][7] = 38.4
    values[4][8] = 52.9
    values[4][9] = 50.2

    values[5][0] = 38.7
    values[5][1] = 50.4
    values[5][2] = 50.6
    values[5][3] = 43.8
    values[5][4] = 40.6
    values[5][5] = 39.8
    values[5][6] = 42.6
    values[5][7] = 51.6
    values[5][8] = 47.7
    values[5][9] = 38.9

    values[6][0] = 35.7
    values[6][1] = 30.8
    values[6][2] = 47.8
    values[6][3] = 51.1
    values[6][4] = 55.0
    values[6][5] = 51.7
    values[6][6] = 49.2
    values[6][7] = 47.1
    values[6][8] = 25.2
    values[6][9] = 26.9

    values[7][0] = 10.0
    values[7][1] = 32.9
    values[7][2] = 41.0
    values[7][3] = 40.3
    values[7][4] = 41.7
    values[7][5] = 34.0
    values[7][6] = 25.0
    values[7][7] = 30.5
    values[7][8] = 17.9
    values[7][9] = 10.0

    values[8][0] = 0.0
    values[8][1] = 10.0
    values[8][2] = 5.9
    values[8][3] = 18.8
    values[8][4] = 41.2
    values[8][5] = 10.7
    values[8][6] = 30.0
    values[8][7] = 29.4
    values[8][8] = 10.7
    values[8][9] = 9.1

    values[9][0] = 30.0
    values[9][1] = 16.7
    values[9][2] = 35.7
    values[9][3] = 7.7
    values[9][4] = 31.6
    values[9][5] = 17.4
    values[9][6] = 13.3
    values[9][7] = 28.1
    values[9][8] = 13.2
    values[9][9] = 15.0

    return values

'''
returns the midpoints of each square and the corresponding values
'''
def get_midpoints_and_values():
    values = gen_position_values()
    mid_points = [[ [0.0,0.0] for i in range(10)] for j in range(10)]
    for x in range(10):
        for y in range(10):
            mid_points[x][y] = [2.5 + x*5, 2.5 + y*5]
    return mid_points, values

#tests midpoint function
def test_get_midpoints():
    mid_points, values = get_midpoints_and_values()
    for m in mid_points:
        print m
    print ""
    for v in values:
        print v

def point_distance(p1, p2):
    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ) 

'''
list of the points a player stood in
returns the entropy of places that a player covers
operates by folding the half-court on the basket
'''
def get_player_entropy(player_points):
    folded_court_rep = []
    for p in player_points:
        if p[1] > 4:
            p[1] = 4 - (p[1]-5)
        folded_court_rep.append(str(p[0]) + str(p[1]))
    probs = []
    for u in set(folded_court_rep):
        p_u = float(folded_court_rep.count(u)) / float(len(folded_court_rep))
        probs.append(p_u)
    return entropy(probs) 

'''
accepts a dictionary mapping player to the points they've stood in
returns a dictionary mapping player to entropy of that player's points
'''
def get_all_player_entropy(player_to_points):
    player_to_entropy = {}
    for p in player_to_points:
        player_to_entropy[p] = get_player_entropy(player_to_points[p])
    return player_to_entropy

def test_get_player_entropy():
    test_dict = {'chavis':[[1,1],[2,2],[1,1]], 'evan':[[1,1],[2,2]] }
    print get_all_player_entropy(test_dict)


'''
accepts a list of the indices in the values matrix that the player owns
returns a summation of the value of the player's land
'''
def total_value_of_player_land(idxs):
    pos_values = gen_position_values()
    total_val = 0.0
    for idx in idxs:
        total_val += pos_values[idx[0]][idx[1]]
    return total_val  

'''
accepts a dictionary mapping player name to a list of the points they own
returns a dictionary mapping player name to the total value of the points they own
'''
def all_players_land_value(players_dict):
    player_to_value = {}
    for p_name in players_dict:
        p_land = players_dict[p_name]
        player_to_value[p_name] = total_value_of_player_land(p_land)
    return player_to_value

'''
test all_players_land_value with made up values
'''
def test_all_players_land():
    player_to_value = {"chavis": [[0,0],[9,9]], "evan":[[1,1],[8,8]]}
    players_value = all_players_land_value(player_to_value)
    print players_value

'''
assigns an x-y coordinate to the correct idx in the 10X10 half-court
'''
def assign_square(x,y):
    #nba court is 94(x) by 50(y)
    #moves all players into the halfcourt
    half_a_court = 94.0/2.0
    if x > half_a_court:
        x = half_a_court - (x - half_a_court)
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if y > 50:
        y = 50
    x_idx = int(math.floor(x/5.0))
    y_idx = int(math.floor(y/5.0))
    return {"x": x_idx, "y": y_idx}

def test_assign_squares():
    a = assign_square(0.0,0.0)
    b = assign_square(98.29, 52.8)
    c = assign_square(-3.17, -1.78)
    d = assign_square(50.0, 3.0)
    print a
    print b
    print c
    print d

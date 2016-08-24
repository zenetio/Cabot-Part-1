#!/usr/bin/python
# carlosrl@gmail.com - 08/08/2016

import numpy as np
import yaml

def dijkstras(occupancy_map, x_spacing, y_spacing, start, goal):
    """
    Implements Dijkstra's shortest path algorithm
    Input:
    occupancy_map - an N by M numpy array of boolean values (represented
        as integers 0 and 1) that represents the locations of the obstacles
        in the world
    x_spacing - parameter representing spacing between adjacent columns
    y_spacing - parameter representing spacing between adjacent rows
    start - a 3 by 1 numpy array of (x,y,theta) for the starting position 
    goal - a 3 by 1 numpy array of (x,y,theta) for the finishing position 
    Output: a tuple (path, numopened)
            path: list of the indices of the nodes on the shortest path found
                starting with "start" and ending with "end" (each node is in
                  metric coordinates)
    """
    global map
    global distances
    global parent

    [row, col] = np.shape(occupancy_map)
    map = np.zeros([row, col], dtype=int)
    all_one = np.nonzero(occupancy_map)  		# get all non zero indexes
    all_zero = np.where(occupancy_map == 0)  	# get all zero indexes
    map[all_one] = 2  							# mark obstacle cells
    map[all_zero] = 1  							# mark free cells
    yi = start[0, 0] / x_spacing - 0.5
    xi = start[1, 0] / y_spacing - 0.5
    xi_idx = int(np.around(xi))
    yi_idx = int(np.around(yi))

    start_node = np.ravel_multi_index((xi_idx, yi_idx), dims=(row, col), order='F')
    yg = goal[0, 0] / x_spacing - 0.5
    xg = goal[1, 0] / y_spacing - 0.5
    xg_idx = int(np.around(xg))
    yg_idx = int(np.around(yg))

    dest_node = np.ravel_multi_index((xg_idx, yg_idx), dims=(row, col), order='F')
    distances = np.zeros([row, col])
    distances[:, :] = np.inf
    distances[xi_idx, yi_idx] = 0
    parent = np.zeros([row, col])
    numExpanded = 0

    # loop
    while True:
        map[xi_idx, yi_idx] = 5
        map[xg_idx, yg_idx] = 6

        # draw the map
        # Find the node with the minimum distance
        current = np.where(distances == distances.min())
        if np.size(current) > 2:
            current = [[current[0][0]], [current[1][0]]]

        current_lin = np.ravel_multi_index(current, dims=(row, col), order='F')[0]
        min_dist = distances[current]

        if current_lin == dest_node or np.isinf(min_dist):
            break
        # Update map
        map[current] = 3  				# mark current node as visited
        distances[current] = np.inf  	# remove this node from further consideration
        numExpanded += 1
        # Visit each neighbor of the current node and update the map, distances
        # and parent tables appropriately.
        for iter in range(1, 5):
            l = current[0][0]
            c = current[1][0]
            if iter == 1:
                c += 1  # right neighbor
            elif iter == 2:
                c -= 1  # left neighbor
            elif iter == 3:
                l -= 1  # up neighbor
            else:
                l += 1  # down neighbor
            # check vertical boundaries
            if l < 0:
                l = row - 1
            elif l == row:
                l = 0
            # check horizontal boundaries
            if c < 0:
                c = col - 1
            elif c == col:
                c = 0
            d = min_dist[0] + 1
            update(l, c, d, current_lin)
    # Generate linear indices of start and dest nodes
    [xr, yr] = [0, 0]
    if np.isinf(distances[xg_idx, yg_idx]):
        route = []
    else:
        [xr, yr] = np.unravel_index(int(parent[xg_idx, yg_idx]), dims=(row, col), order='F')
        route = [[goal[0, 0], goal[1, 0]]]

    while parent[xr, yr] != 0:
        xv = round((yr + 0.5) * x_spacing, 2)
        yv = round((xr + 0.5) * y_spacing, 2)
        route = [[xv, yv]] + route
        [xr, yr] = np.unravel_index(int(parent[xr, yr]), dims=(row, col), order='F')

    # save first node
    route = [[start[0, 0], start[1, 0]]] + route
    return route

def update(i, j, d, p):
    if (map[i, j] != 2) and (map[i, j] != 3) and (map[i, j] != 5) and (distances[i, j] > d):
        distances[i, j] = d
        map[i, j] = 4
        parent[i, j] = p

""""
Example
def test():
    """
    Function that provides a few examples of maps and their solution paths
    """
    test_map1 = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]])
    x_spacing1 = 0.13
    y_spacing1 = 0.2
    start1 = np.array([[0.325], [0.3], [0]])
    goal1 = np.array([[0.6], [1], [0]])
    path1 = dijkstras(test_map1, x_spacing1, y_spacing1, start1, goal1)
    true_path1 = np.array([
        # [ 0.3  ,  0.3  ],
        [0.325, 0.3],
        [0.325, 0.5],
        [0.325, 0.7],
        [0.455, 0.7],
        [0.455, 0.9],
        [0.585, 0.9],
        [0.600, 1.0]
    ])
    if np.array_equal(path1, true_path1):
        print("Ok")


def main():
    # Load parameters from yaml
    test()

if __name__ == '__main__':
    main()
"""
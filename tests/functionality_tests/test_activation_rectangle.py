import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from engine.grid import Grid

 
def main():
    grid = Grid(42.444250, 42.444599, -76.483682, -76.483276)

    rows = grid.get_num_rows()
    cols = grid.get_num_cols()

    if rows <= 2 and cols >= 2:
        h = rows
        rows = cols
        cols = h
        print("flip rows, cols for traversal")

    direction = input("Traversal Direction: ")

    if direction.isnumeric():
        numberToDirection = {"0" : "RIGHT", "1" : "UP", "2" : "LEFT", "3" : "DOWN"}
        direction = numberToDirection.get(direction)
    else:
        direction = direction.upper()
        
    print(direction)
    if direction == "UP" or direction == "DOWN":
        grid.direction = grid.Direction.UP
    elif direction == "DOWN":
        grid.direction = grid.Direction.DOWN
    elif direction == "RIGHT":
        grid.direction = grid.Direction.RIGHT
    else:
        grid.direction = grid.Direction.LEFT
    plt.figure()
    plt.title("Activated Nodes")
    plt.xlim(-1, grid.get_num_rows() + 1)
    plt.ylim(-1, grid.get_num_cols() + 1)
    plt.grid()

    rec_row_start = rows // 3  # Good value 13
    rec_row_limit = 2 * rows // 3  # Good value 26
    rec_col_start = cols // 3  # Good value 11
    rec_col_limit = 2 * cols // 3  # Good value 22
    grid.activate_rectangle(
        rec_row_start, rec_col_start, rec_row_limit, rec_col_limit
    )
    grid.find_border_nodes()
    way_points = grid.get_all_guided_lawnmower_waypoints_adjustable(direction)

    # Questions: what if we make a new file for visualizing the path? It would also help with catching exceptions.
    #  For example, `node = grid.nodes[i,j]` can throw index out of bound error given STEP_SIZE_METERS of 100,
    #   num rows and cols 3 and circle activation type because num_y_step and num_x_step in int and inversely
    #   proportional to STEP_SIZE_METERS, so num_y_step and num_x_step is 0. Same problem when inputting row and col.
    #   Not sure the formula for determining the max row and col to input tho
    for i in range(grid.get_num_rows()):
        for j in range(grid.get_num_cols()):
            node = grid.nodes[i, j]
            if node.is_border_node():
                plt.plot(i, j, marker="o", color="red")  # Color a border
            elif node.is_active_node():
                plt.plot(i, j, marker="o", color="green")
            else:
                plt.plot(i, j, marker="o", color="blue")

    way_points_x = [pt[0] for pt in way_points]
    way_points_y = [pt[1] for pt in way_points]
    plt.plot(way_points_x, way_points_y, color="purple")
    plt.show()


if __name__ == "__main__":
    main()

import turtle
import reeds_shepp as rs
import utils
import draw
import math
import random as rd
import networkx as nx
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming


def calcDistance(start,finish):
    dist = sqrt((start[0]-finish[0])*(start[0]-finish[0]) +
                (start[1]-finish[1])*(start[1]-finish[1]))
    return dist

def tsp(points):
    dist_matrix = []
    for i in range(len(points)):
        dist_matrix.append([])
        for j in range(len(points)):
            dist_matrix[i].append(calcDistance(points[i],points[j]))


    dist_matrix = np.array(dist_matrix)
    dist_matrix[:, 0] = 0

    # Matrice de distante (graf complet)
    print(dist_matrix)


    permutation, distance = solve_tsp_dynamic_programming(dist_matrix)

    return permutation, distance


def main():
    #size

    n = 10
    m = 2

    pts = np.random.randint(-10, 10, (n, m))

    print("Puncte: ", pts)

    optimal_path, distance = tsp(pts)
    optimal_path = [pts[i] for i in optimal_path]

    x_coords = [pt[0] for pt in pts]
    y_coords = [pt[1] for pt in pts]

    print("Distanta totala: ", distance)

    print(*optimal_path)

    plt.scatter(x_coords, y_coords)
    for i in range(len(optimal_path) - 1):
        plt.plot([optimal_path[i][0], optimal_path[i+1][0]], [optimal_path[i][1], optimal_path[i+1][1]], 'r-')
    plt.grid(True)
    plt.show()

    pts=optimal_path

    # generate PATH so the vectors are pointing at each other
    PATH = []
    for i in range(len(pts) - 1):
        dx = pts[i+1][0] - pts[i][0]
        dy = pts[i+1][1] - pts[i][1]
        theta = math.atan2(dy, dx)
        PATH.append((pts[i][0], pts[i][1], utils.rad2deg(theta)))
    PATH.append((pts[-1][0], pts[-1][1], 0))

    # or you can also manually set the angles:
    # PATH = [(-5,5,90),(-5,5,-90),(1,4,180), (5,4,0), (6,-3,90), (4,-4,-40),(-2,0,240), \
    #         (-6, -7, 160), (-7,-1,80)]

    # or just generate a random route:
    # PATH = []
    # for _ in range(10):
    #     PATH.append((rd.randint(-7,7), rd.randint(-7,7), rd.randint(0,359)))

    # init turtle
    tesla = turtle.Turtle()
    tesla.speed(0) # 0: fast; 1: slow, 8.4: cool
    tesla.shape('arrow')
    tesla.resizemode('user')
    tesla.shapesize(1, 1)

    # draw vectors representing points in PATH
    for pt in PATH:
        draw.goto(tesla, pt)
        draw.vec(tesla)

    # draw all routes found
    tesla.speed(0)
    for i in range(len(PATH) - 1):
        paths = rs.get_all_paths(PATH[i], PATH[i+1])

        for path in paths:
            draw.set_random_pencolor(tesla)
            draw.goto(tesla, PATH[i])
            draw.draw_path(tesla, path)

    # draw shortest route
    tesla.pencolor(1, 0, 0)
    tesla.pensize(3)
    tesla.speed(10)
    draw.goto(tesla, PATH[0])
    path_length = 0
    for i in range(len(PATH) - 1):
        path = rs.get_optimal_path(PATH[i], PATH[i+1])
        path_length += rs.path_length(path)
        draw.draw_path(tesla, path)

    print("Shortest path length: {} px.".format(int(draw.scale(path_length))))

    turtle.done()


if __name__ == '__main__':
    main()

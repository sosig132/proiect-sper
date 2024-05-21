import turtle
import reeds_shepp as rs
import utils
import draw
import math
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming


# Functie pentru calcularea distantei dintre doua puncte
def calcDistance(start,finish):
    dist = sqrt((start[0]-finish[0])*(start[0]-finish[0]) +
                (start[1]-finish[1])*(start[1]-finish[1]))
    return dist


# Algoritmul TSP
def tsp(points):
    dist_matrix = []
    for i in range(len(points)):
        dist_matrix.append([])
        for j in range(len(points)):
            dist_matrix[i].append(calcDistance(points[i],points[j]))

    #dist_matrix este un graf complet, cu distantele dintre puncte
    dist_matrix = np.array(dist_matrix)
    dist_matrix[:, 0] = 0

    print(dist_matrix)


    permutation, distance = solve_tsp_dynamic_programming(dist_matrix)

    return permutation, distance


def main():

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

    PATH = []
    # aici se adauga punctele in path, adaugand si unghiul
    for i in range(len(pts) - 1):
        dx = pts[i+1][0] - pts[i][0]
        dy = pts[i+1][1] - pts[i][1]
        theta = math.atan2(dy, dx)
        PATH.append((pts[i][0], pts[i][1], utils.rad2deg(theta)))
    PATH.append((pts[-1][0], pts[-1][1], 0))



    tesla = turtle.Turtle()
    tesla.speed(0) 
    tesla.shape('arrow')
    tesla.resizemode('user')
    tesla.shapesize(1, 1)

    for pt in PATH:
        draw.goto(tesla, pt)
        draw.vec(tesla)

    tesla.speed(0)
    for i in range(len(PATH) - 1):
        paths = rs.get_all_paths(PATH[i], PATH[i+1])

        for path in paths:
            draw.set_random_pencolor(tesla)
            draw.goto(tesla, PATH[i])
            draw.draw_path(tesla, path)

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

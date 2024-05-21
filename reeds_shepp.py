"""
Implementation of the optimal path formulas given in the following paper:

OPTIMAL PATHS FOR A CAR THAT GOES BOTH FORWARDS AND BACKWARDS
J. A. REEDS AND L. A. SHEPP

notes: there are some typos in the formulas given in the paper;
some formulas have been adapted (cf http://msl.cs.uiuc.edu/~lavalle/cs326a/rs.c)

Each of the 12 functions (each representing 4 of the 48 possible words)
have 3 arguments x, y and phi, the goal position and angle (in degrees) of the
object given it starts at position (0, 0) and angle 0, and returns the
corresponding path (if it exists) as a list of PathElements (or an empty list).

(actually there are less than 48 possible words but this code is not optimized)
"""

from utils import *
import math
from enum import Enum
from dataclasses import dataclass, replace


class Steering(Enum):
    LEFT = -1
    RIGHT = 1
    STRAIGHT = 0


class Gear(Enum):
    FORWARD = 1
    BACKWARD = -1


@dataclass(eq=True)
class PathElement:
    param: float
    steering: Steering
    gear: Gear

    @classmethod
    def create(cls, param: float, steering: Steering, gear: Gear):
        if param >= 0:
            return cls(param, steering, gear)
        else:
            return cls(-param, steering, gear).reverse_gear()

    def __repr__(self):
        s = "{ Steering: " + self.steering.name + "\tGear: " + self.gear.name \
            + "\tdistance: " + str(round(self.param, 2)) + " }"
        return s

    def reverse_steering(self):
        steering = Steering(-self.steering.value)
        return replace(self, steering=steering)

    def reverse_gear(self):
        gear = Gear(-self.gear.value)
        return replace(self, gear=gear)


def path_length(path):
 
    return sum([e.param for e in path])


def get_optimal_path(start, end):
    # alegem drumul optim din cele 48 posibile
    paths = get_all_paths(start, end)
    return min(paths, key=path_length)


def get_all_paths(start, end):
    # generam toate cele 48 de drumuri posibile

    path_fns = [path1, path2, path3, path4, path5, path6, \
                path7, path8, path9, path10, path11, path12]
    paths = []

    x, y, theta = change_of_basis(start, end)

    for get_path in path_fns:
        paths.append(get_path(x, y, theta))
        paths.append(timeflip(get_path(-x, y, -theta)))
        paths.append(reflect(get_path(x, -y, -theta)))
        paths.append(reflect(timeflip(get_path(-x, -y, theta))))

    for i in range(len(paths)):
        paths[i] = list(filter(lambda e: e.param != 0, paths[i]))

    paths = list(filter(None, paths))

    return paths


def timeflip(path):

    new_path = [e.reverse_gear() for e in path]
    return new_path


def reflect(path):

    new_path = [e.reverse_steering() for e in path]
    return new_path


def path1(x, y, phi):
    """
    CSC (same turns)
    """
    phi = deg2rad(phi)
    path = []

    u, t = R(x - math.sin(phi), y - 1 + math.cos(phi))
    v = M(phi - t)

    path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
    path.append(PathElement.create(u, Steering.STRAIGHT, Gear.FORWARD))
    path.append(PathElement.create(v, Steering.LEFT, Gear.FORWARD))

    return path


def path2(x, y, phi):
    """
    CSC (opposite turns)
    """
    phi = M(deg2rad(phi))
    path = []

    rho, t1 = R(x + math.sin(phi), y - 1 - math.cos(phi))

    if rho * rho >= 4:
        u = math.sqrt(rho * rho - 4)
        t = M(t1 + math.atan2(2, u))
        v = M(t - phi)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.STRAIGHT, Gear.FORWARD))
        path.append(PathElement.create(v, Steering.RIGHT, Gear.FORWARD))

    return path


def path3(x, y, phi):
    """
    C|C|C
    """
    phi = deg2rad(phi)
    path = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = R(xi, eta)

    if rho <= 4:
        A = math.acos(rho / 4)
        t = M(theta + math.pi/2 + A)
        u = M(math.pi - 2*A)
        v = M(phi - t - u)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.RIGHT, Gear.BACKWARD))
        path.append(PathElement.create(v, Steering.LEFT, Gear.FORWARD))

    return path


def path4(x, y, phi):
    """
    C|CC
    """
    phi = deg2rad(phi)
    path = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = R(xi, eta)

    if rho <= 4:
        A = math.acos(rho / 4)
        t = M(theta + math.pi/2 + A)
        u = M(math.pi - 2*A)
        v = M(t + u - phi)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.RIGHT, Gear.BACKWARD))
        path.append(PathElement.create(v, Steering.LEFT, Gear.BACKWARD))

    return path


def path5(x, y, phi):
    """
    CC|C
    """
    phi = deg2rad(phi)
    path = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = R(xi, eta)

    if rho <= 4:
        u = math.acos(1 - rho*rho/8)
        A = math.asin(2 * math.sin(u) / rho)
        t = M(theta + math.pi/2 - A)
        v = M(t - u - phi)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.RIGHT, Gear.FORWARD))
        path.append(PathElement.create(v, Steering.LEFT, Gear.BACKWARD))

    return path


def path6(x, y, phi):
    """
    CCu|CuC
    """
    phi = deg2rad(phi)
    path = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = R(xi, eta)

    if rho <= 4:
        if rho <= 2:
            A = math.acos((rho + 2) / 4)
            t = M(theta + math.pi/2 + A)
            u = M(A)
            v = M(phi - t + 2*u)
        else:
            A = math.acos((rho - 2) / 4)
            t = M(theta + math.pi/2 - A)
            u = M(math.pi - A)
            v = M(phi - t + 2*u)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.RIGHT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.LEFT, Gear.BACKWARD))
        path.append(PathElement.create(v, Steering.RIGHT, Gear.BACKWARD))

    return path


def path7(x, y, phi):
    """
    C|CuCu|C
    """
    phi = deg2rad(phi)
    path = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = R(xi, eta)
    u1 = (20 - rho*rho) / 16

    if rho <= 6 and 0 <= u1 <= 1:
        u = math.acos(u1)
        A = math.asin(2 * math.sin(u) / rho)
        t = M(theta + math.pi/2 + A)
        v = M(t - phi)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.RIGHT, Gear.BACKWARD))
        path.append(PathElement.create(u, Steering.LEFT, Gear.BACKWARD))
        path.append(PathElement.create(v, Steering.RIGHT, Gear.FORWARD))

    return path


def path8(x, y, phi):
    """
    C|C[pi/2]SC
    """
    phi = deg2rad(phi)
    path = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = R(xi, eta)

    if rho >= 2:
        u = math.sqrt(rho*rho - 4) - 2
        A = math.atan2(2, u+2)
        t = M(theta + math.pi/2 + A)
        v = M(t - phi + math.pi/2)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(math.pi/2, Steering.RIGHT, Gear.BACKWARD))
        path.append(PathElement.create(u, Steering.STRAIGHT, Gear.BACKWARD))
        path.append(PathElement.create(v, Steering.LEFT, Gear.BACKWARD))

    return path


def path9(x, y, phi):
    """
    CSC[pi/2]|C
    """
    phi = deg2rad(phi)
    path = []

    xi = x - math.sin(phi)
    eta = y - 1 + math.cos(phi)
    rho, theta = R(xi, eta)

    if rho >= 2:
        u = math.sqrt(rho*rho - 4) - 2
        A = math.atan2(u+2, 2)
        t = M(theta + math.pi/2 - A)
        v = M(t - phi - math.pi/2)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.STRAIGHT, Gear.FORWARD))
        path.append(PathElement.create(math.pi/2, Steering.RIGHT, Gear.FORWARD))
        path.append(PathElement.create(v, Steering.LEFT, Gear.BACKWARD))

    return path


def path10(x, y, phi):
    """
    C|C[pi/2]SC
    """
    phi = deg2rad(phi)
    path = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = R(xi, eta)

    if rho >= 2:
        t = M(theta + math.pi/2)
        u = rho - 2
        v = M(phi - t - math.pi/2)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(math.pi/2, Steering.RIGHT, Gear.BACKWARD))
        path.append(PathElement.create(u, Steering.STRAIGHT, Gear.BACKWARD))
        path.append(PathElement.create(v, Steering.RIGHT, Gear.BACKWARD))

    return path


def path11(x, y, phi):
    """
    CSC[pi/2]|C
    """
    phi = deg2rad(phi)
    path = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = R(xi, eta)

    if rho >= 2:
        t = M(theta)
        u = rho - 2
        v = M(phi - t - math.pi/2)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(u, Steering.STRAIGHT, Gear.FORWARD))
        path.append(PathElement.create(math.pi/2, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(v, Steering.RIGHT, Gear.BACKWARD))

    return path


def path12(x, y, phi):
    """
    C|C[pi/2]SC[pi/2]|C
    """
    phi = deg2rad(phi)
    path = []

    xi = x + math.sin(phi)
    eta = y - 1 - math.cos(phi)
    rho, theta = R(xi, eta)

    if rho >= 4:
        u = math.sqrt(rho*rho - 4) - 4
        A = math.atan2(2, u+4)
        t = M(theta + math.pi/2 + A)
        v = M(t - phi)

        path.append(PathElement.create(t, Steering.LEFT, Gear.FORWARD))
        path.append(PathElement.create(math.pi/2, Steering.RIGHT, Gear.BACKWARD))
        path.append(PathElement.create(u, Steering.STRAIGHT, Gear.BACKWARD))
        path.append(PathElement.create(math.pi/2, Steering.LEFT, Gear.BACKWARD))
        path.append(PathElement.create(v, Steering.RIGHT, Gear.FORWARD))

    return path

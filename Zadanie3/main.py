import random as rand
import time
import math


def create_towns(map_x, map_y, count):
    return {i: [rand.randint(0, map_x - 1), rand.randint(0, map_y - 1)] for i in range(count)}


def swap(a, b):
    pass


def shuffle_towns(map, swaps, iterate):
    pass


def calculate_path(point_a, point_b):
    x = math.pow(abs(point_a[0] - point_b[0]), 2)
    y = math.pow(abs(point_a[1] - point_b[1]), 2)
    return math.sqrt(x + y)


def calculate_total_cost(map):
    pass


# print(create_towns(200, 200, 20))
print(calculate_path([0, 0], [1, 1]))

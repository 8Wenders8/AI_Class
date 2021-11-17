import random as rand
import time
import math


def create_towns(map_x, map_y, count):
    return [[rand.randint(0, map_x - 1), rand.randint(0, map_y - 1), i] for i in range(count)]


def swap(town_map, a, b):
    return town_map


def shuffle_towns(town_map, swaps, iterate):
    pass


def random_starting_point(town_map):
    start = rand.randint(0, len(town_map))
    town_map = swap(town_map, start, 0)
    town_map.append(town_map[start])
    return town_map


def calculate_path(point_a, point_b):
    x = math.pow(abs(point_a[0] - point_b[0]), 2)
    y = math.pow(abs(point_a[1] - point_b[1]), 2)
    return math.sqrt(x + y)


def calculate_total_cost(town_map):
    total_cost = 0
    for i in range(len(town_map)):
        pass
        # total_cost += calculate_path(town_map[key], town_map[i+1])
    return total_cost


# print(create_towns(200, 200, 20))
print(calculate_path([0, 1], [3, 0]))

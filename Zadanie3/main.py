import random as rand
import time
import math


def create_map(map_x, map_y, count):
    return shuffle_map([[rand.randint(0, map_x - 1), rand.randint(0, map_y - 1), i] for i in range(count)])


def shuffle_map(town_map):
    town_map.pop(-1)
    rand.shuffle(town_map)
    town_map.append(town_map[0])
    return town_map


def swap(town_map, a, b):
    town_map[a], town_map[b] = town_map[b], town_map[a]
    return town_map


def shuffle_towns(town_map):
    count = len(town_map) - 2
    point_a, point_b = rand.randint(1, count), rand.randint(1, count)
    while point_a == point_b:
        point_b = rand.randint(1, count)
    return swap(town_map, point_a, point_b)


def calculate_path(point_a, point_b):
    x = math.pow(abs(point_a[0] - point_b[0]), 2)
    y = math.pow(abs(point_a[1] - point_b[1]), 2)
    return math.sqrt(x + y)


def calculate_total_cost(town_map):
    total_cost = 0
    for i in range(len(town_map) - 1):
        total_cost += calculate_path(town_map[i], town_map[i + 1])
    return total_cost


def hill_climbing(town_map, iterations):
    current_best = town_map
    while True:
        permutations = list()
        costs = list()
        for i in range(0, iterations):
            permutations.append(shuffle_towns(current_best))
            costs.append(calculate_total_cost(permutations[-1]))
        next_best = min(costs)
        print("Best from generated pool:", next_best, "\nBest current:", calculate_total_cost(current_best))
        if calculate_total_cost(current_best) > next_best:
            current_best = permutations[costs.index(next_best)]
            print("Best new current:", calculate_total_cost(current_best))

        else:
            return current_best





t_map = create_map(200, 200, 20)
print(t_map, "\nStart:", calculate_total_cost(t_map))
t_map = hill_climbing(t_map, 20)
print(t_map, "\nEnd:", calculate_total_cost(t_map))

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
    return swap([row[:] for row in town_map], point_a, point_b)


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
        if calculate_total_cost(current_best) > next_best:
            current_best = permutations[costs.index(next_best)]
        else:
            return current_best


def new_tabu_search(town_map, iterations, tabu_limit):
    tabu = list()
    tabu_costs = list()
    current_best = town_map
    while True:
        permutations = list()
        costs = list()
        for i in range(0, iterations):
            permutations.append(shuffle_towns(current_best))
            costs.append(calculate_total_cost(permutations[-1]))
        next_best = min(costs)
        if calculate_total_cost(current_best) > next_best and current_best not in tabu:
            current_best = permutations[costs.index(next_best)]
        else:
            tabu.append(current_best)
            tabu_costs.append(calculate_total_cost(current_best))
            current_best = next_best
            return current_best



def tabu_search(town_map, iterations, tabu_limit):
    current_best = town_map
    tabu = list()
    tabu_costs = list()
    while True:
        permutations = list()
        costs = list()
        current_cost = calculate_total_cost(current_best)
        for i in range(0, iterations):
            permutations.append(shuffle_towns(current_best))
            costs.append(calculate_total_cost(permutations[-1]))
        next_best = min(costs)
        if len(tabu) == tabu_limit:
            tabu.pop(0)
            tabu_costs.pop(0)
        tabu.append(permutations[costs.index(next_best)])
        tabu_costs.append(next_best)
        permutations.pop(costs.index(next_best))
        costs.pop(costs.index(next_best))
        next_best = min(costs)
        if next_best < current_cost:
            current_best = permutations[costs.index(next_best)]
        else:
            tabu_best = min(tabu_costs)
            if tabu_best < current_cost:
                current_best = tabu[tabu_costs.index(tabu_best)]
            else:
                return current_best


def sequence(town_map):
    return [town_map[i][2] for i in range(len(town_map))]


t_map = create_map(200, 200, 20)
print(t_map, "\nStart:", calculate_total_cost(t_map))
hill_map = hill_climbing(t_map, 20)
print(sequence(hill_map), "\nHill End:", calculate_total_cost(hill_map))
tabu_map = tabu_search(t_map, 20, 5)
print(sequence(tabu_map), "\nTabu End:", calculate_total_cost(tabu_map))

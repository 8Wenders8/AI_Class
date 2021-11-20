import random as rand
import queue
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


def tabu_search(town_map, perm_count, tabu_limit, iterations=1000, time_limit=15):
    timeout = time.time() + time_limit
    counter = 0
    tabu = queue.Queue(tabu_limit)
    current = [calculate_total_cost(town_map), town_map]
    best = [calculate_total_cost(town_map), town_map]
    while time.time() < timeout and counter < iterations:
        permutations = queue.PriorityQueue()
        for i in range(0, perm_count):
            shuffled = shuffle_towns(current[1])
            permutations.put(((calculate_total_cost(shuffled)), shuffled))
        counter += perm_count
        next_best = permutations.get()
        if next_best[0] < best[0]:
            best = [next_best[0], next_best[1]]
        if current[0] < next_best[0] or (current[0], current[1]) in list(tabu.queue):
            if tabu.full():
                tabu.get()
            tabu.put((current[0], current[1]))
        current = [next_best[0], next_best[1]]
    return best


def sequence(town_map):
    return str([town_map[i][2] for i in range(len(town_map))]).strip('[]')


def print_map(town_map):
    print("Map:   id: x, y")
    for enum, item in enumerate(town_map):
        print(str(item[2]) + ':'.ljust(3) + str(item[0:2]).strip('[]').ljust(12), end='')
        if not enum == 0 and not enum % 10:
            print("")
    print("\n")


t_map = create_map(200, 200, 20)
print_map(t_map)
print("Start sequence:", sequence(t_map), "\nStart cost:", "{:.2f}".format(calculate_total_cost(t_map)))
hill_map = hill_climbing(t_map, 20)
print("\nHill sequence:", sequence(hill_map), "\nHill cost:", "{:.2f}".format(calculate_total_cost(hill_map)))
tabu_result = tabu_search(t_map, 20, 15, 10000, 20)
print("\nTabu sequence:", sequence(tabu_result[1]), "\nTabu cost:", "{:.2f}".format(tabu_result[0]))

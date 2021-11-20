#  __  ____     __
# |  \/  \ \   / /   Matej Volansky
# | |\/| |\ \ / /    AIS ID: 103180
# | |  | | \ V /     UI Zadanie.3: TSP - Hill climbing, Tabu search, Simulated annealing
# |_|  |_|  \_/
# -----------------------------------------------------------------
import random as rand
import queue
import time
import math


def create_map(map_x, map_y, count):
    return shuffle_map([[rand.randint(0, map_x - 1), rand.randint(0, map_y - 1), i] for i in range(count + 1)])


def shuffle_map(town_map):
    town_map.pop(-1)  # Remove the last generated town so we can put the starting one there
    rand.shuffle(town_map)  # Randomly shuffle the whole map
    town_map.append(town_map[0])  # Add the starting town to the end
    return town_map


def swap(town_map, a, b):
    town_map[a], town_map[b] = town_map[b], town_map[a]
    return town_map


def shuffle_towns(town_map):
    count = len(town_map) - 2  # We don't want to shuffle starting and ending towns
    point_a, point_b = rand.randint(1, count), rand.randint(1, count)
    while point_a == point_b:  # Ensure the random towns aren't the same
        point_b = rand.randint(1, count)
    return swap([row[:] for row in town_map], point_a, point_b)  # Copy town map by string slicing and pass it to swap


def calculate_path(point_a, point_b):
    x = math.pow(abs(point_a[0] - point_b[0]), 2)  # Get the power of 2 of x difference
    y = math.pow(abs(point_a[1] - point_b[1]), 2)  # Get the power of 2 of y difference
    return math.sqrt(x + y)  # Distance between two points by pythagorean theorem


def calculate_total_cost(town_map):
    total_cost = 0
    for i in range(len(town_map) - 1):
        total_cost += calculate_path(town_map[i], town_map[i + 1])
    return total_cost


def hill_climbing(town_map, perm_count):
    current = [calculate_total_cost(town_map), town_map]
    while True:
        permutations = queue.PriorityQueue()
        for i in range(0, perm_count):
            shuffled = shuffle_towns(current[1])
            permutations.put(((calculate_total_cost(shuffled)), shuffled))
        next_best = permutations.get()
        if next_best[0] < current[0]:  # If a better path was found, continue generating with it
            current = [next_best[0], next_best[1]]
        else:  # If not, return the current best path ( local maximum )
            return current


def tabu_search(town_map, perm_count, tabu_limit, iterations=1000, time_limit=15):
    counter, timeout = 0, time.time() + time_limit  # When to end limitation counters
    tabu_list = queue.Queue(tabu_limit)  # FIFO Queue represented as a Tabu list
    best, current = [calculate_total_cost(town_map), town_map], [calculate_total_cost(town_map), town_map]
    while time.time() < timeout and counter < iterations:
        permutations = queue.PriorityQueue()  # Path with lowest cost is always on the top
        for i in range(0, perm_count):
            shuffled = shuffle_towns(current[1])  # Randomly change two towns in path
            permutations.put(((calculate_total_cost(shuffled)), shuffled))  # Add it to the queue, with it's cost
        counter += perm_count
        next_best = permutations.get()  # Best path from generated pool
        if next_best[0] < best[0]:
            best = [next_best[0], next_best[1]]
        if current[0] < next_best[0] or (current[0], current[1]) in list(tabu_list.queue):
            if tabu_list.full():
                tabu_list.get()  # If tabu list is full, throw the first out
            tabu_list.put((current[0], current[1]))  # Add the local best into the tabu list
        current = [next_best[0], next_best[1]]  # Continue generating with the second best
    return best


def simulated_annealing(town_map):
    pass


def sequence(town_map):
    return str([town_map[i][2] for i in range(len(town_map))]).strip('[]')


def print_map(town_map):
    print("Map:   id: x, y")
    for enum, item in enumerate(town_map):
        print(str(item[2]) + ':'.ljust(3) + str(item[0:2]).strip('[]').ljust(12), end='')
        if enum and enum % 10 == 0:
            print("")


t_map = create_map(200, 200, 20)
print_map(t_map)
print("\nStart sequence:", sequence(t_map), "\nStart cost:", "{:.2f}".format(calculate_total_cost(t_map)))
hill_result = hill_climbing(t_map, 20)
print("\nHill sequence:", sequence(hill_result[1]), "\nHill cost:", "{:.2f}".format(hill_result[0]))
tabu_result = tabu_search(t_map, 20, 15, 10000, 20)
print("\nTabu sequence:", sequence(tabu_result[1]), "\nTabu cost:", "{:.2f}".format(tabu_result[0]))

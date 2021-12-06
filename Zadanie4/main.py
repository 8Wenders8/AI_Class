import random
import matplotlib.pyplot as plt
import time
import random as rand
import math
import queue


def generate_map(boundaries, count=20000):
    return add_points({0:[[rand.randint(boundaries[0], boundaries[1] - 1), rand.randint(boundaries[2], boundaries[3] - 1)] for i in range(20)]}, boundaries, count)


def add_points(k_means_map, boundaries, count):
    for i in range(count):
        interval = 100
        rand_index = rand.randint(0, len(k_means_map) - 1)
        rand_point = k_means_map[0][rand_index]
        rand_offset = rand.randint(0 - interval, interval)
        while boundaries[0] < rand_point[0] + rand_offset > boundaries[1]:
            interval -= 10
            rand_offset = rand.randint(0 - interval, interval)
        new_x = rand_offset
        interval = 100
        rand_offset = rand.randint(0 - interval, interval)
        while boundaries[2] < rand_point[1] + rand_offset > boundaries[3]:
            interval -= 10
            rand_offset = rand.randint(0 - interval, interval)
        k_means_map[0].append([new_x, rand_offset])
    return k_means_map


def distance_two_points(point_a, point_b):
    x = math.pow(abs(point_a[0] - point_b[0]), 2)  # Get the power of 2 of x difference
    y = math.pow(abs(point_a[1] - point_b[1]), 2)  # Get the power of 2 of y difference
    return math.sqrt(x + y)  # Distance between two points by pythagorean theorem


def k_means_centroid(k_means_map, k_count, boundaries):
    groups = len(k_means_map)
    if groups == 1:
        centroids = random.sample(k_means_map[0], k_count)
    else:
        centroids = [[rand.randint(boundaries[0], boundaries[1] - 1), rand.randint(boundaries[2], boundaries[3] - 1)] for i in range(k_count)]
    new_k_map = dict()
    for i in range(k_count):
        new_k_map[i] = list()
    for group in k_means_map:
        for value in k_means_map[group]:
            curr_best = distance_two_points(value, centroids[0])
            index_best = 0
            for centroid in range(1, k_count):
                act = distance_two_points(value, centroids[centroid])
                if act < curr_best:
                    curr_best = act
                    index_best = centroid
            if not new_k_map[index_best]:
                new_k_map[index_best] = list()
            new_k_map[index_best].append(value)

    color = ['red', 'black', 'gray']
    for i in range(k_count):
        length = len(new_k_map[i])
        plt.scatter([new_k_map[i][j][0] for j in range(length)]["X"], [new_k_map[i][j][1] for j in range(length)]["X"], c='blue')
    plt.scatter([centroids[i][0] for i in range(k_count)]["X"], [centroids[i][1] for i in range(k_count)]["Y"], c='blue')
    plt.xlabel('AnnualIncome')
    plt.ylabel('Loan Amount (In Thousands)')
    plt.show()
    return new_k_map


def __main__():
    boundaries = [-200, 200, -200, 200]
    inp = generate_map(boundaries, 20)
    print(inp, "\n", k_means_centroid(inp, 3, boundaries))


__main__()


import time
import random as rand


def generate_map(boundaries, count=20000):
    return add_points([[rand.randint(boundaries[0], boundaries[1] - 1), rand.randint(boundaries[2], boundaries[3] - 1)] for i in range(20)], boundaries, count)


def add_points(k_means_map, boundaries, count):
    for i in range(count):
        interval = 100;
        rand_index = rand.randint(0, len(k_means_map) - 1)
        rand_point = k_means_map[rand_index]
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
        k_means_map.append([new_x, rand_offset])
    return k_means_map


print(generate_map([-200, 200, -200, 200], 20))

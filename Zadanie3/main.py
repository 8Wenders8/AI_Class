import random as rand
import time
import math


def create_towns(map_x, map_y, count):
    return {i: [rand.randint(0, map_x - 1), rand.randint(0, map_y - 1)] for i in range(count)}


print(create_towns(200, 200, 20))

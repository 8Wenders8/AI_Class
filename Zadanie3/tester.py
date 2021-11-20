#  __  ____     __
# |  \/  \ \   / /   Matej Volansky
# | |\/| |\ \ / /    AIS ID: 103180
# | |  | | \ V /     UI Zadanie.3: TSP - Hill climbing, Tabu search, Simulated annealing
# |_|  |_|  \_/      tester.py
# -----------------------------------------------------------------

import matplotlib.pyplot as plt
import time
import main as my

t_map = my.create_map(200, 200, 20)
my.print_map(t_map)
print("\nStart sequence:", my.sequence(t_map), "\nStart cost:", "{:.2f}".format(my.distance_path(t_map)))
hill_result = my.hill_climbing(t_map, 20)
print("\nHill sequence:", my.sequence(hill_result[1]), "\nHill cost:", "{:.2f}".format(hill_result[0]))
start = time.time()
tabu_result = my.tabu_search(t_map, 20, 50, 500, 20)
print("\nEnd tabu time:", time.time() - start)
print("Tabu sequence:", my.sequence(tabu_result[1]), "\nTabu cost:", "{:.2f}".format(tabu_result[0]))
start = time.time()
sa_result = my.simulated_annealing(t_map, 20, 100, 0.1)
print("\nEnd SA time:", time.time() - start)
print("SA sequence:", my.sequence(sa_result[1]), "\nSA cost:", "{:.2f}".format(sa_result[0]))

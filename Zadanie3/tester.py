#  __  ____     __
# |  \/  \ \   / /   Matej Volansky
# | |\/| |\ \ / /    AIS ID: 103180
# | |  | | \ V /     UI Zadanie.3: TSP - Hill climbing, Tabu search, Simulated annealing
# |_|  |_|  \_/      tester.py
# -----------------------------------------------------------------

import matplotlib.pyplot as plt
import time
import main as my

# What do I need to test?:
#       - create graphs here
#       - create TSP maps
#       - test times, SA temperature, maybe results, maybe tabu something


def save_map_graphs(data, x, y, towns):
    data_x, data_y = list(), list()
    title = ['Start', 'Hill Climbing', 'Tabu Search', 'Simulated Annealing']

    for i in range(4):
        data_x.append([data[i][j][0] for j in range(towns)])
        data_y.append([data[i][j][1] for j in range(towns)])
    data_cost = [data[j] for j in range(4, 8)]

    fig, axs = plt.subplots(2, 2)
    print(data_cost)
    for enum, ax in enumerate(axs.flat):
        ax.plot(data_x[enum], data_y[enum], 'ro', data_x[enum], data_y[enum], 'k')
        ax.set(xlim=[0, x], ylim=[0, y], title=title[enum], xlabel='Cost: ' + '{:.2f}'.format(data_cost[enum]))

    fig.tight_layout(pad=0.5)
    fig.set_size_inches(8, 6.4)
    plt.savefig('map_result.png', bbox_inches='tight', dpi=120)
    plt.show()


def save_time_graph(data_x, data_y, title, x_label, x_lim):
    plt.plot(data_x, data_y)
    plt.xlabel(x_label)
    plt.xlim(x_lim)
    plt.ylabel('Time in ms')
    plt.title(title)
    plt.savefig(title.strip(' '), bbox_inches='tight', dpi=120)
    plt.show()


def tabu_test_time_tabu_list(tabu_min, tabu_max, tabu_iter, test_iter=20):
    data = list()
    for i in range(tabu_min, tabu_max, tabu_iter):
        testing_map = my.create_map(1000, 1000, 100)
        average_time = 0
        for j in range(test_iter):
            timer_zero = time.time()
            my.tabu_search(testing_map, 20, i)
            average_time += (time.time() - timer_zero) * 1000
        data.append(average_time/test_iter)
    print(data)
    return data


def tabu_test(tabu_min, tabu_max, tabu_iter, x=200, y=200, towns=20, perm_count=20, iterations=100, time_limit=15):
    # Time tabu list test
    save_time_graph(range(tabu_min, tabu_max, tabu_iter), tabu_test_time_tabu_list(tabu_min, tabu_max, tabu_iter)
                    , 'Tabu list time test', 'Tabu list size', [tabu_min, tabu_max])


plot_data = list()
start_map = my.create_map(200, 200, 20)
start_cost = my.distance_path(start_map)
my.print_map(start_map)
print("\nStart sequence:", my.sequence(start_map), "\nStart cost:", "{:.2f}".format(start_cost))

start = time.time()
hill_result = my.hill_climbing(start_map, 20)
hill_end = time.time() - start
print("\nHill sequence:", my.sequence(hill_result[1]), "\nHill cost:", "{:.2f}".format(hill_result[0]))
print("End hill time:", hill_end)

start = time.time()
tabu_result = my.tabu_search(start_map, 20, 50, 500, 20)
tabu_end = time.time() - start
print("\nTabu sequence:", my.sequence(tabu_result[1]), "\nTabu cost:", "{:.2f}".format(tabu_result[0]))
print("End tabu time:", tabu_end)

start = time.time()
sa_result = my.simulated_annealing(start_map, 20, 100, 0.1)
sa_end = time.time() - start
print("\nSA sequence:", my.sequence(sa_result[1]), "\nSA cost:", "{:.2f}".format(sa_result[0]))
print("End SA time:", sa_end)

plot_data.extend([start_map, hill_result[1], tabu_result[1], sa_result[1]])
plot_data.extend([start_cost, hill_result[0], tabu_result[0], sa_result[0]])

save_map_graphs(plot_data, 200, 200, 21)
tabu_test(1, 200, 1)

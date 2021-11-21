#  __  ____     __
# |  \/  \ \   / /   Matej Volansky
# | |\/| |\ \ / /    AIS ID: 103180
# | |  | | \ V /     UI Zadanie.3: TSP - Hill climbing, Tabu search, Simulated annealing
# |_|  |_|  \_/      tester.py
# -----------------------------------------------------------------

import matplotlib.pyplot as plt
import time
import main as my


def save_map_graphs(data, x, y, towns):
    data_x, data_y = list(), list()
    title = ['Start', 'Hill Climbing', 'Tabu Search', 'Simulated Annealing']
    for i in range(4):
        data_x.append([data[i][j][0] for j in range(towns)])
        data_y.append([data[i][j][1] for j in range(towns)])
    data_cost = [data[j] for j in range(4, 8)]
    data_time = [data[j] for j in range(8, 12)]

    fig, axs = plt.subplots(2, 2)
    for enum, ax in enumerate(axs.flat):
        ax.plot(data_x[enum], data_y[enum], 'ro', data_x[enum], data_y[enum], 'k')
        ax.set(xlim=[0, x], ylim=[0, y], title=title[enum],
               xlabel='Cost: ' + '{:.2f}'.format(data_cost[enum]) + ', Time: ' + '{:.2f}'.format(data_time[enum]*1000) + ' ms')
    fig.tight_layout(pad=0.5)
    fig.set_size_inches(8, 6.4)
    plt.savefig('map_result.png', bbox_inches='tight', dpi=120)
    plt.show()


def save_time_graph(data_x, data_y, title, x_label, x_lim, data_a=None, data_b=None):
    plt.plot(data_x, data_y)
    if data_a is not None and data_b is not None:
        plt.plot(data_a, data_b)
    plt.xlabel(x_label)
    plt.xlim(x_lim)
    plt.ylabel('Time in ms')
    plt.title(title)
    plt.savefig(title.replace(' ', '_'), bbox_inches='tight', dpi=120)
    plt.show()


def tabu_test_time_tabu_list(tabu_min, tabu_max, tabu_iter, test_iter=5):
    data = list()
    for i in range(tabu_min, tabu_max, tabu_iter):
        testing_map = my.create_map(1000, 1000, 100)
        average_time = 0
        for j in range(test_iter):
            timer_zero = time.time()
            my.tabu_search(testing_map, 100, i)
            average_time += (time.time() - timer_zero) * 1000
        data.append(average_time / test_iter)
    save_time_graph(range(tabu_min, tabu_max, tabu_iter), data, 'Tabu list time test',
                    'Tabu list size', [tabu_min, tabu_max])


def tabu_test_time_iterations(iter_min, iter_max, iter_i, test_iter=5):
    total_time, result = list(), list()
    testing_map = my.create_map(200, 200, 20)
    for i in range(iter_min, iter_max, iter_i):
        average_time, average_result = 0, 0
        for j in range(test_iter):
            timer_zero = time.time()
            average_result += my.tabu_search(testing_map, 20, 10, i, time_limit=30)[0]
            average_time += (time.time() - timer_zero) * 1000
        result.append((average_result / 1000) / test_iter)
        total_time.append(average_time / test_iter)

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(range(iter_min, iter_max, iter_i), total_time)
    axs[0].set(xlim=[iter_min, iter_max], title='Tabu iteration times',
               xlabel='Iterations of generating neighbours', ylabel='Time in ms')
    axs[1].plot(range(iter_min, iter_max, iter_i), result)
    axs[1].set(xlim=[iter_min, iter_max], title='Tabu iteration results',
               xlabel='Iterations of generating neighbours', ylabel='Final result')
    fig.tight_layout(pad=0.5)
    fig.set_size_inches(8, 6.4)
    plt.savefig('tabu_iterations_time.png', bbox_inches='tight', dpi=120)
    plt.show()


def map_test():
    data = list()
    print("Map tester\nEnter x, y, towns: ", end='')
    args = input().replace(',', ' ').split()
    args = [int(args[i]) for i in range(3)]
    timer_zero = time.time()
    testing_map = my.create_map(args[0], args[1], args[2])
    create_time = time.time() - timer_zero
    print("Enter neighbourhood size: ", end='')
    perm_count = input()
    perm_count = int(perm_count)
    timer_zero = time.time()
    hill_result = my.hill_climbing(testing_map, perm_count)
    hill_time = time.time() - timer_zero
    print("Enter tabu list size: ", end='')
    tabu_list_size = input()
    tabu_list_size = int(tabu_list_size)
    print("Enter tabu iteration limit (default 100): ", end='')
    iterations = input()
    iterations = 100 if iterations == "" else int(iterations)
    timer_zero = time.time()
    tabu_result = my.tabu_search(testing_map, perm_count, tabu_list_size, iterations)
    tabu_time = time.time() - timer_zero
    print("Enter initial temperature and alpha: ", end='')
    sa_args = input().replace(',', ' ').split()
    sa_args = [int(sa_args[0]), float(sa_args[1])]
    timer_zero = time.time()
    sa_result = my.simulated_annealing(testing_map, perm_count, sa_args[0], sa_args[1])
    sa_time = time.time() - timer_zero
    data.extend([testing_map, hill_result[1], tabu_result[1], sa_result[1]])
    data.extend([my.distance_path(testing_map), hill_result[0], tabu_result[0], sa_result[0]])
    data.extend([create_time, hill_time, tabu_time, sa_time])
    save_map_graphs(data, args[0], args[1], args[2] + 1)


def tabu_test():
    print("Tabu tester\nlist - tabu list time test\niter - tabu iteration time test")
    tabu_test_time_iterations(5, 500, 1, 5)


def tester():
    while True:
        print("\n\n\n\n")
        print("Main tester\nhill - hill climbing testing\ntabu - tabu search testing\nsa - simulated annealing testing"
              + "\nmap - print a map of all algorithms\nexit - exit program\nPlease select an option: ", end='')
        option = input()
        print("\n\n\n\n")
        if option == "map":
            map_test()
        elif option == "hill":
            pass
        elif option == "tabu":
            pass
        elif option == "sa":
            pass
        elif option == "exit":
            break


tester()

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
               xlabel='Cost: ' + '{:.2f}'.format(data_cost[enum]) + ', Time: ' + '{:.2f}'.format(
                   data_time[enum] * 1000) + ' ms')
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


def two_graphs(data, x_lim, x_label, y_label1, y_label2, title1, title2):
    fig, (ax0, ax1) = plt.subplots(2, 1)
    ax0.plot(data[0], data[1])
    ax0.set(xlim=x_lim, title=title1, xlabel=x_label, ylabel=y_label1)
    ax0.xaxis.set_major_formatter("{x:.0f}")
    ax1.plot(data[0], data[2])
    ax1.set(xlim=x_lim, title=title2, xlabel=x_label, ylabel=y_label2)
    ax1.xaxis.set_major_formatter("{x:.0f}")
    fig.tight_layout(pad=0.5)
    fig.set_size_inches(8, 6.4)
    plt.savefig(title1.replace(' ', '_') + '.png', bbox_inches='tight', dpi=120)
    plt.show()


def map_input():
    print("Enter x, y, towns: ", end='')
    args = input().replace(',', ' ').split()
    args = [int(args[i]) for i in range(len(args))]
    print("Enter neighbourhood size: ", end='')
    perm_count = input()
    args.append(int(perm_count))
    return args


def tabu_input():
    print("Enter min, max and step: ", end='')
    args = input().replace(',', ' ').split()
    args = [int(args[i]) for i in range(3)]
    print("Enter num of tests to average: ", end='')
    average = input()
    args.append(int(average))
    return args


def hill_test():
    print("Hill tester - Neighbourhood tester")
    print("Enter x, y, towns: ", end='')
    args = input().replace(',', ' ').split()
    args = [int(args[i]) for i in range(len(args))]
    args.extend(tabu_input())
    pool = range(args[3], args[4], args[5])
    total_time, result = list(), list()
    testing_map = my.create_map(args[0], args[1], args[2])
    for i in pool:
        average_time, average_result = 0, 0
        for j in range(args[6]):
            timer_zero = time.time()
            average_result += my.hill_climbing(testing_map, i)[0]
            average_time += (time.time() - timer_zero) * 1000
        result.append((average_result / 1000) / args[3])
        total_time.append(average_time / args[3])
    two_graphs([pool, total_time, result], [args[3], args[4]], 'Neighbours', 'Time in ms', 'Final result',
               'Hill climbing neighbours time', 'Hill climbing neighbours results')


def tabu_test_time_tabu_list():
    data = list()
    print("Tabu list size tester")
    map_args = map_input()
    args = tabu_input()
    print("Enter tabu iterations limit: ", end='')
    iterations = input()
    args.append(int(iterations))
    pool = range(args[0], args[1], args[2])
    testing_map = my.create_map(map_args[0], map_args[1], map_args[2])
    for i in pool:
        average_time, average_result = 0, 0
        for j in range(args[3]):
            timer_zero = time.time()
            my.tabu_search(testing_map, map_args[3], i)
            average_time += (time.time() - timer_zero) * 1000
        data.append(average_time / args[3])
    save_time_graph(pool, data, 'Tabu list time test', 'Tabu list size', [args[0], args[1]])


def tabu_test_time_iterations():
    print("Tabu iterations tester")
    map_args = map_input()
    args = tabu_input()
    print("Enter tabu list size: ", end='')
    tabu_limit = input()
    args.append(int(tabu_limit))
    pool = range(args[0], args[1] + 1, args[2])
    total_time, result = list(), list()
    testing_map = my.create_map(map_args[0], map_args[1], map_args[2])
    for i in pool:
        average_time, average_result = 0, 0
        for j in range(args[3]):
            timer_zero = time.time()
            average_result += my.tabu_search(testing_map, map_args[3], args[4], i, time_limit=30)[0]
            average_time += (time.time() - timer_zero) * 1000
        result.append((average_result / 1000) / args[3])
        total_time.append(average_time / args[3])
    two_graphs([pool, total_time, result], [args[0], args[1]], 'Iterations of generating neighbours', 'Time in ms', 'Final result',
               'Tabu iteration time', 'Tabu iteration results')


def map_test():
    data = list()
    print("Map tester")
    args = map_input()
    timer_zero = time.time()
    testing_map = my.create_map(args[0], args[1], args[2])
    create_time = time.time() - timer_zero
    timer_zero = time.time()
    hill_result = my.hill_climbing(testing_map, args[3])
    hill_time = time.time() - timer_zero
    print("Enter tabu list size: ", end='')
    tabu_list_size = input()
    tabu_list_size = int(tabu_list_size)
    print("Enter tabu iteration limit (default 100): ", end='')
    iterations = input()
    iterations = 100 if iterations == "" else int(iterations)
    timer_zero = time.time()
    tabu_result = my.tabu_search(testing_map, args[3], tabu_list_size, iterations)
    tabu_time = time.time() - timer_zero
    print("Enter initial temperature and alpha: ", end='')
    sa_args = input().replace(',', ' ').split()
    sa_args = [int(sa_args[0]), float(sa_args[1])]
    timer_zero = time.time()
    sa_result = my.simulated_annealing(testing_map, args[3], sa_args[0], sa_args[1])
    sa_time = time.time() - timer_zero
    data.extend([testing_map, hill_result[1], tabu_result[1], sa_result[1]])
    data.extend([my.distance_path(testing_map), hill_result[0], tabu_result[0], sa_result[0]])
    data.extend([create_time, hill_time, tabu_time, sa_time])
    save_map_graphs(data, args[0], args[1], args[2] + 1)


def tabu_test():
    while True:
        print(
            "\nTabu tester\nlist - tabu list time test\niter - tabu iteration time test\nback - to return to main tester\nPlease select an option: ",
            end='')
        option = input()
        print("")
        if "list" in option:
            tabu_test_time_tabu_list()
        elif "iter" in option:
            tabu_test_time_iterations()
        elif "back" in option:
            return


def tester():
    while True:
        print("\n\n\n\n")
        print("Main tester\nhill - hill climbing testing\ntabu - tabu search testing\nsa - simulated annealing testing"
              + "\nmap - print a map of all algorithms\nexit - exit program\nPlease select an option: ", end='')
        option = input()
        print("\n\n\n\n")
        if "map" in option:
            map_test()
        elif "hill" in option:
            hill_test()
        elif "tabu" in option:
            tabu_test()
        elif "sa" in option:
            pass
        elif "exit" in option:
            break


tester()

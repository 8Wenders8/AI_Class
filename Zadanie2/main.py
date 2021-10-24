import random
import time
import queue


class Node:
    def __init__(self, deck, move="", parent=None):
        self.state = deck
        if parent is None: self.moves = move
        else: self.moves = parent.moves + move
        self.value = 0

    # Functions for PriorityQueue, so it can compare nodes
    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value < other.value or self.value == other.value

    def __ge__(self, other):
        return self.value > other.value or self.value == other.value

    def create_children_nodes(self):
        # Create queue of children nodes for all possible moves
        children = queue.Queue()
        for move in self.state.moves:
            new_deck = Puzzle(self.state.x, self.state.y, self.state.move(move), self.state.goal)
            if not new_deck.gap[0] == self.state.gap[0] or not new_deck.gap[1] == self.state.gap[1]:
                children.put(Node(new_deck, move, self))
        return children

    # If all squares are in place, the puzzle is finished
    def is_finished(self):
        return self.heuristic1() == 0

    def get_cost(self, heuristic):
        if heuristic == 1: return self.heuristic1()
        if heuristic == 2: return self.heuristic2()
        if heuristic == 3: return self.heuristic1() + self.heuristic2()

    def heuristic1(self):
        sum_same = 0
        for ix, row in enumerate(self.state.deck):
            for iy, value in enumerate(row):
                if not value == self.state.goal[ix][iy]: sum_same += 1
        return sum_same

    def heuristic2(self):
        xy_start, xy_end, total_sum = {}, {}, 0
        # For the actual deck and the end deck, fill dictionary with deck value as key and position as dict value
        for ix, row in enumerate(self.state.deck):
            for iy, value in enumerate(row):
                if not value == 0: xy_start[value] = [ix, iy]
        for ix, row in enumerate(self.state.goal):
            for iy, value in enumerate(row):
                if not value == 0: xy_end[value] = [ix, iy]
        # Sort both dictionaries so we can iterate through them and compare
        xy_start, xy_end = dict(sorted(xy_start.items())), dict(sorted(xy_end.items()))
        for i in range(1, self.state.x * self.state.y):
            total_sum += abs(xy_start[i][0] - xy_end[i][0]) + abs(xy_start[i][1] - xy_end[i][1])
        return total_sum


class Puzzle:
    def __init__(self, x, y, deck=None, goal=None):
        self.deck, self.goal = deck, goal
        self.x, self.y = x, y
        if deck is not None: self.gap = self.get_gap_pos()
        self.moves = {"U": self.up, "D": self.down, "L": self.left, "R": self.right}

    # Print out the puzzle
    def puzzle_print(self, name):
        print(name + ":\t\t\t\tEnd:")
        for i, row in enumerate(self.deck):
            print(row, "\t\t\t", self.goal[i])

    # Manually set start deck and goal deck
    def set_deck_goal(self, deck, goal):
        self.deck, self.goal = deck, goal
        self.gap = self.get_gap_pos()

    # Get the position of the gap square ( 0 value )
    def get_gap_pos(self):
        for ix, row in enumerate(self.deck):
            for iy, value in enumerate(row):
                if value == 0: return [ix, iy]

    # Functions for manipulating squares in puzzle
    def swap(self, x1, y1):
        new_list = [row[:] for row in self.deck]
        temp = new_list[self.gap[0]][self.gap[1]]
        new_list[self.gap[0]][self.gap[1]] = new_list[x1][y1]
        new_list[x1][y1] = temp
        return new_list

    def up(self):
        if not self.gap[0] == 0: return self.swap(self.gap[0] - 1, self.gap[1])
        else: return [row[:] for row in self.deck]

    def down(self):
        if not self.gap[0] == self.x - 1: return  self.swap(self.gap[0] + 1, self.gap[1])
        else: return [row[:] for row in self.deck]

    def left(self):
        if not self.gap[1] == 0: return self.swap(self.gap[0], self.gap[1] - 1)
        else: return [row[:] for row in self.deck]

    def right(self):
        if not self.gap[1] == self.y - 1: return self.swap(self.gap[0], self.gap[1] + 1)
        else: return [row[:] for row in self.deck]

    # If a move exist, call the function for given move
    def move(self, move):
        if move in self.moves: return self.moves[move]()


def deck_generator(x, y):
    choices = random.sample(list(range(0, x * y)), k=x * y)  # Randomly arranged list [1,7,3,8,4,5]
    return [choices[i:i + y] for i in range(0, x * y, y)]  # Make sub lists [[1,7,3],[8,4,5]]


def greedy_solve(puzzle, heuristic):
    counter, act, visited = 1, Node(puzzle), list()
    choices = queue.PriorityQueue()
    act.value = act.get_cost(heuristic)
    choices.put((act.value, counter, act))
    timeout = time.time() + 15
    while time.time() < timeout:
        if choices.empty(): break
        act = choices.get()[2]
        if act.is_finished():
            act.state.puzzle_print("Result")
            print("Steps: ", str(len(act.moves)), "Moves: ", act.moves)
            return True
        elif act.state.deck not in visited:
            # Debug - Uncomment to see moves made during solving puzzle
            # print(counter, act.value, act.state.deck, act.moves)
            visited.append(act.state.deck)
            children = act.create_children_nodes()
            while not children.empty():
                counter += 1
                child = children.get()
                child.value = child.get_cost(heuristic)
                choices.put((child.value, counter, child))
    print("Solution wasn't found")
    return False


def tester(min_size, max_size):
    i = min_size
    while i <= max_size:
        j = min_size
        while j <= max_size:
            start_deck, end_deck = deck_generator(i, j), deck_generator(i, j)
            start_timer = time.time()
            p = Puzzle(i, j, start_deck, end_deck)
            print("Heuristic 1\n")
            p.puzzle_print("Start")
            if greedy_solve(p, 1) is not False:
                print("Time elapsed: " + str(time.time() - start_timer) + "\nHeuristic 2\n")
                start_timer = time.time()
                greedy_solve(p, 2)
                print("Time elapsed: " + str(time.time() - start_timer) + "\nHeuristic 3\n")
                start_timer = time.time()
                greedy_solve(p, 3)
                print("Time elapsed: " + str(time.time() - start_timer))
                j += 1
        i += 1


tester(2, 3)

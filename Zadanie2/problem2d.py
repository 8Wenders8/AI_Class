import random

class Node:
    def __init__(self, deck, move="", parent=None):
        self.state = deck
        if parent == None:
            self.depth = 0
            self.moves = move
        else:
            self.depth = parent.depth
            self.moves = parent.moves + move

class Puzzle:
    def __init__(self, x , y):
        self.deck = self.deckGenerator(x,y)
        self.goal = self.deckGenerator(x,y)
        self.x = x
        self.y = y
        self.moves = {"U":self.up, "D":self.down, "L":self.left, "R":self.right}

    def deckGenerator(self, x,y):
        choices = random.sample(list(range(0,x*y)), k=x*y) # Randomly aranged list [1,7,3,8,4,5]
        return [choices[i:i+y] for i in range(0,x*y,y)] # Make sub lists [[1,7,3],[8,4,5]]

    def isFinished(self):
        return heuristicsNo1(self.deck,self.goal) == 0

    def getGapPos(self):
        for ix, row in enumerate(self.deck):
            for iy, value in enumerate(row):
                if value == 0: return [ix,iy]


    def swap(self, x1, y1, x2, y2):
        temp = self.deck[x1][y1]
        self.deck[x1][y1] = self.deck[x2][y2]
        self.deck[x2][y2] = temp

    def up(self):
        gapPos = self.getGapPos()
        if not gapPos[0] == 0: self.swap(gapPos[0], gapPos[1], gapPos[0] -1 , gapPos[1])

    def down(self):
        gapPos = self.getGapPos()
        if not gasPos[0] == self.x - 1: self.swap(gapPos[0], gapPos[1], gapPos[0] + 1, gapPos[1])

    def left(self):
        gapPos = self.getGapPos()
        if not gapPos[1] == 0 : self.swap(gapPos[0], gapPos[1], gapPos[0], gapPos[1] - 1 )

    def right(self):
        gapPos = self.getGapPos()
        if not gapPos[1] == self.y - 1: self.swap(gapPos[0], gapPos[1], gapPos[0], gapPos[1] + 1)

    def move(self, move):
        if move is self.moves: self.moves[move]()

        
    def puzzlePrint(self):
        print("Start:\t\t\tEnd:")
        for i,row in enumerate(self.deck): 
            print(row, "\t\t", self.goal[i])


def isSolvable(flatStart, flatEnd, y):
    sumStart, sumEnd  = 0, 0 
    for index, value in enumerate(flatStart):
        if value == 0:
            sumStart += (index // y) + 1
            continue
        for j in range(index - 1, -1, -1):
            if flatStart[j] > value and not flatStart[j] == 0: sumStart += 1
    for index, value in enumerate(flatEnd):
        if value == 0:
            sumEnd += (index // y) + 1
            continue
        for j in range(index -1, -1, -1):
            if flatEnd[j] > value and not flatEnd[j] == 0: sumEnd += 1
    print(sumStart, sumEnd)
    return sumStart % 2 == sumEnd % 2

def heuristicsNo1(start, end):
    sumSame = 0
    for ix, row in enumerate(start):
        for iy, value in enumerate(row):
            if not value == end[ix][iy]: sumSame += 1
    return sumSame

def heuristicsNo2(start, end,x,y):
    xyStart, xyEnd, totalSum = {}, {}, 0
    for ix,row in enumerate(start):
        for iy,value in enumerate(row): 
            if not value == 0: xyStart[value] = [ix,iy]
    for ix,row in enumerate(end):
        for iy,value in enumerate(row):
            if not value == 0: xyEnd[value] = [ix,iy]

    xyStart, xyEnd = dict(sorted(xyStart.items())),  dict(sorted(xyEnd.items()))
    #print("xyStart:", xyStart, "\nxyEnd:", xyEnd)
    for i in range(1, x*y): totalSum += abs(xyStart[i][0] - xyEnd[i][0]) + abs(xyStart[i][1] - xyEnd[i][1])
    return totalSum

        
def greedySolve(start, end):
    pass

x = 3
y = 3
#flatStart, flatEnd = [item for sublist in start for item in sublist], [item for sublist in end for item in sublist]
p = Puzzle(3,3)
p.puzzlePrint()
p.up()
p.puzzlePrint()
p.right()
p.up()
p.puzzlePrint()

#puzzlePrint(start, end)
#print(isSolvable(flatStart, flatEnd, y))
#print(heuristicsNo1(start, end))
#print(heuristicsNo2(start, end , x, y))

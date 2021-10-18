import random

def deckGenerator(x,y):
    choices = random.sample(list(range(0,x*y)), k=x*y)
    return [choices[i:i+y] for i in range(0,x*y,y)]

def heuristicsNo1(start, end,x,y):
    print("Start:", start, "\nEnd:",end)
    totalSum = 0
    xyStart = {}
    xyEnd = {}
    # For every number from range(0,x*y) get posx posy, and diff them
    for i,e in enumerate(start):
        for j,ee in enumerate(e): 
            if not ee == 0: xyStart[ee] = [i,j]
    for i,e in enumerate(end):
        for j,ee in enumerate(e):
            if not ee == 0: xyEnd[ee] = [i,j]

    xyStart = dict(sorted(xyStart.items()))
    xyEnd = dict(sorted(xyEnd.items()))
    print("xyStart:", xyStart, "\nxyEnd:", xyEnd)
    for i in range(1, x*y):
        totalSum += abs(xyStart[i][0] - xyEnd[i][0]) + abs(xyStart[i][1] - xyEnd[i][1])

    print("Heuristika 2:",totalSum)

heuristicsNo1(deckGenerator(3,3),deckGenerator(3,3),3,3)

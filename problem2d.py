import random

def deckGenerator(x,y):
    choices = list(range(0,x*y))
    random.shuffle(choices)
    return [choices[i:i+y] for i in range(0, x*y,y)]


print(deckGenerator(3,3))

import numpy as np
import random

dick = np.zeros((15,9))
dick[0][6] += 1
dick[5][4] += 10

i = np.unravel_index(np.argmax(dick[0]),(3,3)) # gives (2,0)

test = []

test.append([[0,0,0],[0,0,0],[0,0,0]])
test.append([[0,0,0],[0,0,0],[0,0,0]])
test.append([[0,0,0],[0,0,0],[0,0,0]])
test.append([[0,0,0],[0,0,0],[0,0,0]])

test[1][1][2] += 1
meme = [[0,0,0],[0,0,1],[0,0,0]]

if meme in test:
    print("this actually works")

print(test.index(meme))

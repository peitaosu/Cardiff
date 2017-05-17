import os, sys
from differ import diff

def parameterize(file_diff):
    add = 0
    subtract = 0
    for line in file_diff:
        if line.startswith("+"):
            add += 1
        elif line.startswith("-"):
            subtract += 1
    print "add(+): " + str(add)
    print "subtract(-): " + str(subtract)


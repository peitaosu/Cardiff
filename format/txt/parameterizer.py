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

if __name__ == "__main__":
    txt_before = sys.argv[1]
    txt_after = sys.argv[2]
    txt_diff = diff(txt_before, txt_after)
    parameterize(txt_diff)

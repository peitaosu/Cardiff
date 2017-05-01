import os, sys

def parameterize(file_diff):
    with open(file_diff) as diff:
        add = 0
        subtract = 0
        for line in diff:
            if line.startswith("+"):
                add += 1
            elif line.startswith("-"):
                subtract += 1
        print "add(+): " + str(add)
        print "subtract(-): " + str(subtract)

if __name__ == "__main__":
    file_diff = sys.argv[1]
    parameterize(file_diff)
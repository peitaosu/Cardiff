import os, sys

def visualize(file_diff):
    default_editor = os.getenv('EDITOR')
    if default_editor:
        os.system('%s %s' % (default_editor, file_diff))
    else:
        with open(file_diff) as diff:
            for line in diff:
                print line

if __name__ == "__main__":
    file_diff = sys.argv[1]
    visualize(file_diff)
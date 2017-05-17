import os, sys, time
from differ import diff

def visualize(file_diff, file_after, file_output_name = None):
    default_editor = os.getenv('EDITOR')
    if default_editor:
        if file_output_name == None:
            file_output_name = str(time.time())
        with open(file_output_name + ".diff.txt", "w") as diff_file:
            for line in txt_diff:
                diff_file.write(line)
        os.system('%s %s' % (default_editor, file_output_name + ".diff.txt"))
    else:
        for line in file_diff:
            sys.stdout.write(line)


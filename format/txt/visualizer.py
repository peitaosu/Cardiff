import os, sys, time
from differ import diff

def visualize(file_diff, file_output_name = None):
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

if __name__ == "__main__":
    txt_before = sys.argv[1]
    txt_after = sys.argv[2]
    txt_diff = diff(txt_before, txt_after)
    try:
        file_output_name = sys.argv[3]
        visualize(txt_diff, file_output_name)
    except:
        visualize(txt_diff)
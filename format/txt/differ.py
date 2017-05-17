import sys, difflib

def diff(file_before, file_after):
    differ = difflib.Differ()
    with open(file_before) as f_before:
        with open(file_after) as f_after:
            diff_obj = differ.compare(f_before.read().splitlines(1), f_after.read().splitlines(1))
            result = list(diff_obj)
            length = len(result)
            for i in range(length):
                if not result[i].endswith("\n"):
                    result[i] += "\n"
            return result

def make_diff(file_before, file_after, file_output_name):
    txt_diff = diff(file_before, file_after)
    with open(file_output_name+".diff.txt", "w") as diff_file:
        for line in txt_diff:
            diff_file.write(line)
    return file_output_name + ".diff.txt"


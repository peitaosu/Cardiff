import sys, difflib

def diff(file_before, file_after):
    differ = difflib.Differ()
    with open(file_before) as f_before:
        with open(file_after) as f_after: 
            diff_obj = differ.compare(f_before.read().splitlines(1), f_after.read().splitlines(1))
            result = list(diff_obj)
            sys.stdout.writelines(result)

if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    diff(file_before, file_after)

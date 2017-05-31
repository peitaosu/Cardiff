from parser.aif_diff import AIF_DIFF

def parameterize(file_diff):
    """print formatted diff data

    args:
        file_diff (AIF_DIFF)
    """
    print "{:>48} : {:>14} <---> {:<14}".format("============ Parameters ============", "before", "after")
    for i in range(len(file_diff.attributes)):
        print "{:>48} : {:>14} <---> {:<14}".format(file_diff.description[i], getattr(file_diff, file_diff.attributes[i])[0], getattr(file_diff, file_diff.attributes[i])[1])
    print "{:>48} : {:>18}".format("Frame Changed", str(file_diff.frame_diff_count))

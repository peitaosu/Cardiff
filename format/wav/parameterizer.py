from parser.wav_diff import WAV_DIFF

def parameterize(file_diff):
    print "{:>48} : {:>8} <---> {:<8}".format("============ Parameters ============", "before", "after")
    for i in range(len(file_diff.attributes)):
        print "{:>48} : {:>8} <---> {:<8}".format(file_diff.description[i], getattr(file_diff, file_diff.attributes[i])[0], getattr(file_diff, file_diff.attributes[i])[1])
    print "{:>48} : {:>12}".format("Frame Changed", str(len(file_diff.frame_diff)))

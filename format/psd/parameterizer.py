import os, sys
from parser.psd_diff import PSD_DIFF

def parameterize(file_diff):
    print "{:>48} : {} ----> {}".format("============ Header ============", "before", "after")
    for field in file_diff.header.keys():
        print "{:>48} : {} ----> {}".format(file_diff.header_descriptions[field], file_diff.header[field]["before"], file_diff.header[field]["after"])

    print "{:>48} : {} ----> {}".format("============ Layers ============", "before", "after")
    for layer_id, layer_diff in file_diff.layer.iteritems():
        print "{:>48} : {}".format("Layer ID >>>", "<<< " + str(layer_id))
        for parameter, value in layer_diff["parameter"].iteritems():
            if parameter != "bbox":
                print "{:>48} : {} ----> {}".format(file_diff.layer_descriptions[parameter], str(value["before"]), str(value["after"]))
            else:
                print "{:>48} :".format(file_diff.layer_descriptions[parameter] + " >>>")
                for bbox_parameter in value["before"]:
                    print "{:>48} : {} ----> {}".format(file_diff.bbox_descriptions[bbox_parameter], str(value["before"][bbox_parameter]), str(value["after"][bbox_parameter]))
        if layer_diff["pixel"] == "Empty Layer.":
            print "{:>48} : {}".format("Pixel Changed", "Empty Layer.")
        else:
            print "{:>48} : {}".format("Pixel Changed", str(len(layer_diff["pixel"])))

import os, sys, time
from differ import diff
from parser.psd_diff import *
from PIL import Image, ImageTk
import Tkinter

def visualize_as_window(file_list_to_show):
    """visualize the psd diff, open with Tkinter window

    args:
        file_list_to_show (list)
    """
    for image in file_list_to_show:
        for file_ext in [".before.png", ".before.diff.png", ".after.diff.png", ".after.png"]:
            window = Tkinter.Tk()
            window.wm_title(image + file_ext)
            image_to_show = Image.open(image + file_ext)
            image_tk = ImageTk.PhotoImage(image_to_show)
            image_label = Tkinter.Label(window, image=image_tk)
            image_label.pack(side = "bottom", fill = "both", expand = "yes")
            window.mainloop()

def visualize_as_png(file_diff, file_after, file_output_name = None):
    """visualize the psd diff, open as psd file with alpha channel

    args:
        file_diff (PSD_DIFF)
        file_after (str)
        file_output_name (str)
    
    returns:
        png_file (list)
    """
    os.mkdir(file_output_name)
    diff_content = {}
    png_file_list = []
    for attr in ["header", "layer"]:
        diff_content[attr] = getattr(file_diff, attr)
    for layer_id in file_diff.layer.keys():
        if len(file_diff.layer_image[layer_id]) > 1:
            output_image = os.path.join(file_output_name, layer_id)
            file_diff.layer_image[layer_id]["before"].save(output_image + ".before.png")
            file_diff.layer_image[layer_id]["after"].save(output_image + ".after.png")
            diff_image_before = Image.new("RGBA", file_diff.layer_image[layer_id]["before"].size)
            diff_image_before_data = diff_image_before.load()
            diff_image_after = Image.new("RGBA", file_diff.layer_image[layer_id]["after"].size)
            diff_image_after_data = diff_image_after.load()
            width, height = diff_image_before.size
            pixel_index = 1
            for y in xrange(height):
                for x in xrange(width):
                    if str(pixel_index) in diff_content["layer"][layer_id]["pixel"]:
                        diff_image_before_data[x, y] = tuple(diff_content["layer"][layer_id]["pixel"][str(pixel_index)]["before"])
                        diff_image_after_data[x, y] = tuple(diff_content["layer"][layer_id]["pixel"][str(pixel_index)]["after"])
                    else:
                        diff_image_before_data[x, y] = (0, 0, 0, 0)
                        diff_image_after_data[x, y] = (0, 0, 0, 0)
                    pixel_index += 1
            diff_image_before.save(output_image + ".before.diff.png", "PNG")
            diff_image_after.save(output_image + ".after.diff.png", "PNG")
            png_file_list.append(output_image)
    return png_file_list

def visualize(file_diff, file_after, file_output_name = None):
    """visualize the psd diff, open with Tk window

    args:
        file_diff (PSD_DIFF)
        file_after (str)
        file_output_name (str)
    """
    if file_output_name == None:
        file_output_name = str(time.time())
    saved_file = visualize_as_png(file_diff, file_after, file_output_name)
    visualize_as_window(saved_file)

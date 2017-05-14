import os, sys, time
from differ import diff
from parser.png_diff import *
from PIL import Image, ImageTk
import Tkinter

def visualize_as_window(file_to_show):
    """visualize the png diff, open with Tkinter window

    args:
        file_to_show (str)
    """
    window = Tkinter.Tk()
    window.wm_title(file_to_show)
    image_to_show = Image.open(file_to_show)
    image_tk = ImageTk.PhotoImage(image_to_show)
    image_label = Tkinter.Label(window, image=image_tk)
    image_label.pack(side = "bottom", fill = "both", expand = "yes")
    window.mainloop()


def visualize_as_png(file_diff, file_after, file_output_name = None):
    """visualize the png diff, open as png file with alpha channel

    args:
        file_diff (PNG_DIFF)
        file_after (str)
        file_output_name (str)
    
    returns:
        png_file (str)
    """
    for attr in file_diff.attributes:
        if getattr(file_diff, attr)[0] != getattr(file_diff, attr)[1]:
            return
    image = Image.open(file_after)
    pixel_data = image.load()
    pixel_index = 1
    width, height = image.size
    for y in xrange(height):
        for x in xrange(width):
            if str(pixel_index) in file_diff.pixel_diff:
                pixel_index += 1
                continue
            else:
                pixel_index += 1
                pixel_data[x, y] = (pixel_data[x, y][0], pixel_data[x, y][1], pixel_data[x, y][2], 0)
    if file_output_name == None:
        file_output_name = str(time.time())
    image.save(file_output_name + ".diff.png", "PNG")
    return file_output_name + ".diff.png"

def visualize(file_diff, file_after, file_output_name = None):
    """visualize the png diff, open with Tk window

    args:
        file_diff (PNG_DIFF)
        file_after (str)
        file_output_name (str)
    """
    if file_output_name == None:
        file_output_name = str(time.time())
    saved_file = visualize_as_png(file_diff, file_after, file_output_name)
    visualize_as_window(saved_file)

if __name__ == "__main__":
    png_before = sys.argv[1]
    png_after = sys.argv[2]
    png_diff = PNG_DIFF()
    png_diff.diff(png_before, png_after)
    try:
        file_output_name = sys.argv[3]
        visualize(png_diff, sys.argv[2], file_output_name)
    except:
        visualize(png_diff, sys.argv[2])
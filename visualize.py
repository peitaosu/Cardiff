import os, sys, importlib, time
from PIL import Image, ImageTk
import Tkinter

def visualize_image(file_image):
    """visualize the image with Tk window

    args:
        file_image (str)
    """
    window = Tkinter.Tk()
    window.wm_title(file_image)
    image_to_show = Image.open(file_image)
    image_tk = ImageTk.PhotoImage(image_to_show)
    image_label = Tkinter.Label(window, image=image_tk)
    image_label.pack(side = "bottom", fill = "both", expand = "yes")
    window.mainloop()

def visualize_diff(file_before, file_diff_before, file_diff_after, file_after, file_ext, file_output_name = None):
    """visualize the file diff

    args:
        file_before (str)
        file_diff_before (str)
        file_diff_after (str)
        file_after (str)
        file_ext (str)
        file_output_name (str)
    
    returns:
        saved_file (list)
    """
    file_visualizer = importlib.import_module("format." + file_ext + ".visualizer")
    saved_file = file_visualizer.visualize(file_before, file_diff_before, file_diff_after, file_after)
    return saved_file

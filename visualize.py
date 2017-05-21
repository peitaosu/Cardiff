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

def visualize_diff(file_diff, file_after, file_ext, file_output_name = None):
    """visualize the file diff

    args:
        file_diff (object)
        file_after (str)
        file_ext (str)
        file_output_name (str)
    
    returns:
        saved_file (str)
    """
    file_visualizer = importlib.import_module("format." + file_ext + ".visualizer")
    if file_output_name == None:
        file_output_name = str(time.time())
    saved_file = file_visualizer.visualize(file_diff, file_after, file_output_name)
    return saved_file

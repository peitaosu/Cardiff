import os
import sys
import time
from differ import diff
from parser.psd import *
from parser.psd_diff import *
from PIL import Image, ImageTk
import Tkinter
import shutil


def visualize_as_window(file_list_to_show):
    """visualize the psd diff, open with Tkinter window

    args:
        file_list_to_show (list)
    """
    layer_count = int(len(file_list_to_show)/4)
    for index in range(layer_count):
        image_before_path = file_list_to_show[index*4 + 0]
        image_before_diff_path = file_list_to_show[index*4 + 1]
        image_after_diff_path = file_list_to_show[index*4 + 2]
        image_after_path = file_list_to_show[index*4 + 3]
        window = Tkinter.Tk()
        window.wm_title("PSD DIFF")
        width, height = Image.open(image_before_path).size
        ratio = width / height
        width = int(window.winfo_screenwidth() * 0.96 / 4)
        height = width / ratio
        image_before = Image.new("RGB", (width, height))
        image_before_diff = Image.new("RGB", (width, height))
        image_after_diff = Image.new("RGB", (width, height))
        image_after = Image.new("RGB", (width, height))
        for x in range(width):
            for y in range(height):
                if x / 16 % 2 == y / 16 % 2:
                    image_before.load()[x, y] = image_before_diff.load()[x, y] = image_after_diff.load()[
                        x, y] = image_after.load()[x, y] = (192, 192, 192)
                else:
                    image_before.load()[x, y] = image_before_diff.load()[x, y] = image_after_diff.load()[
                        x, y] = image_after.load()[x, y] = (255, 255, 255)
        image_before.paste(Image.open(image_before_path).resize((width, height), Image.ANTIALIAS), (0, 0),
                           Image.open(image_before_path).convert('RGBA').resize((width, height), Image.ANTIALIAS))
        image_before_diff.paste(Image.open(image_before_diff_path).resize((width, height), Image.ANTIALIAS),
                                (0, 0), Image.open(image_before_diff_path).convert('RGBA').resize((width, height), Image.ANTIALIAS))
        image_after_diff.paste(Image.open(image_after_diff_path).resize((width, height), Image.ANTIALIAS),
                               (0, 0), Image.open(image_after_diff_path).convert('RGBA').resize((width, height), Image.ANTIALIAS))
        image_after.paste(Image.open(image_after_path).resize((width, height), Image.ANTIALIAS), (0, 0),
                          Image.open(image_after_path).convert('RGBA').resize((width, height), Image.ANTIALIAS))
        image_tk_before = ImageTk.PhotoImage(image_before)
        image_tk_before_diff = ImageTk.PhotoImage(image_before_diff)
        image_tk_after_diff = ImageTk.PhotoImage(image_after_diff)
        image_tk_after = ImageTk.PhotoImage(image_after)
        image_label = Tkinter.Label(window, image=image_tk_before)
        image_label.pack(side="left", fill="both", expand="yes")
        image_label = Tkinter.Label(window, image=image_tk_before_diff)
        image_label.pack(side="left", fill="both", expand="yes")
        image_label = Tkinter.Label(window, image=image_tk_after_diff)
        image_label.pack(side="left", fill="both", expand="yes")
        image_label = Tkinter.Label(window, image=image_tk_after)
        image_label.pack(side="left", fill="both", expand="yes")
        window.mainloop()


def visualize_as_png(file_diffs, file_output_name=None):
    """visualize the psd diff, open as psd file with alpha channel

    args:
        file_diffs (list)
        file_output_name (str)

    returns:
        saved_file_list (list)
    """
    saved_file_list = []
    file_path = os.path.dirname(file_diffs[0])
    if file_path != file_output_name:
        for file_exist in file_diffs:
            dest_path = os.path.join(file_output_name, os.path.basename(file_exist))
            if os.path.exists(dest_path):
                os.remove(dest_path)
            shutil.copy(file_exist, os.path.join(dest_path))
            saved_file_list.append(dest_path)
    return saved_file_list


def visualize(file_before, file_after, file_diffs, file_output_name=None):
    """visualize the psd diff, open with Tk window

    args:
        file_before (str)
        file_after (str)
        file_diffs (list)
        file_output_name (str)
    """
    if file_output_name == None:
        visualize_as_window(file_diffs)
    else:
        visualize_as_png(file_diffs, file_output_name)


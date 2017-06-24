import os
import shutil
import Tkinter
from PIL import Image, ImageTk


def visualize_image_as_window(file_to_show):
    """visualize the image diff, open with Tkinter window

    args:
        file_to_show (list)
    """
    window = Tkinter.Tk()
    window.wm_title("IMAGE DIFF")
    width, height = Image.open(file_to_show[0]).size
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
                    x, y] = image_after.load()[x, y] = (220, 220, 220)
            else:
                image_before.load()[x, y] = image_before_diff.load()[x, y] = image_after_diff.load()[
                    x, y] = image_after.load()[x, y] = (255, 255, 255)
    image_before.paste(Image.open(file_to_show[0]).resize((width, height), Image.ANTIALIAS), (0, 0),
                       Image.open(file_to_show[0]).convert('RGBA').resize((width, height), Image.ANTIALIAS))
    image_before_diff.paste(Image.open(file_to_show[1]).resize((width, height), Image.ANTIALIAS),
                            (0, 0), Image.open(file_to_show[1]).convert('RGBA').resize((width, height), Image.ANTIALIAS))
    image_after_diff.paste(Image.open(file_to_show[2]).resize((width, height), Image.ANTIALIAS),
                           (0, 0), Image.open(file_to_show[2]).convert('RGBA').resize((width, height), Image.ANTIALIAS))
    image_after.paste(Image.open(file_to_show[3]).resize((width, height), Image.ANTIALIAS), (0, 0),
                      Image.open(file_to_show[3]).convert('RGBA').resize((width, height), Image.ANTIALIAS))
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


def visualize_image_as_png(file_diff_before, file_diff_after, file_output_name):
    """visualize the image diff, save as png file with alpha channel

    args:
        file_diff_before (str)
        file_diff_after (str)
        file_output_name (str)

    returns:
        file_output_list (list)
    """
    file_output_list = [file_output_name + ".before.diff.png",
                        file_output_name + ".after.diff.png"]
    if file_diff_before != file_output_name + ".before.diff.png":
        for file_exist in file_output_list:
            if os.path.exists(file_exist):
                os.remove(file_exist)
        shutil.copy(file_diff_before, file_output_name + ".before.diff.png")
        shutil.copy(file_diff_after, file_output_name + ".after.diff.png")
    return file_output_list


def create_diff_image(image_mode, image_size, pixel_changes, output_file, coord_reversed = None):
    diff_image_before = Image.new("RGBA", image_size)
    diff_image_after = Image.new("RGBA", image_size)
    width, height = image_size
    pixel_index = 1
    if coord_reversed == "y":
        y_range = reversed(xrange(height))
    else:
        y_range = xrange(height)
    if coord_reversed == "x":
        x_range = reversed(xrange(width))
    else:
        x_range = xrange(width)
    for y in y_range:
        for x in x_range:
            if str(pixel_index) in pixel_changes:
                if image_mode == "RGB":
                    diff_image_before.load()[x, y] = tuple(
                        pixel_changes[str(pixel_index)]["before"]) + (255,)
                    diff_image_after.load()[x, y] = tuple(
                        pixel_changes[str(pixel_index)]["after"]) + (255,)
                else:
                    diff_image_before.load()[x, y] = tuple(
                        pixel_changes[str(pixel_index)]["before"])
                    diff_image_after.load()[x, y] = tuple(
                        pixel_changes[str(pixel_index)]["after"])
            else:
                diff_image_before.load()[x, y] = diff_image_after.load()[
                    x, y] = (0, 0, 0, 0)
            pixel_index += 1
    diff_image_before.save(output_file + ".before.diff.png", "PNG")
    diff_image_after.save(output_file + ".after.diff.png", "PNG")
    return [output_file + ".before.diff.png", output_file + ".after.diff.png"]

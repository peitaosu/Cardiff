from PIL import Image, ImageTk
import Tkinter
import shutil
import os

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
    file_output_list = [file_output_name + ".before.diff.png", file_output_name + ".after.diff.png"] 
    if file_diff_before != file_output_name + ".before.diff.png":
        for file_exist in file_output_list:
            if os.path.exists(file_exist):
                os.remove(file_exist)
        shutil.copy(file_diff_before, file_output_name + ".before.diff.png")
        shutil.copy(file_diff_after, file_output_name + ".after.diff.png")
    return file_output_list

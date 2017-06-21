import os, sys, time
from differ import diff
from parser.psd_diff import *
from PIL import Image, ImageTk
import Tkinter
import shutil

def visualize_as_window(file_list_to_show):
    """visualize the psd diff, open with Tkinter window

    args:
        file_list_to_show (list)
    """
    for image in file_list_to_show:
        window = Tkinter.Tk()
        window.wm_title("PSD DIFF")
        width, height = Image.open(image + ".before.png").size
        ratio = width/height
        width = 256
        height = width/ratio
        image_before = Image.new("RGB", (width, height))
        image_before_diff = Image.new("RGB", (width, height))
        image_after_diff = Image.new("RGB",(width, height))
        image_after = Image.new("RGB",(width, height))
        for x in range(width):
            for y in range(height):
                if x/16%2 == y/16%2:
                    image_before.load()[x, y] = (192, 192, 192)
                    image_before_diff.load()[x, y] = (192, 192, 192)
                    image_after_diff.load()[x, y] = (192, 192, 192)
                    image_after.load()[x, y] = (192, 192, 192)
                else:
                    image_before.load()[x, y] = (255, 255, 255)
                    image_before_diff.load()[x, y] = (255, 255, 255)
                    image_after_diff.load()[x, y] = (255, 255, 255)
                    image_after.load()[x, y] = (255, 255, 255)
        image_before.paste(Image.open(image + ".before.png").resize((width, height)), (0, 0), Image.open(image + ".before.png").convert('RGBA').resize((width, height)))
        image_before_diff.paste(Image.open(image + ".before.diff.png").resize((width, height)), (0, 0), Image.open(image + ".before.diff.png").convert('RGBA').resize((width, height)))
        image_after_diff.paste(Image.open(image + ".after.diff.png").resize((width, height)), (0, 0), Image.open(image + ".after.diff.png").convert('RGBA').resize((width, height)))
        image_after.paste(Image.open(image + ".after.png").resize((width, height)), (0, 0), Image.open(image + ".after.png").convert('RGBA').resize((width, height)))
        image_tk_before = ImageTk.PhotoImage(image_before)
        image_tk_before_diff = ImageTk.PhotoImage(image_before_diff)
        image_tk_after_diff = ImageTk.PhotoImage(image_after_diff)
        image_tk_after = ImageTk.PhotoImage(image_after)
        image_label = Tkinter.Label(window, image=image_tk_before)
        image_label.pack(side = "left", fill = "both", expand = "yes")
        image_label = Tkinter.Label(window, image=image_tk_before_diff)
        image_label.pack(side = "left", fill = "both", expand = "yes")
        image_label = Tkinter.Label(window, image=image_tk_after_diff)
        image_label.pack(side = "left", fill = "both", expand = "yes")
        image_label = Tkinter.Label(window, image=image_tk_after)
        image_label.pack(side = "left", fill = "both", expand = "yes")
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
    if os.path.exists(file_output_name):
        shutil.rmtree(file_output_name)
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

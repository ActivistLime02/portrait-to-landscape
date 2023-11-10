# For changing directory, listing files in directories and deleting files
import os
# Run terminal commands
import subprocess
# To move files around
import shutil
# To use all the cpu cores available for parallel computing
from multiprocessing import Pool
import multiprocessing
# Parse arguments
import argparse
# Round upwards
import math
# pyoxipng, some linux distributions don't include oxipng in the standard repo. (debian 11 for example)
import oxipng
# Wand, binding for imagemagick
from wand.image import Image
from wand.color import Color
from wand.resource import limits
# measure time it takes to complete the script
import time
# Get most frequent thing from a list
from collections import Counter

# This script will consume a lot of resources
# Therefore I will set a high nice level
os.nice(20)

# Parse aguments for later use
parser = argparse.ArgumentParser(description="Python script for editing pictures to a specific resolution by adding blur to the sides.")
parser.add_argument("-x", "--width", required=True, type=int, dest="cmd_width")
parser.add_argument("-y", "--height", required=True, type=int, dest="cmd_height")
parser.add_argument("-f", "--file_format", choices=["png", "jxl"], required=True, type=str, dest="file_format")
args = parser.parse_args()

cmd_width = args.cmd_width
cmd_height = args.cmd_height
file_format = args.file_format

# Set single thread when editing images
limits['thread'] = 1

# Making a function because it will be used twice and for practice
def preprocess(to, image):
    with Image(filename=image) as img:
        width = img.width
        height = img.height
    if height < cmd_height and width < cmd_width:
        shutil.move(image, to)


print("Starting the script.")
os.chdir("input")
if __name__ == "__main__":
    with Pool() as pool:
        for image in os.listdir():
            pool.apply_async(preprocess, ("../1", image,))
        pool.close()
        pool.join()
for item in os.listdir():
    shutil.move(item, "../inbetween")
os.chdir("..")

upscaling_time_start = time.time()
print("Preperations are made for upscaling with waifu2x-ncnn-vulkan.")
while os.listdir("1") != []:
    subprocess.run(["waifu2x-ncnn-vulkan", "-i", "1", "-o", "2", "-f", "png"])
    os.chdir("1")
    for item in os.listdir():
        os.remove(item)
    os.chdir("../2")
    if __name__ == "__main__":
        with Pool() as pool:
            for image in os.listdir():
                pool.apply_async(preprocess, ("../1", image,))
            pool.close()
            pool.join()
    for item in os.listdir():
        shutil.move(item, "../inbetween")
    os.chdir("..")
upscaling_time_end = time.time()

editing_time_start = time.time()
print("I will now start to edit the pictures.")
os.chdir("inbetween")

# Convert the integers to strings so I can paste together a series of strings
str_cmd_width = str(cmd_width)
str_cmd_height = str(cmd_height)


def most_frequent_element_in_percent(list):
    frequency = Counter(list)
    most_frequent_element = frequency.most_common(1)[0][0]
    count = 0
    for element in list:
        if element == most_frequent_element:
            count += 1
    percent = count / len(list) * 100
    return percent


def most_frequent_color(list):
    frequency = Counter(list)
    most_frequent_color = frequency.most_common(1)[0][0]
    return most_frequent_color

def image_editing(image):
    with Image(filename=image) as test:
        # Test if image has any transparency
        transparency = False
        list_with_pixel_data = test.export_pixels(channel_map="A", storage="char")
        total_count = len(list_with_pixel_data)
        zero_count = 0
        for number in list_with_pixel_data:
            if number == 0:
                zero_count += 1
        percentage = round(zero_count / total_count * 100, 2)
        if percentage >= 5:
            transparency = True
        # Test if the image has any sides with the same color
        # Convert test.width to width as this is shorter same for height
        width = test.width
        height = test.height
        # north
        can_i_extend_north = False
        pixels_north = test.export_pixels(x=0, y=0, width=width, height=5, channel_map="RGB", storage="char")
        pixels_north_list = list(zip(*[iter(pixels_north)]*3))
        percentage = most_frequent_element_in_percent(pixels_north_list)
        if percentage >= 80:
            can_i_extend_north = True
        # east
        can_i_extend_east = False
        pixels_east = test.export_pixels(x=width, y=0, width=5, height=height, channel_map="RGB", storage="char")
        pixels_east_list = list(zip(*[iter(pixels_east)]*3))
        percentage = most_frequent_element_in_percent(pixels_east_list)
        if percentage >= 80:
            can_i_extend_east = True
        # south
        can_i_extend_south = False
        pixels_south = test.export_pixels(x=0, y=height, width=width, height=5, channel_map="RGB", storage="char")
        pixels_south_list = list(zip(*[iter(pixels_south)]*3))
        percentage = most_frequent_element_in_percent(pixels_south_list)
        if percentage >= 80:
            can_i_extend_south = True
        # west
        can_i_extend_west = False
        pixels_west = test.export_pixels(x=0, y=0, width=5, height=height, channel_map="RGB", storage="char")
        pixels_west_list = list(zip(*[iter(pixels_west)]*3))
        percentage = most_frequent_element_in_percent(pixels_west_list)
        if percentage >= 80:
            can_i_extend_west = True
        # north and south
        can_i_extend_north_south = False
        pixels_north_south_list = pixels_north_list + pixels_south_list
        percentage = most_frequent_element_in_percent(pixels_north_south_list)
        if percentage >= 80:
            can_i_extend_north_south = True
        # west and east
        can_i_extend_west_east = False
        pixels_west_east_list = pixels_west_list + pixels_east_list
        percentage = most_frequent_element_in_percent(pixels_west_east_list)
        if percentage >= 80:
            can_i_extend_west_east = True
    if transparency is True:
        with Image(width=cmd_width, height=cmd_height, pseudo="xc:black") as new_image:
            with Image(filename=image) as main_img:
                main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                new_image.composite(main_img, gravity="center")
            new_image.save(filename="../inbetween2/" + image[:-4] + ".png")
    elif cmd_width / cmd_height >= 1 and can_i_extend_west_east is True and transparency is False:
        color = most_frequent_color(pixels_west_east_list)
        string_color = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        with Color(string_color) as backgroud:
            with Image(width=cmd_width, height=cmd_height, background=backgroud) as new_image:
                with Image(filename=image) as main_img:
                    main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                    new_image.composite(main_img, gravity="center")
                new_image.save(filename="../inbetween2/" + image[:-4] + ".png")
    elif cmd_width / cmd_height < 1 and can_i_extend_north_south is True and transparency is False:
        color = most_frequent_color(pixels_north_south_list)
        string_color = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        with Color(string_color) as backgroud:
            with Image(width=cmd_width, height=cmd_height, background=backgroud) as new_image:
                with Image(filename=image) as main_img:
                    main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                    new_image.composite(main_img, gravity="center")
                new_image.save(filename="../inbetween2/" + image[:-4] + ".png")
    else:
        with Image(width=cmd_width, height=cmd_height) as new_image:
            with Image(filename=image) as blur_img:
                blur_img.transform(resize=str_cmd_width + "x" + str_cmd_height + "^")
                blur_img.blur(radius=0, sigma=25)
                new_image.composite(blur_img, gravity="center")
            with Image(filename=image) as main_img:
                main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                new_image.composite(main_img, gravity="center")
            new_image.save(filename="../inbetween2/" + image[:-4] + ".png")
    os.remove(image)

if __name__ == "__main__":
    with Pool() as pool:
        for image in os.listdir():
            pool.apply_async(image_editing, (image,))
        pool.close()
        pool.join()

os.chdir("..")
editing_time_end = time.time()

optimizing_time_start = time.time()
os.chdir("inbetween2")

if file_format == "jxl":
    print("I will now start processing files to jxl.")

    def optimize(image):
        new_image = image[:-4] + ".jxl"
        subprocess.run(["cjxl", image, new_image, "-d", "0", "-e", "8", "--num_threads=0"])
        shutil.move(new_image, "../output")
        os.remove(image)

    if __name__ == "__main__":
        with Pool() as pool:
            for image in os.listdir():
                pool.apply_async(optimize, (image,))
            pool.close()
            pool.join()

elif file_format == "png":
    print("I will now start optimizing the png pictures")

    def optimize(image):
        oxipng.optimize(image, level=5, strip=oxipng.StripChunks.safe())
        shutil.move(image, "../output")

    if __name__ == "__main__":
        if multiprocessing.cpu_count() <= 8:
            with Pool(1) as pool:
                for image in os.listdir():
                    pool.apply_async(optimize, (image,))
                pool.close()
                pool.join()
        else:
            number_of_threads = int(math.ceil(multiprocessing.cpu_count()/8))
            with Pool(number_of_threads) as pool:
                for image in os.listdir():
                    pool.apply_async(optimize, (image,))
                pool.close()
                pool.join()

optimizing_time_end = time.time()

upscaling_time = upscaling_time_end - upscaling_time_start
editing_time = editing_time_end - editing_time_start
optimizing_time = optimizing_time_end - optimizing_time_start
overall_time = optimizing_time_end - upscaling_time_start

print()
print("Files have been processed and ready in the output directory.")
print()
print("This scipt took", round(overall_time, 2), "seconds to compleet.")
print("Upscaling took", round(upscaling_time, 2), "seconds to compleet.")
print("Editing took", round(editing_time, 2), "seconds to compleet.")
print("Lossless compression took", round(optimizing_time, 2), "seconds to compleet.")

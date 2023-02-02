# For changing directory, listing files in directories and deleting files
import os
# Run terminal commands
import subprocess
# To get the width and height of a picture in pixels  !!!Will be replaced with wand
#from PIL import Image
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
# measure time it takes to complete the script
import time

# Parse aguments for later use
parser = argparse.ArgumentParser(description="Python script for editing pictures to a specific resolution by adding blur to the sides.")
parser.add_argument("-x", "--width", required=True, type=int, dest="cmd_width")
parser.add_argument("-y", "--height", required=True, type=int, dest="cmd_height")
parser.add_argument("-f", "--file_format", choices=["png", "jxl"], required=True, type=str, dest="file_format")
args = parser.parse_args()

cmd_width = args.cmd_width
cmd_height = args.cmd_height
file_format = args.file_format


# Making a function because it will be used twice and for practice
def preprocess(to) :
    for item in os.listdir() :        
        with Image(filename=item) as img :
            width = img.width
            height = img.height
        if height < cmd_height and width < cmd_width :
            shutil.move(item, to)

print("Starting the script.")
os.chdir("input")
preprocess("../1")
for item in os.listdir() :
    shutil.move(item, "../inbetween")
os.chdir("..")

upscaling_time_start = time.time()
print("Preperations are made for upscaling with waifu2x-ncnn-vulkan.")
while os.listdir("1") != [] :
    subprocess.run(["waifu2x-ncnn-vulkan","-i","1","-o","2","-f","png"])
    os.chdir("1")
    for item in os.listdir() :
        os.remove(item)
    os.chdir("../2")
    preprocess("../1")
    for item in os.listdir() :
        shutil.move(item, "../inbetween")
    os.chdir("..")
upscaling_time_end = time.time()

editing_time_start = time.time()
print("I will now start to edit the pictures.")
os.chdir("inbetween")

# Convert the integers to strings so I can paste together a series of strings
str_cmd_width = str(cmd_width)
str_cmd_height = str(cmd_height)

for item in os.listdir() :
    #subprocess.run(["convert","-size","3840x2160","xc:black",item,"-resize","3840x2160^","-blur","0x25","-gravity","center","-composite",item,"-geometry","3840x2160","-gravity","center","-composite","../inbetween2/" + item[:-4] + ".png"])
    #subprocess.run(["convert","-size",cmd_width+"x"+cmd_height,"xc:black",item,"-resize",cmd_width+"x"+cmd_height+"^","-blur","0x25","-gravity","center","-composite",item,"-geometry",cmd_width+"x"+cmd_height,"-gravity","center","-composite","../inbetween2/" + item[:-4] + ".png"])
    with Image(filename=item) as test :
        # Test if image has any transparency     
        transparency = False
        list_with_pixel_data = set(test.export_pixels(channel_map="A", storage="char"))
        for number in list_with_pixel_data :
            if number == 0 :
                transparency = True
        # Test if the image has any sides with the same color
        width = test.width
        height = test.height
        # north
        can_i_extend_north = False
        pixels_north = test.export_pixels(x=0, y=0, width=width, height=1, channel_map="RGB", storage="char")
        pixels_north_set = list(zip(*[iter(pixels_north)]*3))
        if len(set(pixels_north_set)) == 1 :
            can_i_extend_north = True
        # east
        can_i_extend_east = False
        pixels_east = test.export_pixels(x=width, y=0, width=1, height=height, channel_map="RGB", storage="char")
        pixels_east_set = list(zip(*[iter(pixels_east)]*3))
        if len(set(pixels_east_set)) == 1 :
            can_i_extend_east = True
        # south
        can_i_extend_south = False
        pixels_south = test.export_pixels(x=0, y=height, width=width, height=1, channel_map="RGB", storage="char")
        pixels_south_set = list(zip(*[iter(pixels_south)]*3))
        if len(set(pixels_south_set)) == 1 :
            can_i_extend_south = True
        # west
        can_i_extend_west = False
        pixels_west = test.export_pixels(x=0, y=0, width=1, height=height, channel_map="RGB", storage="char")
        pixels_west_set = list(zip(*[iter(pixels_west)]*3))
        if len(set(pixels_west_set)) == 1 :
            can_i_extend_west = True
        # north and south
        can_i_extend_north_south = False
        pixels_north_south_set = pixels_north_set + pixels_south_set
        if len(set(pixels_north_south_set)) == 1 :
            can_i_extend_north_south = True
        # west and east
        can_i_extend_west_east = False
        pixels_west_east_set = pixels_west_set + pixels_east_set
        if len(set(pixels_west_east_set)) == 1 :
            can_i_extend_west_east = True
    
    if transparency == True :
        with Image(width=cmd_width, height=cmd_height, pseudo="xc:black") as new_image :
            with Image(filename=item) as main_img :
                main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                new_image.composite(main_img, gravity="center")
            new_image.save(filename="../inbetween2/" + item[:-4] + ".png")
    
    elif cmd_width / cmd_height >= 1 and can_i_extend_west_east == True and transparency == False :
        color = pixels_west_east_set[0]
        string_color = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        with Color(string_color) as backgroud :
            with Image(width=cmd_width, height=cmd_height, background=backgroud) as new_image :
                with Image(filename=item) as main_img :
                    main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                    new_image.composite(main_img, gravity="center")
                new_image.save(filename="../inbetween2/" + item[:-4] + ".png")
    
    elif cmd_width / cmd_height < 1 and can_i_extend_north_south == True and transparency == False :
        color = pixels_north_south_set[0]
        string_color = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        with Color(string_color) as backgroud :
            with Image(width=cmd_width, height=cmd_height, background=backgroud) as new_image :
                with Image(filename=item) as main_img :
                    main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                    new_image.composite(main_img, gravity="center")
                new_image.save(filename="../inbetween2/" + item[:-4] + ".png")

    elif cmd_width / cmd_height < 1 and can_i_extend_north_south == False and can_i_extend_north == True and transparency == False :
        color = pixels_north_set[0]
        string_color = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        with Color(string_color) as backgroud :
            with Image(width=cmd_width, height=cmd_height, background=backgroud) as new_image :
                with Image(filename=item) as main_img :
                    main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                    new_image.composite(main_img, gravity="south")
                new_image.save(filename="../inbetween2/" + item[:-4] + ".png")

    else :
        with Image(width=cmd_width, height=cmd_height) as new_image :
            with Image(filename=item) as blur_img :
                blur_img.transform(resize=str_cmd_width + "x" + str_cmd_height + "^")
                blur_img.blur(radius=0,sigma=25)
                new_image.composite(blur_img, gravity="center")
            with Image(filename=item) as main_img :
                main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
                new_image.composite(main_img, gravity="center")
            new_image.save(filename="../inbetween2/" + item[:-4] + ".png")
    #with Image(width=cmd_width, height=cmd_height, pseudo="xc:black") as new_image :
    #    if transparency == False :
    #        with Image(filename=item) as blur_img :
    #            blur_img.transform(resize=str_cmd_width + "x" + str_cmd_height + "^")
    #            blur_img.blur(radius=0,sigma=25)
    #            new_image.composite(blur_img, gravity="center")
    #    with Image(filename=item) as main_img :
    #        main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
    #        new_image.composite(main_img, gravity="center")
    #    new_image.save(filename="../inbetween2/" + item[:-4] + ".png")
    os.remove(item)
os.chdir("..")
editing_time_end = time.time()

optimizing_time_start = time.time()
os.chdir("inbetween2")

if file_format == "jxl" :
    print("I will now start processing files to jxl.")
    def optimize(image) :
        new_image = image[:-4] + ".jxl"
        subprocess.run(["cjxl",image,new_image,"-d","0","-e","8"])
        shutil.move(new_image, "../output")
        os.remove(image)

    if __name__ == "__main__" :
        with Pool(round(multiprocessing.cpu_count()//4*3)) as pool :
            for image in os.listdir() :
                pool.apply_async(optimize, (image,))
            pool.close()
            pool.join()

elif file_format == "png" :
    print("I will now start optimizing the png pictures")
    def optimize(image) :
        #subprocess.run(["oxipng","-o","5","-s","safe",image])
        oxipng.optimize(image, level=5, strip=oxipng.Headers.safe())
        shutil.move(image, "../output")

    if __name__ == "__main__" :
        if multiprocessing.cpu_count() <= 8 :
            with Pool(1) as pool :
                for image in os.listdir() :
                    pool.apply_async(optimize, (image,))
                pool.close()
                pool.join()
        else :
            number_of_threads = int(math.ceil(multiprocessing.cpu_count()/8))
            with Pool(number_of_threads) as pool :
                for image in os.listdir() :
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
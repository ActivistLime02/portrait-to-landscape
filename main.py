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


print("I will now start to edit the pictures.")
os.chdir("inbetween")

# Convert the integers to strings so I can paste together a series of strings
str_cmd_width = str(cmd_width)
str_cmd_height = str(cmd_height)

for item in os.listdir() :
    #subprocess.run(["convert","-size","3840x2160","xc:black",item,"-resize","3840x2160^","-blur","0x25","-gravity","center","-composite",item,"-geometry","3840x2160","-gravity","center","-composite","../inbetween2/" + item[:-4] + ".png"])
    #subprocess.run(["convert","-size",cmd_width+"x"+cmd_height,"xc:black",item,"-resize",cmd_width+"x"+cmd_height+"^","-blur","0x25","-gravity","center","-composite",item,"-geometry",cmd_width+"x"+cmd_height,"-gravity","center","-composite","../inbetween2/" + item[:-4] + ".png"])
    with Image(width=cmd_width, height=cmd_height, pseudo="xc:black") as new_image :
        with Image(filename=item) as blur_img :
            blur_img.transform(resize=str_cmd_width + "x" + str_cmd_height + "^")
            blur_img.blur(radius=0,sigma=25)
            new_image.composite(blur_img, gravity="center")
        with Image(filename=item) as main_img :
            main_img.transform(resize=str_cmd_width + "x" + str_cmd_height)
            new_image.composite(main_img, gravity="center")
        new_image.save(filename="../inbetween2/" + item[:-4] + ".png")
    os.remove(item)
os.chdir("..")


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
        subprocess.run(["oxipng","-o","5","-s","safe",image])
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
print("Files have been processed and ready in the output directory.")
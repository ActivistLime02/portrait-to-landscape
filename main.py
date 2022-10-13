import os
# For changing directory, listing files in directories and deleting files
import subprocess
# Run terminal commands
from PIL import Image
# To get the width and height of a picture in pixels
import shutil
# To move files around
from multiprocessing import Pool
# To use all the cpu cores available for parallel computing

# Making a function because it will be used twice and for practice
def preprocess(to) :
    for item in os.listdir() :
        img = Image.open(item)
        width,height = img.size
        if height < 2160 and width < 3840 :
            shutil.move(item, to)

print("Starting the script.")
os.chdir("input")
preprocess("../1")
for item in os.listdir() :
    shutil.move(item, "../inbetween")
os.chdir("..")

print("Preperations are mode for upscaling with waifu2x-ncnn-vulkan.")
while os.listdir("1") != [] :
    subprocess.run(["waifu2x-ncnn-vulkan","-i","1","-o","2"])
    os.chdir("1")
    for item in os.listdir() :
        os.remove(item)
    os.chdir("../2")
    preprocess("../1")
    for item in os.listdir() :
        shutil.move(item, "../inbetween")
    os.chdir("..")

print("I will now start to edit the pictures.")
for item in os.listdir("inbetween") :
    
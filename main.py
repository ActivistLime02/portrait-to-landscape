import os
# For changing directory, listing files in directories and deleting files
import subprocess
# Run terminal commands
from PIL import Image
# To get the width and height of a picture in pixels
import shutil
# To move files around
from multiprocessing import Pool
import multiprocessing
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


print("Preperations are made for upscaling with waifu2x-ncnn-vulkan.")
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
os.chdir("inbetween")

for item in os.listdir() :
    subprocess.run(["convert","-size","3840x2160","xc:black",item,"-resize","3840x2160^","-blur","0x25","-gravity","center","-composite",item,"-geometry","3840x2160","-gravity","center","-composite","../inbetween2/"+item])
    os.remove(item)
os.chdir("..")


os.chdir("inbetween2")

print("I will now start processing files to jxl.")
def optimize(image) :
    new_image = image[:-4] + ".jxl"
    subprocess.run(["cjxl",image,new_image,"-d","0","-e","7"])
    shutil.move(new_image, "../output")
    os.remove(image)

if __name__ == "__main__" :
    with Pool((multiprocessing.cpu_count())) as pool :
        for image in os.listdir() :
            pool.apply_async(optimize, (image,))
        pool.close()
        pool.join()


# https://stackoverflow.com/questions/20886565/using-multiprocessing-process-with-a-maximum-number-of-simultaneous-processes
# https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing.pool
# https://youtu.be/X7vBbelRXn0
# These sources helped alot.

print("Files have been processed and ready in the output directory.")
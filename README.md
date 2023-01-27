# Portrait to landscape python
This is a rewriten version of my bash script doing the same thing but a little more optimized.
## What does it do?
This program takes a picture of any aspect ratio and change it to a custom resolution. Since this will use [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan) it is recommended to use anime/manga styled images.
## How to use
Firstly, use prepare-folders.py to create a couple of folders that the main script will use.
```
python prepare-folders.py
```
Then, place your images in the input directory. And specify the resolution with -x and -y arguments. -x for the horizontal pixels and -y for the vertical pixels. Specify the image format with -f, the options are png or jxl.
The images in the input directory will get deleted. If you need to keep the original pictures then please back it up in another directory that isn't made by the script. Run the script if you are ready.
```
python main.py -f jxl -x 3640 -y 2160 # For 4K image with jxl as file format
```
The processed images will be in the output folder.
## Dependencies
- `python`
- `imagemagick`
- `waifu2x-ncnn-vulkan`
- `oxipng`
- `libjxl` (for cjxl)
## Caviats
The script is made with usage on Linux in mind. Theoretically this should work in any other OS as long as the dependencies are in your PATH.
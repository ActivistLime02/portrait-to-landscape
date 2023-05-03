# Portrait to landscape python
## What does it do?
This program takes a picture of any aspect ratio and change it to a custom resolution. Since this will use [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan) it is recommended to use anime/manga styled images.
## How to use
### Preperation
Firstly, you will need to download this repository.
```
git clone https://github.com/ActivistLime02/portrait-to-landscape.git
cd portrait-to-landscape
```
I recommend you to make a virtual environment for this script. This make sure that any packages that will be installed via pip will not interfere with other programs installed on your computer.
The below command wil create a virtual environment called env. I will also assume that you will be using bash. If you use fish for example you need to append `.fish` after `env/bin/activate`.
```
python -m venv env
source env/bin/activate
```
Now that we are in the virtual environment we can install our pip packages for this script. When installing packages via pip in a virtual environment, the packages will be installed the folder env. That's the name we chose earlier.
Later when you want to continue using this script. You need to repeat the last command.
```
pip install -r requirements.txt
```
### Script
Use prepare-folders.py to create a couple of folders that the main script will use.
```
python prepare-folders.py
```
Then, place your images in the `input` directory. Specify the resolution with -x and -y arguments. -x for the horizontal pixels and -y for the vertical pixels. Specify the image format with -f, the options are png or jxl.
The images in the input directory will get deleted. If you need to keep the original pictures then please back it up in another directory that isn't made by the script. Run the script if you are ready.
```
python main.py -f png -x 3840 -y 2160 # For 4K image with png as file format
```
The processed images will be in the output folder.
## Dependencies
### requirements.txt
This will be automatically installed when following the how to.
- `pyoxipng`
- `Wand`
### System
- `python`
- `imagemagick`
- `waifu2x-ncnn-vulkan`
- `libjxl` (for cjxl)
## Caviats
The script is made with usage on Linux in mind. Theoretically this should work in any other OS as long as the dependencies are in your PATH.

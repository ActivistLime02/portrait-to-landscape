# portrait-to-landscape

## What does it do?

This program takes a picture of any aspect ratio and makes it 16:9 in 4K resolution. Since this will use [waifu2x](https://github.com/nihui/waifu2x-ncnn-vulkan) it is recommended to use anime/manga styled images.

## How to use

Place your images in the input directory. The images in this directory may or may not get edited. If you need to keep the original pictures then please back it up in another directory. Run the script if you are ready. The processed images will be in the output folder.

## Dependencies

- `bash`
- `imagemagick`
- `waifu2x-ncnn-vulkan`
- `oxipng`

## To do

- [ ] Fix terminal output of line 18 and 43
- [ ] Option to disable upscaling with waifu2x
- [ ] Option to choose cpu or gpu with upscaling 
- [ ] Option to choose resolution

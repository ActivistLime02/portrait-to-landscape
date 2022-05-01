#!/bin/bash

echo "The script has started"
cd input
echo "Upscaling with waifu2x"

# Resize pictures with AI
list=$(ls *)
for img in $list
do
    height=$(convert -ping $img -format "%h" info:)
    if [ "$height" -lt "2160" ]
    then
        mv $img ../1
    fi

    width=$(convert -ping $img -format "%w" info: 2>/dev/null)
    if [ "$width" -lt "3840" ]
    then
        mv $img ../1 2>/dev/null
    fi
done
echo "Preperations are ready for waifu2x"

cd ..
until [ -z "$(ls -A 1)" ]
do
    waifu2x-ncnn-vulkan -i 1 -o 2
    rm 1/*
    cd 2

    list=$(ls *)
    for img in $list
    do
        height=$(convert -ping $img -format "%h" info:)
        if [ "$height" -lt "2160" ]
        then
            mv $img ../1
        fi

        width=$(convert -ping $img -format "%w" info: 2>/dev/null)
        if [ "$width" -lt "3840" ]
        then
            mv $img ../1
        fi
    done
    cd ..
done
echo "Waifu2x is done"
mv 2/* input/

cd input
list=$(ls *) # List all the pictures in the folder
for img in $list
do
    inname=$(convert -ping $img -format "%f" info:) # This will make sure the names in the output folder is the same
    convert -size 3840x2160 xc:black $img -resize 3840x2160^ -blur 0x25 -gravity center -composite $img -geometry 3840x2160 -gravity center -composite ../output/${inname} # Magick, pun intended
done

# Change everything to png
echo "Changing everything to png"
cd ../output
list=$(ls -A | grep -v ".png")
for img in $list
do
    inname=$(convert -ping $img -format "%t" info:)
    convert $img ${inname}.png
    rm $img
done

# Optimize png files
oxipng -o max -s safe *.png


echo "Check the output folder for the results"

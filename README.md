# ImageResize

This program is intended to crop images captured, for example in a `4:3` aspect ratio,
to another aspect ratio such as `16:9`. At the same time, the imagequality can be
reduced on a percentual setting. Input and Output images are of type `.jpg`. Make
sure you select a different Output folder when prompted, to not overwrite your
existing images. If you select the same folder, images will be overwritten.

## Installation

Install the dependencies using `pip install -r requirements.txt`. Then you can run
the `main.py` python script. (tested only on windows, but should work on linux too)

## Usage

- Press `open directory` to select an input and output directory
  - files present in the output directory may be overwritten!
- Use the `skip` and `last image` buttons to navigate through the image folder
  - alternatively you can use the `space` and `backspace` keys respectively
- Use `save and skip` or `right_shift` to convert and save the image, without cropping
- Use `crop and save` or `enter` to crop, convert and save the image
- Click `convert until res change` to convert all images until the resolution
differs from the resolution of the current image. Images will not be cropped
- Click `convert except 16/9` to convert all images that do not have a `16:9`
aspect ratio. Images will not be cropped. The program will end when it reaches
the `0th` image.
- Type in the percentage of the imagequality into the `Image Quality:` field, that
you want your output images to have. The quality corresponds to the `jpg` compression
quality.

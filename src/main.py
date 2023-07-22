# import custom classes
from TkWindow import *

# global variables
image_directory_path = None
image_paths = None
image_index = None
panel = None
window = None
img = None

# show the TkInter GUI
if __name__ == '__main__':

    # setting variables
    aspect_ratios = { 'original': 4.0/3.0, '16:9': 16.0/9.0, '21:9': 21.0/9.0 }

    window_dimensions = (1100, 900)
    image_preview_height = 700
    image_preview_dimensions = (int(image_preview_height*aspect_ratios['original']), image_preview_height)

    window = TKWindow(window_dimensions, image_preview_dimensions, aspect_ratios, first_image_index=0)




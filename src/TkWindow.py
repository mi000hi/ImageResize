from PIL import Image,  ImageOps

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from PIL import ImageTk, Image

import glob
import os

Image.MAX_IMAGE_PIXELS = 933120000

class TKWindow():

    root = None
    button_open = None
    button_save = None
    button_skip = None
    image_directory_path = None
    image_paths = None
    image_index = None
    panel_image = None
    current_image_path = None
    current_tk_image_raw = None
    current_tk_image_drawn = None
    image_resized = None
    canvas = None
    canvas_rectangle = None
    rectangle = None
    input_quality_entry = None

    image_output_quality = 85

    def save_image(self, image):
        quality = int(self.input_quality_entry.get())
        exif = self.img_raw.info['exif']

        img_filename = os.path.basename(self.current_image_path)
        image.save(f"{self.image_directory_path_output}/{img_filename}", quality=quality, optimize=True, exif=exif)

    def update_tk_image(self, tk_image):
        self.canvas_image = self.canvas.create_image(0,0, anchor=tk.NW, image=tk_image)

    def load_new_image(self):
        self.image_index = self.image_index%len(self.image_paths)
        self.progress['value'] = int(self.image_index/len(self.image_paths)*100)
        self.progress.update_idletasks()

        self.current_image_path = self.image_paths[self.image_index]
        print(f"new image: {self.current_image_path}")
        self.img_raw = Image.open(self.current_image_path)
        self.img_raw = ImageOps.exif_transpose(self.img_raw)

        ratio = self.img_raw.width/self.img_raw.height

        width = int(self.image_preview_dimensions[1]*ratio)
        height = self.image_preview_dimensions[1]

        if width > self.window_dimensions[0]-100:
            width = self.window_dimensions[0]-100
            height = int(width/ratio)
        self.img_resized = self.img_raw.resize((width, height))

        self.current_tk_image_raw = ImageTk.PhotoImage(self.img_resized)

    def button_skip_function(self):
        print("skipping image")

        self.image_index += 1
        self.load_new_image()
        self.update_tk_image(self.current_tk_image_raw)

    def button_save_and_skip_function(self):
        print("saving and skipping image")
        self.save_image(self.img_raw)

        self.image_index += 1
        self.load_new_image()
        self.update_tk_image(self.current_tk_image_raw)

    def button_crop_and_save_function(self):
        img = self.img_raw.copy()
        ratio = img.width/self.image_preview_dimensions[0]

        y1 = int(self.rectangle[0][1]*ratio)
        y2 = int(y1+img.width/self.aspect_ratios[self.aspect_ratio_new_string])
        if y2 > img.height:
            y2 = int(self.image_preview_dimensions[1]*ratio)
            y1 = int(y2-img.width/self.aspect_ratios[self.aspect_ratio_new_string])
        crop_points = (0, y1, img.width, y2)
        img = img.crop(crop_points)

        self.save_image(img)
        self.button_skip_function()
        

    def button_open_function(self):
        self.image_directory_path = fd.askdirectory()
        print(f"selected directory: {self.image_directory_path}")

        # get image path list
        self.image_paths = glob.glob(f"{self.image_directory_path}/*.jpg")
        self.image_index = self.image_index_first

        self.load_new_image()
        self.update_tk_image(self.current_tk_image_raw)

        self.image_directory_path_output = fd.askdirectory()
        print(f"selected output directory: {self.image_directory_path_output}")

    def button_convert_all_except_16_9_function(self):
        while self.image_index > 0:
            if self.img_raw.width/self.img_raw.height != 16.0/9.0:
                self.button_save_and_skip_function()
            else:
                self.button_skip_function()

    def button_last_function(self):
        self.image_index -= 1
        self.load_new_image()
        self.update_tk_image(self.current_tk_image_raw)

    def button_convert_all_until_change_function(self):
        current_width = self.img_raw.width
        current_height = self.img_raw.height

        while self.img_raw.width == current_width and self.img_raw.height == current_height:
            self.button_save_and_skip_function()

    def key_handler(self, event):
        print(event.char, event.keysym, event.keycode)

        if event.keysym == 'Return':
            self.button_crop_and_save_function()
        elif event.keysym == 'Shift_R':
            self.button_save_and_skip_function()
        elif event.keysym == 'space':
            self.button_skip_function()
        elif event.keysym == 'BackSpace':
            self.button_last_function()

    def click_handler(self, event):
        mouse_y = event.y
        self.rectangle = ((0+2,mouse_y), (self.image_preview_dimensions[0]-1,mouse_y+int(self.image_preview_dimensions[0]/self.aspect_ratios[self.aspect_ratio_new_string])))

        # draw rect on image
        self.canvas.delete(self.canvas_rectangle)
        self.canvas_rectangle = self.canvas.create_rectangle(self.rectangle, outline="red")

    def __init__(self, window_dimensions, image_preview_dimensions, aspect_ratios, first_image_index):
        self.window_dimensions        = window_dimensions
        self.image_preview_dimensions = image_preview_dimensions
        self.aspect_ratios            = aspect_ratios
        self.aspect_ratio_new_string  = '16:9'
        self.image_index_first        = first_image_index

        #This creates the main window of an application
        self.root = tk.Tk()
        self.root.title("Image resizer")
        self.root.geometry(f"{window_dimensions[0]}x{window_dimensions[1]}")

        # key handler
        self.root.bind("<Key>", self.key_handler)

        # top frames
        self.top_frame = tk.Frame(self.root, width=self.window_dimensions[0]-20, height=100)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10)

        self.top_frame_buttons = tk.Frame(self.top_frame, width=self.window_dimensions[0]-20-20, height=100-20)
        self.top_frame_buttons.grid(row=0, column=0, padx=10, pady=10)

        # add buttons
        self.button_open = tk.Button(self.top_frame_buttons, width=20, height=1, text="open directory", command=self.button_open_function)
        self.button_open.grid(row=0, column=0, padx=5, pady=5)
        self.button_skip = tk.Button(self.top_frame_buttons, width=20, height=1, text="skip", command=self.button_skip_function)
        self.button_skip.grid(row=0, column=1, padx=5, pady=5)
        self.button_last = tk.Button(self.top_frame_buttons, width=20, height=1, text="last image", command=self.button_last_function)
        self.button_last.grid(row=1, column=1, padx=5, pady=5)
        self.button_save_and_skip = tk.Button(self.top_frame_buttons, width=20, height=1, text="save and skip", command=self.button_save_and_skip_function)
        self.button_save_and_skip.grid(row=0, column=2, padx=5, pady=5)
        self.button_save = tk.Button(self.top_frame_buttons, width=20, height=1, text="crop and save", command=self.button_crop_and_save_function)
        self.button_save.grid(row=1, column=2, padx=5, pady=5)
        self.button_convert_all_until_change = tk.Button(self.top_frame_buttons, width=20, height=1, text="convert until res change", command=self.button_convert_all_until_change_function)
        self.button_convert_all_until_change.grid(row=0, column=3, padx=5, pady=5)
        self.button_convert_all_except_16_9 = tk.Button(self.top_frame_buttons, width=20, height=1, text='convert except 16/9', command=self.button_convert_all_except_16_9_function)
        self.button_convert_all_except_16_9.grid(row=1, column=3, padx=5, pady=5)

        # image quality input field
        self.image_quality_label = tk.Label(self.top_frame_buttons, text="Image Quality: ", width=20, height=1)
        self.image_quality_label.grid(row=0, column=4, padx=5, pady=5)
        self.input_quality_entry = tk.Entry(self.top_frame_buttons, width=20)
        self.input_quality_entry.insert(0, str(self.image_output_quality))
        self.input_quality_entry.grid(row=0, column=5, padx=5, pady=5)

        # # add progress bar
        self.progress = ttk.Progressbar(self.top_frame, orient='horizontal', mode='determinate', length=window_dimensions[0]-20-20)
        self.progress.grid(row=1, column=0, padx=5, pady=5)

        # image preview canvas
        self.canvas = tk.Canvas(self.root, width=self.window_dimensions[0]-20-20, height=self.window_dimensions[1]-100-20-20-20)
        self.canvas.bind("<B1-Motion>", self.click_handler)
        self.canvas.grid(row=1, column=0, padx=5, pady=5)

        #Start the GUI
        self.root.mainloop()
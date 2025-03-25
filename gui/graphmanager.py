import tkinter as tk
from tkinter import Label, ttk
from PIL import ImageTk, Image
import os

class GraphManager:
    def __init__(self, parent, bd=1):
        self.parent = parent 
        # Create a fixed-size frame.
        self.frame = tk.Frame(parent, width=800, height=1000, padx=10)
        self.frame.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')
        # Prevent the frame from auto-resizing to its content.
        self.frame.grid_propagate(False)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Configure the grid of self.frame:
        # Row 0 will be a spacer (takes up extra vertical space)
        self.frame.grid_rowconfigure(0, weight=1)
        # Rows 1 and 2 will hold the image and button container respectively.
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=0)
        # Configure columns to center content.
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Load the default image.
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = os.path.join(self.current_dir, "graphs")
        image_path = os.path.join(self.folder_path, "no_image.png")
        self.my_photo = ImageTk.PhotoImage(Image.open(image_path), master=self.frame)

        self.label = Label(self.frame, image=self.my_photo)
        # sticky 's' ensures it aligns to the bottom of its grid cell.
        self.label.grid(row=1, column=0, columnspan=2, sticky='s', pady=(0,10))
        
        button_frame = tk.Frame(self.frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='s')
        # Center the buttons horizontally.
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        self.button_bar = ttk.Button(button_frame, text="Bar Graph", command=self.bar)
        self.button_pie = ttk.Button(button_frame, text="Pie Chart", command=self.pie)
        # The buttons are arranged side-by-side.
        self.button_bar.grid(row=0, column=0, padx=10, sticky='e')
        self.button_pie.grid(row=0, column=1, padx=10, sticky='w')
        
    def bar(self):
        image_path = os.path.join(self.folder_path, "bargraph.png")
        if not os.path.exists(image_path):
            image_path = os.path.join(self.folder_path, "no_image.png")
        new_image = ImageTk.PhotoImage(Image.open(image_path), master=self.frame)
        self.label.config(image=new_image)
        self.my_photo = new_image

    def pie(self):
        image_path = os.path.join(self.folder_path, "piechart.png")
        if not os.path.exists(image_path):
            image_path = os.path.join(self.folder_path, "no_image.png")
        new_image = ImageTk.PhotoImage(Image.open(image_path), master=self.frame)
        self.label.config(image=new_image)
        self.my_photo = new_image

import tkinter as tk
from tkinter import Label, Button
from PIL import ImageTk, Image
import os

class GraphManager:
    def __init__(self, parent):
        self.parent = parent
        # Place frame in row=0, column=0 of the right_frame
        self.frame = tk.Frame(parent)
        self.frame.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = os.path.join(self.current_dir, "graphs")
        image_path = os.path.join(self.folder_path, "no_image.png")
        # Store the image in a dedicated instance variable
        self.my_photo = ImageTk.PhotoImage(Image.open(image_path), master=self.frame)
        # Attach the image to a label and grid it within the frame
        self.label = Label(self.frame, image=self.my_photo)
        self.label.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        self.button_bar = Button(self.frame, text="Bar Graph", command=self.bar)
        self.button_pie = Button(self.frame, text="Pie Chart", command=self.pie)
        
        self.button_bar.grid(row=5, column=0, padx=10, pady=10)
        self.button_pie.grid(row=5, column=1, padx=10, pady=10)
        
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


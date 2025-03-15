import tkinter as tk

class ButtonManager:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=2, padx=20, pady=20, sticky='wn')
        self.button = tk.Button(self.frame, text="Export As PDF")
        self.button.grid(row=0, column=1, padx=10, sticky='wn')
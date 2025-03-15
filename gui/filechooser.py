import tkinter as tk
from tkinter import filedialog as fd
import os

class FileChooser:
    def __init__(self, parent, callback):
        """
        parent: the parent widget
        callback: function called after file selection
        """
        self.parent = parent
        self.callback = callback
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky='w')
        self.label = tk.Label(self.frame, text="Select SBOM .json file")
        self.label.grid(row=0, column=0, padx=10, sticky='w')
        self.button = tk.Button(self.frame, text="Open a File", command=self.select_file)
        self.button.grid(row=0, column=1, padx=10, sticky='w')

    def select_file(self):
        filetypes = (('JSON files', '*.json'),)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "lastFolder.txt")
        folder = open(file_path, 'r').read()
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir= folder if folder != "" else '/',
            filetypes=filetypes
        )
        newFolder = os.path.dirname(filename)
        if newFolder != folder:
            f = open(file_path, 'w')
            f.write(newFolder)
            f.close()

        # Show rest of UI
        if self.callback:
            self.callback(filename)
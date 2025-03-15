import tkinter as tk
from tkinter import ttk
from .checkboxpanel import CheckboxPanel
from .tablemanager import TableManager
from .filechooser import FileChooser
from .graphmanager import GraphManager
from .scrollableframe import ScrollableFrame
from .buttonmanager import ButtonManager


class App(tk.Tk):
    json_file = ""
    def __init__(self):
        super().__init__()
        self.title("SBOM Visualizer")
        self.state('zoomed')  # Maximizes the window
        
        # Create a scrollable container that holds all widgets.
        scrollable = ScrollableFrame(self)
        scrollable.pack(fill="both", expand=True)
        
        # Create two container frames – left and right – inside the scrollable inner frame.
        self.left_frame = tk.Frame(scrollable.inner_frame, borderwidth=2, relief="groove", border=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.right_frame = tk.Frame(scrollable.inner_frame, borderwidth=2, relief="groove", border=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Configure grid in the inner frame for equal distribution.
        scrollable.inner_frame.grid_columnconfigure(0, weight=1)
        scrollable.inner_frame.grid_columnconfigure(1, weight=1)
        scrollable.inner_frame.grid_rowconfigure(0, weight=1)
        
        # Instantiate your custom widget classes in the left and right frames.
        self.file_chooser = FileChooser(self.left_frame, self.file_selected)
        self.table_manager = TableManager(self.left_frame)
        self.checkbox_panel = CheckboxPanel(self.left_frame, self.table_manager)
        self.graph_viewer = GraphManager(self.right_frame)
        self.button_manager = ButtonManager(self.right_frame)
    
    def file_selected(self, filename):
        self.checkbox_panel.show()
        self.table_manager.create_table(filename)

if __name__ == "__main__":
    app = App()
    app.mainloop()
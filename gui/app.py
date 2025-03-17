import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .checkboxpanel import CheckboxPanel
from .tablemanager import TableManager
from .filechooser import FileChooser
from .graphmanager import GraphManager
from .scrollableframe import ScrollableFrame
import sbom.sbom_json_to_table
from tkinter import filedialog as fd
import os

 
class App(tk.Tk):
    json_file = ""

    def __init__(self):
        super().__init__()
        self.title("SBOM Visualizer")
        self.state('zoomed')  # Start maximized

        # Use grid to manage full-screen layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a scrollable container that expands
        scrollable = ScrollableFrame(self)
        scrollable.grid(row=0, column=0, sticky="nsew")

        # Create two container frames – left and right
        self.left_frame = tk.Frame(scrollable.inner_frame, borderwidth=2, relief="groove", border=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_frame = tk.Frame(scrollable.inner_frame, borderwidth=2, relief="groove", border=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Configure layout to expand dynamically
        scrollable.inner_frame.grid_columnconfigure(0, weight=1)
        scrollable.inner_frame.grid_columnconfigure(1, weight=1)
        scrollable.inner_frame.grid_rowconfigure(0, weight=1)

        # Add components
        self.file_chooser = FileChooser(self.left_frame, self.file_selected)
        self.table_manager = TableManager(self.left_frame)
        self.checkbox_panel = CheckboxPanel(self.left_frame, self.table_manager)
        self.graph_viewer = GraphManager(self.right_frame)

        # Generate PDF Button
        self.button = tk.Button(self.right_frame, text="Export As PDF", command=self.generate_pdf)
        self.button.grid(row=0, column=1, padx=10, sticky='wn')

        # Ensure the window updates before adjusting scroll
        self.update_idletasks()
        scrollable.canvas.configure(scrollregion=scrollable.canvas.bbox("all"))

    def file_selected(self, filename):
        self.json_file = filename
        self.checkbox_panel.show()
        self.table_manager.create_table(filename)

    def generate_pdf(self):
        folder = fd.askdirectory(
            title='Select folder to save PDF',
            initialdir='/',
        )
        filename = os.path.splitext(os.path.basename(self.json_file))[0]
        output_file = os.path.join(folder, filename)
        if folder and folder != "":
            try:
                sbom.sbom_json_to_table.generate_pdf_from_sbom(self.json_file, output_file)
                messagebox.showinfo("Success", f"PDF Generated: {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate PDF: {e}")
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
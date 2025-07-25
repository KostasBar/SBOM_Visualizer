import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from .checkboxpanel import CheckboxPanel
from .tablemanager import TableManager
from .filechooser import FileChooser
from .graphmanager import GraphManager
import sbom.sbom_json_to_table
import sbom.sbom_parser
from tkinter import filedialog as fd
import os

class App(tk.Tk):
    json_file = ""

    def __init__(self):
        super().__init__()
        self.title("SBOM Visualizer")
        # Set the theme immediately so all widgets use "clam"
        style = ttk.Style(self)
        style.theme_use("clam")

        # Configure the main grid so the content_frame fills the window.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        content_frame = tk.Frame(self)
        content_frame.grid(row=0, column=0, sticky="nsew")
        # Configure grid weights for left/right split (60/40 split)
        content_frame.grid_columnconfigure(0, weight=3)  # left_frame
        content_frame.grid_columnconfigure(1, weight=2)  # right_frame
        content_frame.grid_rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(content_frame, borderwidth=4, relief="groove")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Add components in the left frame.
        self.file_chooser = FileChooser(self.left_frame, self.file_selected)
        # self.table_manager = TableManager(self.left_frame)
        # self.checkbox_panel = CheckboxPanel(self.left_frame, self.table_manager)

        # Generate PDF Button in right_frame (aligned to left).
        self.button = ttk.Button(self.left_frame, text="Export As PDF", command=self.generate_pdf)
        self.button.grid(row=1, column=0, padx=15, pady=10, sticky='w')

        self.button.grid(row=1, column=0, padx=(30, 5), pady=10, sticky='w')

        ttk.Label(self.left_frame, text="Export as Chart:").grid(row=1, column=1, padx=(0, 0), pady=10, sticky='e')

        self.chart_var = tk.StringVar()
        self.chart_combobox = ttk.Combobox(self.left_frame, width=10, textvariable=self.chart_var, state="readonly")
        self.chart_combobox['values'] = ('Bar', 'Pie')
        self.chart_combobox.grid(row=1, column=2, padx=(0, 15), pady=10, sticky='w')
        self.chart_combobox.current(1)
        self.chart_combobox.bind("<<ComboboxSelected>>", self.chart_selected)   

        # # Disable window resizing.
        self.resizable(False, False)

        # Set the window icon.
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = os.path.join(self.current_dir, "img")
        image_path = os.path.join(self.folder_path, "app-icon.png")
        img = ImageTk.PhotoImage(Image.open(image_path), master=self)
        self.iconphoto(False, img)

    def file_selected(self, filename):
        self.json_file = filename
        sbom.sbom_parser.get_table_rows(filename)

    def generate_pdf(self):
        if self.json_file and self.json_file != '':
            folder = fd.askdirectory(title='Select folder to save PDF', initialdir='/')
            filename = os.path.splitext(os.path.basename(self.json_file))[0]
            output_file = os.path.join(folder, filename)
            if folder and folder != "":
                try:
                    sbom.sbom_json_to_table.generate_pdf_from_sbom(self.json_file, output_file)
                    messagebox.showinfo("Success", f"PDF Generated: {output_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate PDF: {e}")
        else:
            messagebox.showwarning("Warning!", "Please select a valid SBOM json file first!")

    def chart_selected(self, event):
        if self.json_file and self.json_file != '':

            selected = self.chart_combobox.get()
            if selected == "Pie":
                sbom.graphGenerator.generate_graphs(2)
            elif selected == "Bar":
                sbom.graphGenerator.generate_graphs(1)

if __name__ == "__main__":
    app = App()
    app.mainloop()

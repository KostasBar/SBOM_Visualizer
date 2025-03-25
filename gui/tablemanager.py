import tkinter as tk
from tkinter import ttk
import sbom
import sbom.sbom_parser
import tkinter.font as tkFont
import sbom.graphGenerator

class TableManager:
    def __init__(self, parent):
        self.parent = parent
        
        self.frame = tk.Frame(parent, bd=1, width=1000, height=1000, relief="solid", border=0)
        self.frame.grid(row=2, column=0, padx=20, pady=10, sticky='nsew')
        self.frame.grid_propagate(False)  # Keep size
        
        # Attach Grid To Parent
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        self.table = None
        self.columns = ["Name", "Type", "Version", "License", "Latest Version", "HasBeta"]
        self.default_widths = {
            "Name": 150,
            "Type": 100,
            "Version": 100,
            "License": 100,
            "Latest Version": 120,
            "HasBeta": 80,
        }
        
        # Row Styling
        style = ttk.Style()
        style.configure("Custom.Treeview",
                rowheight=30,
                font=("Segoe UI", 10),
                background="#ffffff",
                fieldbackground="#f9f9f9",
                bordercolor="#dcdcdc",)
        style.map("Custom.Treeview", background=[('selected', '#90D5FF')],)
        style = ttk.Style()
        style.theme_use("clam")

        self.normal_font = tkFont.Font(family="TkDefaultFont", size=10)
        self.bold_font = tkFont.Font(family="TkDefaultFont", size=10, weight="bold")

    def create_table(self, filename):
        # Clear previous widgets
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.table = ttk.Treeview(self.frame, columns=self.columns, show="headings", style="Custom.Treeview")
        
        # Set up columns & headers
        for col in self.columns:
            self.table.heading(col, text=col)
            width = self.default_widths.get(col, 100)
            self.table.column(col, width=width, minwidth=width, stretch=True)
        
        loading_label = tk.Label(self.frame, text="Loading data...", font=("Arial", 16))
        loading_label.grid(row=2, column=0, columnspan=2, pady=10)
        self.frame.update()  # Force update so the label appears

        # Insert Data
        table_rows = sbom.sbom_parser.get_table_rows(filename)
        cnt = 0
        for row in table_rows[1:]:
            apply_red = False
            values = []
            for cell in row:
                # if datum is type Paragraph, get its plain text
                if hasattr(cell, "getPlainText"):
                    values.append(cell.getPlainText())
                else:
                    values.append(str(cell))
            
            # Check condition for red text
            if values[2].strip() != values[4].strip() and values[0].lower() != 'nutrinet':
                apply_red = True
            
            cnt += 1
            base_tag = 'even' if cnt % 2 == 0 else 'odd'
            # Combine base tag with red if condition met
            final_tags = ('red', base_tag) if apply_red else (base_tag,)
            
            self.table.insert("", tk.END, values=values, tags=final_tags)

        # Configure row colors
        self.table.tag_configure('even', background='#f0f0f0', foreground='black')
        self.table.tag_configure('odd', background='white', foreground='black')
        self.table.tag_configure('red', foreground='red')
        self.table.tag_configure('selected', background='#90D5FF')
        
        # Scrollbars
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.table.yview)
        hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid()
        loading_label.destroy()
        
        sbom.graphGenerator.generate_graphs()
        
        self.table.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def on_parent_resize(self, event):
        new_width = min(event.width - 40, 1200) 
        new_height = min(event.height - 40, 1100)
        self.frame.config(width=new_width, height=new_height)


    def on_treeview_select(self, event):

        for item in self.table.get_children():

            tags = [t for t in self.table.item(item, "tags") if t not in ("selected",)]
            self.table.item(item, tags=tuple(tags))

        for item in self.table.selection():
            current_tags = list(self.table.item(item, "tags"))
            if "selected" not in current_tags:
                current_tags.append("selected")
                self.table.item(item, tags=tuple(current_tags))

    def toggle_column(self, col, visible):
        if self.table:
            if visible:
                width = self.default_widths.get(col, 100)
                self.table.column(col, width=width, minwidth=width, stretch=True)
            else:
                self.table.column(col, width=0, minwidth=0, stretch=False)


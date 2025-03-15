import tkinter as tk

class CheckboxPanel:
    def __init__(self, parent, table_manager):
        self.parent = parent
        self.table_manager = table_manager
        self.frame = tk.Frame(parent)
        self.frame.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.frame.grid_remove() # Hide the frame

        self.vars = {}
        self.checkboxes = {}
        for col in ["Name", "Type", "Version", "License", "Latest Version"]:
            var = tk.IntVar(value=1)
            self.vars[col] = var
            cb = tk.Checkbutton(self.frame, text=col, variable=var,
                                command=lambda c=col: self.toggle(c))
            self.checkboxes[col] = cb
            cb.pack(side=tk.LEFT, padx=5)

    def toggle(self, col):
        visible = self.vars[col].get() == 1
        self.table_manager.toggle_column(col, visible)

    def show(self):
        self.frame.grid() 
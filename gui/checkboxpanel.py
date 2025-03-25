import tkinter as tk
from tkinter import ttk

class CheckboxPanel:
    def __init__(self, parent, table_manager):
        self.parent = parent
        self.table_manager = table_manager
        self.frame = tk.Frame(parent)
        self.frame.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.frame.grid_remove()  # Hide the frame initially

        style = ttk.Style()
        # Use a theme that allows customization
        style.theme_use("clam")

        # Base style for checkbuttons: a neutral background with flat edges.
        style.configure("Custom.TCheckbutton",
                        font=("Segoe UI", 10),
                        background="#ececec",  # Neutral light gray background
                        foreground="#333333",
                        padding=5,
                        relief="flat",
                        borderwidth=0)
        # Hover style: add a raised relief and a small border to simulate a shadow effect.
        style.configure("Custom.Hover.TCheckbutton",
                        font=("Segoe UI", 10),
                        background="#ececec",
                        foreground="#333333",
                        padding=5,
                        relief="raised",
                        borderwidth=1)

        self.vars = {}
        self.checkboxes = {}
        for col in ["Name", "Type", "Version", "License", "Latest Version"]:
            var = tk.IntVar(value=1)
            self.vars[col] = var
            cb = ttk.Checkbutton(self.frame, text=col, variable=var,
                                 command=lambda c=col: self.toggle(c),
                                 style="Custom.TCheckbutton")
            self.checkboxes[col] = cb
            cb.pack(side=tk.LEFT, padx=5)

            # Bind hover events to swap styles.
            cb.bind("<Enter>", lambda e, widget=cb: widget.configure(style="Custom.Hover.TCheckbutton"))
            cb.bind("<Leave>", lambda e, widget=cb: widget.configure(style="Custom.TCheckbutton"))

    def toggle(self, col):
        visible = self.vars[col].get() == 1
        self.table_manager.toggle_column(col, visible)

    def show(self):
        self.frame.grid()

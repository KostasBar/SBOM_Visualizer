import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create a canvas to hold the scrollable content.
        self.canvas = tk.Canvas(self)
        # Vertical scrollbar (standard style).
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        # Create a custom style for the horizontal scrollbar to remove borders.
        style = ttk.Style()
        style.configure("Custom.Horizontal.TScrollbar", borderwidth=0, bordercolor='transparent', relief="flat")
        # Horizontal scrollbar with custom style.
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview,
                                  style="Custom.Horizontal.TScrollbar")
        self.canvas.configure(xscrollcommand=self.hsb.set)
        
        # Layout scrollbars and canvas.
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create an inner frame to hold all content.
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        # Update the scrollable region when the inner frame changes.
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Optionally, bind mousewheel scrolling.
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        # For Windows, delta is in event.delta; adjust as needed for other OS.
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
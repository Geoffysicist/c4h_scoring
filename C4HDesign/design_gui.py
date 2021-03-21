import tkinter as tk
from tkinter import ttk
from .design import C4HArena

root = tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sketch = C4HArena(root)
sketch.grid(column=0, row=0, sticky=(N, W, E, S))

root.mainloop()

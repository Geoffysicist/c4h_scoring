"""
Setup for Ghostscript:
Download it from http://www.ghostscript.com/ and
add `/path/to/gs9.07/bin/` and `/path/to/gs9.07/lib/` to your path.
"""

import os
import subprocess
import tkinter as tk

class App(object):
    def __init__(self, root):
        self.line_start = None
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.bind("<Button-1>", lambda e: self.draw(e.x, e.y))
        self.button = tk.Button(root, text="Generate PDF", command=self.generate_pdf)
        self.canvas.pack()
        self.button.pack(pady=10)

    def draw(self, x, y):
        if self.line_start:
            x_origin, y_origin = self.line_start
            self.canvas.create_line(x_origin, y_origin, x, y)
            self.line_start = None
        else:
            self.line_start = (x, y)

    def generate_pdf(self):
        self.canvas.postscript(file="tmp.ps", colormode="color")
        process = subprocess.Popen(["ps2pdf", "tmp.ps", "result.pdf"], shell=True)
        process.wait()
        os.remove("tmp.ps")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Canvas2PDF")
    app = App(root)
    root.mainloop()
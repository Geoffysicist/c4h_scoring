# from ttkthemes import ThemedTk
import tkinter as tk
from C4HDesign import design_gui as c4h

if __name__ == "__main__":

    # root = ThemedTk(theme="arc")
    root = tk.Tk()
    c4h.C4HDesignGUI(root)
    root.mainloop()
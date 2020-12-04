# set up the gui
# from tkinter import PhotoImage, Menu
from ttkthemes import ThemedTk
import c4h_scoreboard as c4h
# import ctypes

# # makes dpi aware so tkinter text isnt blurry
# ctypes.windll.shcore.SetProcessDpiAwareness(1)

def donothing():
    pass


if __name__ == "__main__":

    root = ThemedTk(theme="arc")
    c4h.C4HScoreGUI(root)
    root.mainloop()

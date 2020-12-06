# set up the gui
# from tkinter import PhotoImage, Menu
from ttkthemes import ThemedTk
import ch4_score_gui as gui
# import ctypes

# # makes dpi aware so tkinter text isnt blurry
# ctypes.windll.shcore.SetProcessDpiAwareness(1)

def donothing():
    pass


if __name__ == "__main__":

    root = ThemedTk(theme="arc")
    gui.C4HScoreGUI(root)
    root.mainloop()

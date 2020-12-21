from ttkthemes import ThemedTk
from C4HScore import score_gui as gui

if __name__ == "__main__":

    root = ThemedTk(theme="arc")
    gui.C4HScoreGUI(root)
    root.mainloop()
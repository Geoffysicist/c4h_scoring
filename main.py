from ttkthemes import ThemedTk
# import c4h_score as c4h
# from ch4_score_gui import C4HScoreGUI
from C4HScore import score_gui as gui

if __name__ == "__main__":

    root = ThemedTk(theme="arc")
    gui.C4HScoreGUI(root)
    root.mainloop()
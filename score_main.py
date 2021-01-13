from ttkthemes import ThemedTk
from C4HScore import score_gui as c4h
# import C4HScore as c4h

if __name__ == "__main__":

    root = ThemedTk(theme="arc")
    c4h.C4HScoreGUI(root)
    root.mainloop()
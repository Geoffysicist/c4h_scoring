from ttkthemes import ThemedTk
import ch4_score_gui as gui


def donothing():
    pass


if __name__ == "__main__":

    root = ThemedTk(theme="arc")
    gui.C4HScoreGUI(root)
    root.mainloop()

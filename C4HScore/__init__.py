from ttkthemes import ThemedTk
# import c4h_score as c4h
import ch4_score_gui as gui



if __name__ == "__main__":

    root = ThemedTk(theme="arc")
    gui.C4HScoreGUI(root)
    root.mainloop()
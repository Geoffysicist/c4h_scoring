from ttkthemes import ThemedTk
from C4HDesign import design_gui as c4h

if __name__ == "__main__":

    root = ThemedTk(theme="arc")
    c4h.C4HDesignGUI(root)
    root.mainloop()
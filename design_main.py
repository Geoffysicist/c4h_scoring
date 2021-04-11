# from ttkthemes import ThemedTk
import tkinter as tk
from C4HDesign import design_gui as c4h

DEBUG = True

if __name__ == "__main__":

    # root = ThemedTk(theme="arc")
    root = tk.Tk()
    gui = c4h.C4HDesignGUI(root)
    if DEBUG:
        import cmath as c
        plan = gui.plan_new()
        # plan.focus_set()
        plan.update()
        plan.event_generate("<Button-3>", x=500, y=500)
        plan.event_generate("<Button-3>", x=700, y=500)
        plan.set_focus(plan.sprites[-1])
        plan.rotate(3*c.pi/2)
        plan.translate(complex(0,-200))
        plan.clear_focus()

    root.mainloop()
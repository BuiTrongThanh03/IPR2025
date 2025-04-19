import tkinter as tk
from UI import CanvasEditorUI
from function import CanvasEditorLogic

if __name__ == "__main__":
    root = tk.Tk()
    logic = CanvasEditorLogic(None)  # Temporary None, set after UI creation
    ui = CanvasEditorUI(root, logic)
    logic.ui = ui  # Set UI reference in logic
    root.mainloop()
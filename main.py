import tkinter as tk
from function import CanvasEditorLogic
from text_UI import EditorApp

if __name__ == "__main__":
    root = tk.Tk()
    logic = CanvasEditorLogic(None)  # Temporary None, set after UI creation
    ui = EditorApp(root, logic)
    logic.ui = ui  # Set UI reference in logic
    root.mainloop()
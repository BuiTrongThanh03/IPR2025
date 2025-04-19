import tkinter as tk
from tkinter import ttk, font, filedialog

class CanvasEditorUI:
    def __init__(self, root, logic):
        self.root = root
        self.root.title("Image Canvas Editor")
        self.logic = logic  # Reference to CanvasEditorLogic

        # Canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # General Toolbar
        self.general_toolbar = tk.Frame(root)
        self.general_toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(self.general_toolbar, text="Upload Image", command=self.logic.upload_image).pack(side=tk.LEFT)

        self.text_input = tk.Entry(self.general_toolbar)
        self.text_input.pack(side=tk.LEFT)
        tk.Button(self.general_toolbar, text="Add Text", command=self.logic.add_text).pack(side=tk.LEFT)

        tk.Button(self.general_toolbar, text="Add Rectangle", command=self.logic.add_rectangle).pack(side=tk.LEFT)

        tk.Button(self.general_toolbar, text="Apply Changes", command=self.logic.apply_changes).pack(side=tk.LEFT)

        # Text Toolbar
        self.text_toolbar = tk.Frame(root)
        self.text_toolbar.pack(side=tk.TOP, fill=tk.X)

        self.font_var = tk.StringVar(value="Arial")
        self.font_size_var = tk.StringVar(value="12")
        self.text_color_var = tk.StringVar(value="black")
        self.bold_var = tk.BooleanVar()
        self.italic_var = tk.BooleanVar()
        self.underline_var = tk.BooleanVar()
        self.text_stroke_var = tk.BooleanVar()
        self.text_align_var = tk.StringVar(value="left")
        self.text_alpha_var = tk.DoubleVar(value=1.0)

        tk.Label(self.text_toolbar, text="Font:").pack(side=tk.LEFT)
        tk.OptionMenu(self.text_toolbar, self.font_var, *font.families()).pack(side=tk.LEFT)
        tk.Label(self.text_toolbar, text="Size:").pack(side=tk.LEFT)
        tk.Entry(self.text_toolbar, textvariable=self.font_size_var, width=5).pack(side=tk.LEFT)
        tk.Label(self.text_toolbar, text="Color:").pack(side=tk.LEFT)
        tk.Entry(self.text_toolbar, textvariable=self.text_color_var, width=10).pack(side=tk.LEFT)
        tk.Checkbutton(self.text_toolbar, text="Bold", variable=self.bold_var).pack(side=tk.LEFT)
        tk.Checkbutton(self.text_toolbar, text="Italic", variable=self.italic_var).pack(side=tk.LEFT)
        tk.Checkbutton(self.text_toolbar, text="Underline", variable=self.underline_var).pack(side=tk.LEFT)
        tk.Checkbutton(self.text_toolbar, text="Stroke", variable=self.text_stroke_var).pack(side=tk.LEFT)
        tk.Label(self.text_toolbar, text="Align:").pack(side=tk.LEFT)
        tk.OptionMenu(self.text_toolbar, self.text_align_var, "left", "center", "right").pack(side=tk.LEFT)
        tk.Label(self.text_toolbar, text="Alpha:").pack(side=tk.LEFT)
        tk.Scale(self.text_toolbar, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, variable=self.text_alpha_var).pack(side=tk.LEFT)

        # Image Toolbar
        self.image_toolbar = tk.Frame(root)
        self.image_toolbar.pack(side=tk.TOP, fill=tk.X)

        self.img_border_var = tk.BooleanVar()
        self.img_border_color_var = tk.StringVar(value="black")
        self.img_round_var = tk.BooleanVar()
        self.img_alpha_var = tk.DoubleVar(value=1.0)
        self.flip_h_var = tk.BooleanVar()
        self.flip_v_var = tk.BooleanVar()

        tk.Checkbutton(self.image_toolbar, text="Image Border", variable=self.img_border_var).pack(side=tk.LEFT)
        tk.Entry(self.image_toolbar, textvariable=self.img_border_color_var, width=10).pack(side=tk.LEFT)
        tk.Checkbutton(self.image_toolbar, text="Round Corners", variable=self.img_round_var).pack(side=tk.LEFT)
        tk.Label(self.image_toolbar, text="Image Alpha:").pack(side=tk.LEFT)
        tk.Scale(self.image_toolbar, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, variable=self.img_alpha_var).pack(side=tk.LEFT)
        tk.Checkbutton(self.image_toolbar, text="Flip Horizontal", variable=self.flip_h_var).pack(side=tk.LEFT)
        tk.Checkbutton(self.image_toolbar, text="Flip Vertical", variable=self.flip_v_var).pack(side=tk.LEFT)

        # Shape Toolbar
        self.shape_toolbar = tk.Frame(root)
        self.shape_toolbar.pack(side=tk.TOP, fill=tk.X)

        self.shape_border_color_var = tk.StringVar(value="black")
        self.shape_fill_color_var = tk.StringVar(value="blue")
        self.shape_border_size_var = tk.StringVar(value="2")
        self.shape_round_var = tk.BooleanVar()
        self.shape_alpha_var = tk.DoubleVar(value=1.0)

        tk.Label(self.shape_toolbar, text="Shape Border Color:").pack(side=tk.LEFT)
        tk.Entry(self.shape_toolbar, textvariable=self.shape_border_color_var, width=10).pack(side=tk.LEFT)
        tk.Label(self.shape_toolbar, text="Fill Color:").pack(side=tk.LEFT)
        tk.Entry(self.shape_toolbar, textvariable=self.shape_fill_color_var, width=10).pack(side=tk.LEFT)
        tk.Label(self.shape_toolbar, text="Border Size:").pack(side=tk.LEFT)
        tk.Entry(self.shape_toolbar, textvariable=self.shape_border_size_var, width=5).pack(side=tk.LEFT)
        tk.Checkbutton(self.shape_toolbar, text="Round Corners", variable=self.shape_round_var).pack(side=tk.LEFT)
        tk.Label(self.shape_toolbar, text="Shape Alpha:").pack(side=tk.LEFT)
        tk.Scale(self.shape_toolbar, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, variable=self.shape_alpha_var).pack(side=tk.LEFT)

        # Canvas Bindings
        self.canvas.bind("<Button-1>", self.logic.select_object)
        self.canvas.bind("<B1-Motion>", self.logic.drag_object)
        self.canvas.bind("<ButtonRelease-1>", self.logic.release_object)
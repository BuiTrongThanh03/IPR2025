import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, font
from PIL import Image, ImageTk
from function import CanvasEditorLogic
from text import TextEditor
from shape import ShapeEditor
from image import ImageEditor

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text, Image, and Shape Editor")
        self.text_editor = TextEditor()
        self.shape_editor = ShapeEditor()
        self.image_editor = ImageEditor()
        self.canvas_logic = CanvasEditorLogic(self)
        self.current_font_size = tk.DoubleVar(value=20)
        self.current_stroke_width = tk.DoubleVar(value=0)
        self.current_transparency = tk.DoubleVar(value=255)
        self.current_corner_radius = tk.DoubleVar(value=0)
        self.current_border_width = tk.DoubleVar(value=0)
        self.current_shape_width_cm = tk.StringVar(value="5.0")
        self.current_shape_height_cm = tk.StringVar(value="5.0")
        self.font_bold = tk.BooleanVar(value=False)
        self.font_italic = tk.BooleanVar(value=False)
        self.font_underline = tk.BooleanVar(value=False)
        self.text_color = "black"
        self.stroke_color = "black"
        self.border_color = "black"
        self.fill_color = "white"
        self.max_radius = 500
        self.DPI = 96  # 1 cm = 37.8 pixel tại 96 DPI
        self.CM_TO_PIXEL = self.DPI / 2.54  # 1 cm = 37.8 pixel

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas = tk.Canvas(self.main_frame, width=400, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3, pady=5)

        self.load_button = ttk.Button(self.main_frame, text="Load Image", command=self.canvas_logic.upload_image)
        self.load_button.grid(row=1, column=0, pady=5)
        self.add_text_button = ttk.Button(self.main_frame, text="Add Text", command=self.canvas_logic.add_text)
        self.add_text_button.grid(row=1, column=1, pady=5)
        self.add_shape_button = ttk.Button(self.main_frame, text="Add Shape", command=self.canvas_logic.add_shape)
        self.add_shape_button.grid(row=1, column=2, pady=5)

        self.edit_frame = ttk.LabelFrame(self.main_frame, text="Edit Properties", padding="5")
        self.edit_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))

        # Text controls
        self.text_label = ttk.Label(self.edit_frame, text="Text Content:")
        self.text_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.text_entry = ttk.Entry(self.edit_frame)
        self.text_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.text_entry.bind("<Return>", self.update_text_content)

        self.font_label = ttk.Label(self.edit_frame, text="Font:")
        self.font_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        available_fonts = ["Arial", "Times New Roman", "Courier New"]
        self.font_combo = ttk.Combobox(self.edit_frame, values=available_fonts, state="readonly")
        self.font_combo.set("Arial")
        self.font_combo.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.font_combo.bind("<<ComboboxSelected>>", self.update_font)

        self.font_size_label = ttk.Label(self.edit_frame, text="Font Size: 20")
        self.font_size_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        self.font_size_scale = ttk.Scale(self.edit_frame, from_=10, to=100, orient=tk.HORIZONTAL, variable=self.current_font_size, command=self.update_font_size)
        self.font_size_scale.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.bold_check = ttk.Checkbutton(self.edit_frame, text="Bold", variable=self.font_bold, command=self.update_font_style)
        self.bold_check.grid(row=3, column=0, pady=2)
        self.italic_check = ttk.Checkbutton(self.edit_frame, text="Italic", variable=self.font_italic, command=self.update_font_style)
        self.italic_check.grid(row=3, column=1, pady=2)
        self.underline_check = ttk.Checkbutton(self.edit_frame, text="Underline", variable=self.font_underline, command=self.update_font_style)
        self.underline_check.grid(row=3, column=2, pady=2)

        self.text_color_button = ttk.Button(self.edit_frame, text="Pick Text Color", command=self.pick_text_color)
        self.text_color_button.grid(row=4, column=0, columnspan=3, pady=2)

        self.stroke_width_label = ttk.Label(self.edit_frame, text="Stroke Width: 0")
        self.stroke_width_label.grid(row=5, column=0, sticky=tk.W, pady=2)
        self.stroke_width_scale = ttk.Scale(self.edit_frame, from_=0, to=5, orient=tk.HORIZONTAL, variable=self.current_stroke_width, command=self.update_stroke_width)
        self.stroke_width_scale.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.stroke_color_button = ttk.Button(self.edit_frame, text="Pick Stroke Color", command=self.pick_stroke_color)
        self.stroke_color_button.grid(row=6, column=0, columnspan=3, pady=2)

        self.align_label = ttk.Label(self.edit_frame, text="Alignment:")
        self.align_label.grid(row=7, column=0, sticky=tk.W, pady=2)
        self.align_combo = ttk.Combobox(self.edit_frame, values=["left", "center", "right"], state="readonly")
        self.align_combo.set("center")
        self.align_combo.grid(row=7, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.align_combo.bind("<<ComboboxSelected>>", self.update_alignment)

        self.transparency_label = ttk.Label(self.edit_frame, text="Transparency: 255")
        self.transparency_label.grid(row=8, column=0, sticky=tk.W, pady=2)
        self.transparency_scale = ttk.Scale(self.edit_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.current_transparency, command=self.update_transparency)
        self.transparency_scale.grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Shape controls
        self.shape_width_label = ttk.Label(self.edit_frame, text="Shape Width (cm):")
        self.shape_width_label.grid(row=9, column=0, sticky=tk.W, pady=2)
        self.shape_width_entry = ttk.Entry(self.edit_frame, textvariable=self.current_shape_width_cm)
        self.shape_width_entry.grid(row=9, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.shape_height_label = ttk.Label(self.edit_frame, text="Shape Height (cm):")
        self.shape_height_label.grid(row=10, column=0, sticky=tk.W, pady=2)
        self.shape_height_entry = ttk.Entry(self.edit_frame, textvariable=self.current_shape_height_cm)
        self.shape_height_entry.grid(row=10, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.apply_size_button = ttk.Button(self.edit_frame, text="Apply Size", command=self.update_shape_size)
        self.apply_size_button.grid(row=11, column=0, columnspan=3, pady=2)

        self.shape_border_color_button = ttk.Button(self.edit_frame, text="Pick Border Color", command=self.pick_shape_border_color)
        self.shape_border_color_button.grid(row=12, column=0, columnspan=3, pady=2)

        self.shape_fill_color_button = ttk.Button(self.edit_frame, text="Pick Fill Color", command=self.pick_shape_fill_color)
        self.shape_fill_color_button.grid(row=13, column=0, columnspan=3, pady=2)

        self.shape_border_width_label = ttk.Label(self.edit_frame, text="Border Width: 0")
        self.shape_border_width_label.grid(row=14, column=0, sticky=tk.W, pady=2)
        self.shape_border_width_scale = ttk.Scale(self.edit_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.current_border_width, command=self.update_shape_border_width)
        self.shape_border_width_scale.grid(row=14, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.shape_corner_label = ttk.Label(self.edit_frame, text="Corner Radius: 0")
        self.shape_corner_label.grid(row=15, column=0, sticky=tk.W, pady=2)
        self.shape_corner_scale = ttk.Scale(self.edit_frame, from_=0, to=self.max_radius, orient=tk.HORIZONTAL, variable=self.current_corner_radius, command=self.update_shape_corner)
        self.shape_corner_scale.grid(row=15, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Image controls
        self.image_corner_label = ttk.Label(self.edit_frame, text="Corner Radius: 0")
        self.image_corner_label.grid(row=16, column=0, sticky=tk.W, pady=2)
        self.image_corner_scale = ttk.Scale(self.edit_frame, from_=0, to=self.max_radius, orient=tk.HORIZONTAL, variable=self.current_corner_radius, command=self.update_image_corner)
        self.image_corner_scale.grid(row=16, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.image_border_width_label = ttk.Label(self.edit_frame, text="Border Width: 0")
        self.image_border_width_label.grid(row=17, column=0, sticky=tk.W, pady=2)
        self.image_border_width_scale = ttk.Scale(self.edit_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.current_border_width, command=self.update_image_border_width)
        self.image_border_width_scale.grid(row=17, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.image_border_color_button = ttk.Button(self.edit_frame, text="Pick Border Color", command=self.pick_image_border_color)
        self.image_border_color_button.grid(row=18, column=0, columnspan=3, pady=2)

        self.flip_h_button = ttk.Button(self.edit_frame, text="Flip Horizontal", command=self.flip_horizontal)
        self.flip_h_button.grid(row=19, column=0, pady=2)
        self.flip_v_button = ttk.Button(self.edit_frame, text="Flip Vertical", command=self.flip_vertical)
        self.flip_v_button.grid(row=19, column=1, pady=2)

        self.canvas.bind("<Button-1>", self.canvas_logic.select_object)
        self.canvas.bind("<B1-Motion>", self.canvas_logic.drag_object)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_logic.release_object)

        self.hide_all_controls()

    def hide_all_controls(self):
        """Ẩn tất cả các điều khiển chỉnh sửa"""
        for widget in self.edit_frame.winfo_children():
            widget.grid_remove()

    def update_controls(self):
        """Cập nhật giao diện điều khiển dựa trên đối tượng được chọn"""
        self.hide_all_controls()
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj:
            if selected_obj["type"] == "text":
                self.text_entry.delete(0, tk.END)
                self.text_entry.insert(0, selected_obj.get("text", ""))
                self.font_combo.set(selected_obj.get("font_name", "Arial"))
                self.current_font_size.set(selected_obj.get("font_size", 20))
                self.font_bold.set(selected_obj.get("font_bold", False))
                self.font_italic.set(selected_obj.get("font_italic", False))
                self.font_underline.set(selected_obj.get("font_underline", False))
                self.text_color = selected_obj.get("text_color", "black")
                self.current_stroke_width.set(selected_obj.get("stroke_width", 0))
                self.stroke_color = selected_obj.get("stroke_color", "black")
                self.align_combo.set(selected_obj.get("alignment", "center"))
                self.current_transparency.set(selected_obj.get("alpha", 1.0) * 255)
                self.font_size_label.config(text=f"Font Size: {int(self.current_font_size.get())}")
                self.stroke_width_label.config(text=f"Stroke Width: {int(self.current_stroke_width.get())}")
                self.transparency_label.config(text=f"Transparency: {int(self.current_transparency.get())}")
                self.text_label.grid()
                self.text_entry.grid()
                self.font_label.grid()
                self.font_combo.grid()
                self.font_size_label.grid()
                self.font_size_scale.grid()
                self.bold_check.grid()
                self.italic_check.grid()
                self.underline_check.grid()
                self.text_color_button.grid()
                self.stroke_width_label.grid()
                self.stroke_width_scale.grid()
                self.stroke_color_button.grid()
                self.align_label.grid()
                self.align_combo.grid()
                self.transparency_label.grid()
                self.transparency_scale.grid()
            elif selected_obj["type"] == "shape":
                self.current_shape_width_cm.set(str(selected_obj.get("width_cm", 5.0)))
                self.current_shape_height_cm.set(str(selected_obj.get("height_cm", 5.0)))
                self.border_color = selected_obj.get("border_color", "black")
                self.fill_color = selected_obj.get("fill_color", "white")
                self.current_border_width.set(selected_obj.get("border_width", 2))
                self.current_corner_radius.set(selected_obj.get("corner_radius", 0))
                self.current_transparency.set(selected_obj.get("alpha", 1.0) * 255)
                self.shape_border_width_label.config(text=f"Border Width: {int(self.current_border_width.get())}")
                self.shape_corner_label.config(text=f"Corner Radius: {int(self.current_corner_radius.get())}")
                self.transparency_label.config(text=f"Transparency: {int(self.current_transparency.get())}")
                self.max_radius = min(selected_obj["width"], selected_obj["height"]) // 2
                self.shape_corner_scale.configure(to=self.max_radius)
                self.shape_width_label.grid()
                self.shape_width_entry.grid()
                self.shape_height_label.grid()
                self.shape_height_entry.grid()
                self.apply_size_button.grid()
                self.shape_border_color_button.grid()
                self.shape_fill_color_button.grid()
                self.shape_border_width_label.grid()
                self.shape_border_width_scale.grid()
                # Chỉ hiển thị bo góc cho rectangle và square
                if selected_obj["shape_type"] in ["rectangle", "square"]:
                    self.shape_corner_label.grid()
                    self.shape_corner_scale.grid()
                self.transparency_label.grid()
                self.transparency_scale.grid()
            else:  # image
                self.current_transparency.set(selected_obj.get("alpha", 1.0) * 255)
                self.current_corner_radius.set(selected_obj.get("round_radius", 0))
                self.current_border_width.set(selected_obj.get("border_width", 0))
                self.border_color = selected_obj.get("border_color", "blue")
                self.transparency_label.config(text=f"Transparency: {int(self.current_transparency.get())}")
                self.max_radius = min(selected_obj["image"].size[0], selected_obj["image"].size[1]) // 2
                self.image_corner_scale.configure(to=self.max_radius)
                self.image_corner_label.config(text=f"Corner Radius: {int(self.current_corner_radius.get())} (Max: {self.max_radius})")
                self.image_border_width_label.config(text=f"Border Width: {int(self.current_border_width.get())}")
                self.transparency_label.grid()
                self.transparency_scale.grid()
                self.image_corner_label.grid()
                self.image_corner_scale.grid()
                self.image_border_width_label.grid()
                self.image_border_width_scale.grid()
                self.image_border_color_button.grid()
                self.flip_h_button.grid()
                self.flip_v_button.grid()

    def update_text_content(self, event=None):
        """Cập nhật nội dung văn bản"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "text":
            new_text = self.text_entry.get()
            selected_obj["text"] = new_text or " "
            self.apply_text_edits(selected_obj)

    def update_font(self, event=None):
        """Cập nhật phông chữ"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "text":
            selected_obj["font_name"] = self.font_combo.get()
            self.apply_text_edits(selected_obj)

    def update_font_size(self, value=None):
        """Cập nhật kích thước chữ"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "text":
            font_size = int(self.current_font_size.get())
            selected_obj["font_size"] = font_size
            self.font_size_label.config(text=f"Font Size: {font_size}")
            self.apply_text_edits(selected_obj)

    def update_font_style(self):
        """Cập nhật kiểu chữ"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "text":
            selected_obj["font_bold"] = self.font_bold.get()
            selected_obj["font_italic"] = self.font_italic.get()
            selected_obj["font_underline"] = self.font_underline.get()
            self.apply_text_edits(selected_obj)

    def pick_text_color(self):
        """Chọn màu chữ"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "text":
            color = colorchooser.askcolor(title="Choose Text Color")[1]
            if color:
                selected_obj["text_color"] = color
                self.text_color = color
                self.apply_text_edits(selected_obj)

    def update_stroke_width(self, value=None):
        """Cập nhật độ dày viền chữ"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "text":
            stroke_width = int(self.current_stroke_width.get())
            selected_obj["stroke_width"] = stroke_width
            self.stroke_width_label.config(text=f"Stroke Width: {stroke_width}")
            self.apply_text_edits(selected_obj)

    def pick_stroke_color(self):
        """Chọn màu viền chữ"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "text":
            color = colorchooser.askcolor(title="Choose Stroke Color")[1]
            if color:
                selected_obj["stroke_color"] = color
                self.stroke_color = color
                self.apply_text_edits(selected_obj)

    def update_alignment(self, event=None):
        """Cập nhật căn chỉnh văn bản"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "text":
            selected_obj["alignment"] = self.align_combo.get()
            self.apply_text_edits(selected_obj)

    def update_transparency(self, value=None):
        """Cập nhật độ trong suốt"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj:
            alpha = self.current_transparency.get() / 255
            selected_obj["alpha"] = alpha
            self.transparency_label.config(text=f"Transparency: {int(self.current_transparency.get())}")
            if selected_obj["type"] == "text":
                self.apply_text_edits(selected_obj)
            elif selected_obj["type"] == "shape":
                self.apply_shape_edits(selected_obj)
            else:
                self.apply_image_edits(selected_obj)

    def update_shape_size(self):
        """Cập nhật kích thước Shape từ cm sang pixel"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            try:
                width_cm = float(self.current_shape_width_cm.get())
                height_cm = float(self.current_shape_height_cm.get())
            except ValueError:
                width_cm = 5.0
                height_cm = 5.0
                self.current_shape_width_cm.set("5.0")
                self.current_shape_height_cm.set("5.0")
            width_cm = max(1.0, width_cm)
            height_cm = max(1.0, height_cm)
            width_pixel = int(width_cm * self.CM_TO_PIXEL)
            height_pixel = int(height_cm * self.CM_TO_PIXEL)
            selected_obj["width_cm"] = width_cm
            selected_obj["height_cm"] = height_cm
            selected_obj["width"] = width_pixel
            selected_obj["height"] = height_pixel
            self.max_radius = min(width_pixel, height_pixel) // 2
            self.shape_corner_scale.configure(to=self.max_radius)
            self.shape_corner_label.config(text=f"Corner Radius: {int(self.current_corner_radius.get())} (Max: {self.max_radius})")
            self.apply_shape_edits(selected_obj)

    def pick_shape_border_color(self):
        """Chọn màu viền Shape"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            color = colorchooser.askcolor(title="Choose Border Color")[1]
            if color:
                selected_obj["border_color"] = color
                self.border_color = color
                self.apply_shape_edits(selected_obj)

    def pick_shape_fill_color(self):
        """Chọn màu nền Shape"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            color = colorchooser.askcolor(title="Choose Fill Color")[1]
            if color:
                selected_obj["fill_color"] = color
                self.fill_color = color
                self.apply_shape_edits(selected_obj)

    def update_shape_border_width(self, value=None):
        """Cập nhật độ dày viền Shape"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            border_width = int(self.current_border_width.get())
            selected_obj["border_width"] = border_width
            self.shape_border_width_label.config(text=f"Border Width: {border_width}")
            self.apply_shape_edits(selected_obj)

    def update_shape_corner(self, value=None):
        """Cập nhật bo góc Shape"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            radius = int(self.current_corner_radius.get())
            selected_obj["corner_radius"] = radius
            self.shape_corner_label.config(text=f"Corner Radius: {radius} (Max: {self.max_radius})")
            self.apply_shape_edits(selected_obj)

    def update_image_corner(self, value=None):
        """Cập nhật bo góc ảnh"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "image":
            radius = int(self.current_corner_radius.get())
            selected_obj["round"] = radius > 0
            selected_obj["round_radius"] = radius
            self.image_corner_label.config(text=f"Corner Radius: {radius} (Max: {self.max_radius})")
            self.apply_image_edits(selected_obj)

    def update_image_border_width(self, value=None):
        """Cập nhật kích thước viền ảnh"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "image":
            border_width = int(self.current_border_width.get())
            selected_obj["border_width"] = border_width
            self.image_border_width_label.config(text=f"Border Width: {border_width}")
            self.apply_image_edits(selected_obj)

    def pick_image_border_color(self):
        """Chọn màu viền ảnh"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "image":
            color = colorchooser.askcolor(title="Choose Border Color")[1]
            if color:
                selected_obj["border_color"] = color
                self.border_color = color
                self.apply_image_edits(selected_obj)

    def flip_horizontal(self):
        """Lật ngang ảnh"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "image":
            selected_obj["flip_h"] = not selected_obj["flip_h"]
            self.apply_image_edits(selected_obj)

    def flip_vertical(self):
        """Lật dọc ảnh"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "image":
            selected_obj["flip_v"] = not selected_obj["flip_v"]
            self.apply_image_edits(selected_obj)

    def apply_text_edits(self, selected_obj):
        """Áp dụng chỉnh sửa văn bản"""
        if selected_obj and selected_obj["type"] == "text":
            self.text_editor.set_text(
                text=selected_obj["text"],
                font_name=selected_obj["font_name"],
                font_size=selected_obj["font_size"],
                font_bold=selected_obj["font_bold"],
                font_italic=selected_obj["font_italic"],
                font_underline=selected_obj["font_underline"],
                text_color=selected_obj["text_color"],
                stroke_width=selected_obj["stroke_width"],
                stroke_color=selected_obj["stroke_color"],
                alignment=selected_obj["alignment"],
                alpha=selected_obj["alpha"]
            )
            new_image = self.text_editor.render_text()
            if new_image:
                self.canvas_logic.update_object_image(selected_obj, new_image)

    def apply_shape_edits(self, selected_obj):
        """Áp dụng chỉnh sửa Shape"""
        if selected_obj and selected_obj["type"] == "shape":
            self.shape_editor.set_shape(
                shape_type=selected_obj["shape_type"],
                width=selected_obj["width"],
                height=selected_obj["height"],
                border_color=selected_obj["border_color"],
                fill_color=selected_obj["fill_color"],
                border_width=selected_obj["border_width"],
                corner_radius=selected_obj["corner_radius"],
                alpha=selected_obj["alpha"]
            )
            new_image = self.shape_editor.render_shape()
            if new_image:
                self.canvas_logic.update_object_image(selected_obj, new_image)

    def apply_image_edits(self, selected_obj):
        """Áp dụng chỉnh sửa ảnh"""
        if selected_obj and selected_obj["type"] == "image":
            self.image_editor.set_image(selected_obj["original_image"])
            if selected_obj["flip_h"]:
                self.image_editor.flip_horizontal()
            if selected_obj["flip_v"]:
                self.image_editor.flip_vertical()
            if selected_obj["round"]:
                self.image_editor.round_corners(selected_obj["round_radius"])
            if selected_obj["alpha"] < 1.0:
                self.image_editor.set_transparency(selected_obj["alpha"])
            if selected_obj["border_width"] > 0:
                self.image_editor.add_border(selected_obj["border_width"], selected_obj["border_color"])
            self.canvas_logic.update_object_image(selected_obj, self.image_editor.get_image())

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
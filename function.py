from PIL import Image, ImageTk
import uuid
import tkinter as tk
from tkinter import filedialog, ttk

class CanvasEditorLogic:
    def __init__(self, ui):
        self.ui = ui
        self.objects = []
        self.selected_object = None
        self.start_x = None
        self.start_y = None
        self.selection_rect = None

    def upload_image(self):
        """Tải hình ảnh và thêm vào danh sách objects"""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            img = Image.open(file_path).resize((100, 100), Image.Resampling.LANCZOS)
            obj_id = str(uuid.uuid4())
            obj = {
                "type": "image",
                "id": obj_id,
                "original_image": img.copy(),
                "image": img,
                "photo": ImageTk.PhotoImage(img),
                "x": 50,
                "y": 50,
                "border_color": "blue",
                "border_width": 0,
                "round": False,
                "round_radius": 0,
                "alpha": 1.0,
                "flip_h": False,
                "flip_v": False
            }
            self.objects.append(obj)
            canvas_id = self.ui.canvas.create_image(50, 50, image=obj["photo"], anchor="nw")
            obj["canvas_id"] = canvas_id
            self.clear_selection()
            self.selected_object = obj
            self.highlight_object(obj)
            self.ui.update_controls()

    def add_text(self):
        """Thêm văn bản vào canvas với loại được chọn"""
        dialog = tk.Toplevel(self.ui.root)
        dialog.title("Add Text")
        dialog.geometry("300x200")
        dialog.transient(self.ui.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Select Text Type:").pack(pady=5)
        text_type = tk.StringVar(value="Text")
        ttk.Radiobutton(dialog, text="Heading", value="Heading", variable=text_type).pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Subheading", value="Subheading", variable=text_type).pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Text", value="Text", variable=text_type).pack(anchor=tk.W, padx=10)

        ttk.Label(dialog, text="Enter Text:").pack(pady=5)
        text_entry = ttk.Entry(dialog)
        text_entry.pack(pady=5, padx=10, fill=tk.X)
        text_entry.focus()

        def submit():
            text = text_entry.get()
            if text:
                type = text_type.get()
                obj_id = str(uuid.uuid4())
                defaults = {
                    "Heading": {
                        "font_name": "Arial",
                        "font_size": 36,
                        "font_bold": True,
                        "font_italic": False,
                        "font_underline": False,
                        "text_color": "black",
                        "stroke_width": 0,
                        "stroke_color": "black",
                        "alignment": "center",
                        "alpha": 1.0
                    },
                    "Subheading": {
                        "font_name": "Arial",
                        "font_size": 24,
                        "font_bold": True,
                        "font_italic": False,
                        "font_underline": False,
                        "text_color": "black",
                        "stroke_width": 0,
                        "stroke_color": "black",
                        "alignment": "center",
                        "alpha": 1.0
                    },
                    "Text": {
                        "font_name": "Arial",
                        "font_size": 16,
                        "font_bold": False,
                        "font_italic": False,
                        "font_underline": False,
                        "text_color": "black",
                        "stroke_width": 0,
                        "stroke_color": "black",
                        "alignment": "center",
                        "alpha": 1.0
                    }
                }
                obj = {
                    "type": "text",
                    "id": obj_id,
                    "text": text,
                    "x": 50,
                    "y": 50,
                    **defaults[type]
                }
                self.objects.append(obj)
                from text import TextEditor
                editor = TextEditor()
                editor.set_text(
                    text=obj["text"],
                    font_name=obj["font_name"],
                    font_size=obj["font_size"],
                    font_bold=obj["font_bold"],
                    font_italic=obj["font_italic"],
                    font_underline=obj["font_underline"],
                    text_color=obj["text_color"],
                    stroke_width=obj["stroke_width"],
                    stroke_color=obj["stroke_color"],
                    alignment=obj["alignment"],
                    alpha=obj["alpha"]
                )
                img = editor.render_text()
                if img:
                    obj["image"] = img
                    obj["photo"] = ImageTk.PhotoImage(img)
                    canvas_id = self.ui.canvas.create_image(50, 50, image=obj["photo"], anchor="nw")
                    obj["canvas_id"] = canvas_id
                    self.clear_selection()
                    self.selected_object = obj
                    self.highlight_object(obj)
                    self.ui.update_controls()
                dialog.destroy()

        ttk.Button(dialog, text="OK", command=submit).pack(pady=10)
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

    def add_shape(self):
        """Thêm Shape vào canvas với loại được chọn"""
        dialog = tk.Toplevel(self.ui.root)
        dialog.title("Add Shape")
        dialog.geometry("300x200")
        dialog.transient(self.ui.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Select Shape Type:").pack(pady=5)
        shape_type = tk.StringVar(value="rectangle")
        ttk.Radiobutton(dialog, text="Rectangle", value="rectangle", variable=shape_type).pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Square", value="square", variable=shape_type).pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Circle", value="circle", variable=shape_type).pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Triangle", value="triangle", variable=shape_type).pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Hexagon", value="hexagon", variable=shape_type).pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Star", value="star", variable=shape_type).pack(anchor=tk.W, padx=10)

        def submit():
            type = shape_type.get()
            obj_id = str(uuid.uuid4())
            # Mặc định 5 cm x 5 cm, tương ứng 189 pixel x 189 pixel (1 cm = 37.8 pixel)
            obj = {
                "type": "shape",
                "id": obj_id,
                "shape_type": type,
                "width": 189,  # 5 cm
                "height": 189,  # 5 cm
                "width_cm": 5.0,
                "height_cm": 5.0,
                "border_color": "black",
                "fill_color": "white",
                "border_width": 2,
                "corner_radius": 0,
                "alpha": 1.0,
                "x": 50,
                "y": 50
            }
            self.objects.append(obj)
            from shape import ShapeEditor
            editor = ShapeEditor()
            editor.set_shape(
                shape_type=obj["shape_type"],
                width=obj["width"],
                height=obj["height"],
                border_color=obj["border_color"],
                fill_color=obj["fill_color"],
                border_width=obj["border_width"],
                corner_radius=obj["corner_radius"],
                alpha=obj["alpha"]
            )
            img = editor.render_shape()
            if img:
                obj["image"] = img
                obj["photo"] = ImageTk.PhotoImage(img)
                canvas_id = self.ui.canvas.create_image(50, 50, image=obj["photo"], anchor="nw")
                obj["canvas_id"] = canvas_id
                self.clear_selection()
                self.selected_object = obj
                self.highlight_object(obj)
                self.ui.update_controls()
            dialog.destroy()

        ttk.Button(dialog, text="OK", command=submit).pack(pady=10)
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

    def select_object(self, event):
        """Chọn một đối tượng tại tọa độ chuột"""
        self.clear_selection()
        if event:
            x, y = event.x, event.y
            for obj in reversed(self.objects):
                if obj["type"] in ["image", "text", "shape"] and obj.get("image"):
                    if obj["x"] <= x <= obj["x"] + obj["image"].width and obj["y"] <= y <= obj["y"] + obj["image"].height:
                        self.selected_object = obj
                        self.start_x, self.start_y = x, y
                        self.highlight_object(obj)
                        self.ui.update_controls()
                        break

    def clear_selection(self):
        """Xóa lựa chọn hiện tại"""
        self.selected_object = None
        self.start_x = None
        self.start_y = None
        if self.selection_rect:
            self.ui.canvas.delete(self.selection_rect)
            self.selection_rect = None
        self.ui.update_controls()

    def highlight_object(self, obj):
        """Đánh dấu đối tượng được chọn bằng khung đỏ"""
        if self.selection_rect:
            self.ui.canvas.delete(self.selection_rect)
        if obj["type"] in ["image", "text", "shape"] and obj.get("image"):
            x, y, w, h = obj["x"], obj["y"], obj["image"].width, obj["image"].height
            self.selection_rect = self.ui.canvas.create_rectangle(x-2, y-2, x+w+2, y+h+2, outline="red", width=2)

    def drag_object(self, event):
        """Kéo đối tượng được chọn"""
        if self.selected_object and self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.selected_object["x"] += dx
            self.selected_object["y"] += dy
            self.ui.canvas.move(self.selected_object["canvas_id"], dx, dy)
            if self.selection_rect:
                self.ui.canvas.move(self.selection_rect, dx, dy)
            self.start_x, self.start_y = event.x, event.y

    def release_object(self, event):
        """Thả đối tượng sau khi kéo"""
        pass

    def get_selected_object(self):
        """Trả về đối tượng được chọn"""
        return self.selected_object

    def update_object_image(self, obj, new_image):
        """Cập nhật hình ảnh của đối tượng"""
        if new_image:
            obj["image"] = new_image
            obj["photo"] = ImageTk.PhotoImage(new_image)
            self.ui.canvas.itemconfig(obj["canvas_id"], image=obj["photo"])
            if self.selected_object == obj:
                self.highlight_object(obj)
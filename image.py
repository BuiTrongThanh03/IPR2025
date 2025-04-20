from PIL import Image, ImageDraw, ImageOps
import numpy as np
from tkinter import colorchooser

class ImageEditor:
    def __init__(self):
        """Khởi tạo không có hình ảnh ban đầu"""
        self.image = None

    def set_image(self, image):
        """Gán hình ảnh để chỉnh sửa"""
        self.image = image.copy()

    def add_border(self, border_width, border_color):
        """Thêm viền cho hình ảnh nếu border_width > 0"""
        if self.image and border_width > 0:
            border_size = border_width
            new_img = Image.new("RGBA", (self.image.width + 2 * border_size, self.image.height + 2 * border_size), border_color)
            new_img.paste(self.image, (border_size, border_size))
            self.image = new_img
        return self

    def round_corners(self, radius):
        """Bo tròn các góc của hình ảnh"""
        if self.image:
            max_radius = min(self.image.size[0], self.image.size[1]) // 2
            radius = min(radius, max_radius)
            mask = Image.new("L", self.image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, self.image.width, self.image.height), radius=radius, fill=255)
            if self.image.mode != 'RGBA':
                self.image = self.image.convert('RGBA')
            self.image.putalpha(mask)
        return self

    def set_transparency(self, alpha):
        """Điều chỉnh độ trong suốt (0.0: trong suốt, 1.0: không trong suốt)"""
        if self.image:
            if self.image.mode != 'RGBA':
                self.image = self.image.convert('RGBA')
            alpha_value = int(255 * alpha)
            data = np.array(self.image)
            r, g, b, a = data.T
            a[...] = alpha_value
            self.image = Image.fromarray(np.array([r, g, b, a]).T)
        return self

    def flip_horizontal(self):
        """Lật ngang hình ảnh"""
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        return self

    def flip_vertical(self):
        """Lật dọc hình ảnh"""
        if self.image:
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        return self

    def get_image(self):
        """Trả về hình ảnh hiện tại"""
        return self.image

class ImageLogic:
    def __init__(self, ui, canvas_logic):
        self.ui = ui
        self.canvas_logic = canvas_logic
        self.image_editor = ImageEditor()
    def update_image_corner(self, value=None):
        """Cập nhật bo góc ảnh"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "image":
            radius = int(self.ui.current_corner_radius.get())
            selected_obj["round"] = radius > 0
            selected_obj["round_radius"] = radius
            self.ui.image_corner_label.config(text=f"Corner Radius: {radius} (Max: {self.ui.max_radius})")
            self.apply_image_edits(selected_obj)
    def update_image_border_width(self, value=None):
        """Cập nhật kích thước viền ảnh"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "image":
            border_width = int(self.ui.current_border_width.get())
            selected_obj["border_width"] = border_width
            self.ui.image_border_width_label.config(text=f"Border Width: {border_width}")
            self.apply_image_edits(selected_obj)
    def pick_image_border_color(self):
        """Chọn màu viền ảnh"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "image":
            color = colorchooser.askcolor(title="Choose Border Color")[1]
            if color:
                selected_obj["border_color"] = color
                self.ui.border_color = color
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
from PIL import Image, ImageDraw
import numpy as np
import math
from tkinter import colorchooser

class ShapeEditor:
    def __init__(self):
        """Khởi tạo ShapeEditor với các thuộc tính mặc định"""
        self.shape_type = "rectangle"
        self.width = 100  # Pixel
        self.height = 100  # Pixel
        self.border_color = "black"
        self.fill_color = "white"
        self.border_width = 2
        self.corner_radius = 0
        self.alpha = 1.0
        self.image = None

    def set_shape(self, shape_type, width, height, border_color, fill_color, border_width, corner_radius, alpha):
        """Gán các thuộc tính cho Shape"""
        self.shape_type = shape_type or "rectangle"
        self.width = max(1, int(width))
        self.height = max(1, int(height))
        self.border_color = border_color or "black"
        self.fill_color = fill_color or "white"
        self.border_width = max(0, int(border_width))
        self.corner_radius = max(0, int(corner_radius))
        self.corner_radius = min(self.corner_radius, min(self.width, self.height) // 2)
        self.alpha = min(max(0.0, float(alpha)), 1.0)
        return self

    def render_shape(self):
        """Vẽ Shape dựa trên các thuộc tính"""
        # Tính kích thước hình ảnh (bao gồm border_width và padding)
        padding = 2
        image_width = self.width + self.border_width * 2 + padding * 2
        image_height = self.height + self.border_width * 2 + padding * 2

        # Tạo hình ảnh mới với nền trong suốt
        self.image = Image.new("RGBA", (int(image_width), int(image_height)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.image)

        # Tọa độ trung tâm và dịch chuyển để có không gian cho border
        center_x = image_width / 2
        center_y = image_height / 2
        shape_width = self.width
        shape_height = self.height

        if self.shape_type == "rectangle" or self.shape_type == "square":
            if self.shape_type == "square":
                shape_width = shape_height = min(self.width, self.height)
            xy = (
                center_x - shape_width / 2,
                center_y - shape_height / 2,
                center_x + shape_width / 2,
                center_y + shape_height / 2
            )
            if self.fill_color:
                if self.corner_radius > 0:
                    draw.rounded_rectangle(xy, radius=self.corner_radius, fill=self.fill_color)
                else:
                    draw.rectangle(xy, fill=self.fill_color)
            if self.border_width > 0:
                if self.corner_radius > 0:
                    draw.rounded_rectangle(xy, radius=self.corner_radius, outline=self.border_color, width=self.border_width)
                else:
                    draw.rectangle(xy, outline=self.border_color, width=self.border_width)

        elif self.shape_type == "circle":
            radius = min(self.width, self.height) / 2
            xy = (
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius
            )
            if self.fill_color:
                draw.ellipse(xy, fill=self.fill_color)
            if self.border_width > 0:
                draw.ellipse(xy, outline=self.border_color, width=self.border_width)

        elif self.shape_type == "triangle":
            points = [
                (center_x, center_y - self.height / 2),  # Đỉnh trên
                (center_x - self.width / 2, center_y + self.height / 2),  # Góc trái dưới
                (center_x + self.width / 2, center_y + self.height / 2)   # Góc phải dưới
            ]
            if self.fill_color:
                draw.polygon(points, fill=self.fill_color)
            if self.border_width > 0:
                draw.polygon(points, outline=self.border_color, width=self.border_width)

        elif self.shape_type == "hexagon":
            radius = min(self.width, self.height) / 2
            points = []
            for i in range(6):
                angle = math.pi / 3 * i + math.pi / 6
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            if self.fill_color:
                draw.polygon(points, fill=self.fill_color)
            if self.border_width > 0:
                draw.polygon(points, outline=self.border_color, width=self.border_width)

        elif self.shape_type == "star":
            outer_radius = min(self.width, self.height) / 2
            inner_radius = outer_radius / 2
            points = []
            for i in range(10):
                angle = math.pi / 5 * i + math.pi / 2
                radius = outer_radius if i % 2 == 0 else inner_radius
                x = center_x + radius * math.cos(angle)
                y = center_y - radius * math.sin(angle)
                points.append((x, y))
            if self.fill_color:
                draw.polygon(points, fill=self.fill_color)
            if self.border_width > 0:
                draw.polygon(points, outline=self.border_color, width=self.border_width)

        # Áp dụng độ trong suốt
        if self.alpha < 1.0:
            data = np.array(self.image)
            r, g, b, a = data.T
            a[...] = int(255 * self.alpha)
            self.image = Image.fromarray(np.array([r, g, b, a]).T)

        return self.image

    def get_image(self):
        """Trả về hình ảnh Shape hiện tại"""
        return self.image

class ShapeLogic:
    def __init__(self, ui, canvas_logic):
        self.ui = ui
        self.canvas_logic = canvas_logic
        self.shape_editor = ShapeEditor()

    def update_shape_size(self):
        """Cập nhật kích thước Shape từ cm sang pixel dựa trên thanh trượt"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            width_cm = self.ui.current_shape_width_cm.get()
            height_cm = self.ui.current_shape_height_cm.get()
            width_cm = max(1.0, width_cm)
            height_cm = max(1.0, height_cm)
            width_pixel = int(width_cm * self.ui.CM_TO_PIXEL)
            height_pixel = int(height_cm * self.ui.CM_TO_PIXEL)
            selected_obj["width_cm"] = width_cm
            selected_obj["height_cm"] = height_cm
            selected_obj["width"] = width_pixel
            selected_obj["height"] = height_pixel
            self.ui.max_radius = min(width_pixel, height_pixel) // 2
            self.ui.shape_corner_scale.configure(to=self.ui.max_radius)
            self.ui.shape_corner_label.config(text=f"Corner Radius: {int(self.ui.current_corner_radius.get())} (Max: {self.ui.max_radius})")
            self.ui.shape_width_label.config(text=f"Width (cm): {width_cm:.1f}")
            self.ui.shape_height_label.config(text=f"Height (cm): {height_cm:.1f}")
            self.apply_shape_edits(selected_obj)

    def pick_shape_border_color(self):
        """Chọn màu viền Shape"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            color = colorchooser.askcolor(title="Choose Border Color")[1]
            if color:
                selected_obj["border_color"] = color
                self.ui.border_color = color
                self.apply_shape_edits(selected_obj)

    def pick_shape_fill_color(self):
        """Chọn màu nền Shape"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            color = colorchooser.askcolor(title="Choose Fill Color")[1]
            if color:
                selected_obj["fill_color"] = color
                self.ui.fill_color = color
                self.apply_shape_edits(selected_obj)

    def update_shape_border_width(self, value=None):
        """Cập nhật độ dày viền Shape"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            border_width = int(self.ui.current_border_width.get())
            selected_obj["border_width"] = border_width
            self.ui.shape_border_width_label.config(text=f"Border Width: {border_width}")
            self.apply_shape_edits(selected_obj)

    def update_shape_corner(self, value=None):
        """Cập nhật bo góc Shape"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj and selected_obj["type"] == "shape":
            radius = int(self.ui.current_corner_radius.get())
            selected_obj["corner_radius"] = radius
            self.ui.shape_corner_label.config(text=f"Corner Radius: {radius} (Max: {self.ui.max_radius})")
            self.apply_shape_edits(selected_obj)

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
from PIL import Image, ImageDraw
import numpy as np
import math

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
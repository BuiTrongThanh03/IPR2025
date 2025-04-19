from PIL import Image, ImageDraw, ImageOps
import numpy as np

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
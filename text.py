from PIL import Image, ImageDraw, ImageFont
import numpy as np

class TextEditor:
    def __init__(self):
        """Khởi tạo không có văn bản ban đầu"""
        self.text = ""
        self.font_name = "Arial"
        self.font_size = 20
        self.font_bold = False
        self.font_italic = False
        self.font_underline = False
        self.text_color = "black"
        self.stroke_width = 0
        self.stroke_color = "black"
        self.alignment = "center"
        self.alpha = 1.0
        self.image = None

    def set_text(self, text, font_name, font_size, font_bold, font_italic, font_underline, text_color, stroke_width, stroke_color, alignment, alpha):
        """Gán các thuộc tính văn bản để chỉnh sửa"""
        self.text = text or ""
        self.font_name = font_name or "Arial"
        self.font_size = max(1, int(font_size))
        self.font_bold = bool(font_bold)
        self.font_italic = bool(font_italic)
        self.font_underline = bool(font_underline)
        self.text_color = text_color or "black"
        self.stroke_width = max(0, int(stroke_width))
        self.stroke_color = stroke_color or "black"
        self.alignment = alignment or "center"
        self.alpha = min(max(0.0, float(alpha)), 1.0)
        return self

    def render_text(self):
        """Vẽ văn bản lên hình ảnh với các thuộc tính được chỉ định"""
        if not self.text:
            return None

        # Bản đồ các tên phông chữ sang tệp phông cụ thể
        font_map = {
            "Arial": {"normal": "arial.ttf", "bold": "arialbd.ttf", "italic": "ariali.ttf", "bold_italic": "arialbi.ttf"},
            "Times New Roman": {"normal": "times.ttf", "bold": "timesbd.ttf", "italic": "timesi.ttf", "bold_italic": "timesbi.ttf"},
            "Courier New": {"normal": "cour.ttf", "bold": "courbd.ttf", "italic": "couri.ttf", "bold_italic": "courbi.ttf"}
        }

        # Xác định tệp phông chữ dựa trên font_name, bold, italic
        font_file = None
        font_key = "normal"
        if self.font_bold and self.font_italic:
            font_key = "bold_italic"
        elif self.font_bold:
            font_key = "bold"
        elif self.font_italic:
            font_key = "italic"

        # Tải phông chữ
        font = None
        try:
            # Nếu font_name có trong font_map, thử tải tệp phông cụ thể
            if self.font_name in font_map:
                font_file = font_map[self.font_name][font_key]
                font = ImageFont.truetype(font_file, self.font_size)
            else:
                # Nếu không, thử tải trực tiếp bằng tên phông
                font = ImageFont.truetype(self.font_name, self.font_size)
        except:
            try:
                # Quay về Arial nếu phông không tồn tại
                font_file = font_map["Arial"][font_key]
                font = ImageFont.truetype(font_file, self.font_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", self.font_size)
                except:
                    font = ImageFont.load_default()

        # Tính kích thước văn bản
        text_bbox = font.getbbox(self.text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Thêm không gian đệm bổ sung
        padding = 10
        extra_height = 4 if self.font_underline else 0  # Tăng không gian cho gạch chân
        image_width = text_width + self.stroke_width * 2 + padding * 2
        image_height = text_height + self.stroke_width * 2 + extra_height + padding * 2

        # Tạo hình ảnh với kích thước đủ lớn
        self.image = Image.new("RGBA", (int(image_width), int(image_height)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.image)

        # Căn chỉnh văn bản
        if self.alignment == "left":
            position = (self.stroke_width + padding, self.stroke_width + padding)
        elif self.alignment == "right":
            position = (image_width - text_width - self.stroke_width - padding, self.stroke_width + padding)
        else:  # center
            position = ((image_width - text_width) / 2, self.stroke_width + padding)

        # Vẽ viền chữ (stroke)
        if self.stroke_width > 0:
            for offset_x in range(-self.stroke_width, self.stroke_width + 1):
                for offset_y in range(-self.stroke_width, self.stroke_width + 1):
                    if offset_x != 0 or offset_y != 0:
                        draw.text(
                            (position[0] + offset_x, position[1] + offset_y),
                            self.text,
                            font=font,
                            fill=self.stroke_color
                        )

        # Vẽ văn bản chính
        draw.text(position, self.text, font=font, fill=self.text_color)

        # Vẽ gạch chân thủ công nếu underline được bật
        if self.font_underline:
            # Tính vị trí gạch chân ngay dưới văn bản
            underline_y = position[1] + text_height + 2  # Đặt ngay dưới văn bản, thêm 2px
            underline_start = (position[0], underline_y)
            underline_end = (position[0] + text_width, underline_y)
            draw.line([underline_start, underline_end], fill=self.text_color, width=1)

        # Áp dụng độ trong suốt
        if self.alpha < 1.0:
            if self.image.mode != 'RGBA':
                self.image = self.image.convert('RGBA')
            data = np.array(self.image)
            r, g, b, a = data.T
            a[...] = int(255 * self.alpha)
            self.image = Image.fromarray(np.array([r, g, b, a]).T)

        return self.image

    def get_image(self):
        """Trả về hình ảnh văn bản hiện tại"""
        return self.image
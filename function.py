from PIL import Image, ImageTk
import uuid
import tkinter as tk
import json
import base64
from io import BytesIO
from tkinter import filedialog, ttk
from image import ImageEditor
from shape import ShapeEditor
from text import TextEditor


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
            img = Image.open(file_path)
            obj_id = str(uuid.uuid4())
            obj = {
                "type": "image",
                "id": obj_id,
                "original_image": img.copy(),
                "image": img,
                "photo": ImageTk.PhotoImage(img),
                "x": 50,
                "y": 50,
                "width": img.size[0],  # Store initial width
                "height": img.size[1],  # Store initial height
                "border_color": "blue",
                "border_width": 0,
                "round": False,
                "round_radius": 0,
                "alpha": 1.0,
                "flip_h": False,
                "flip_v": False,
                "locked": False
            }
            self.objects.append(obj)
            canvas_id = self.ui.canvas.create_image(50, 50, image=obj["photo"], anchor="nw")
            obj["canvas_id"] = canvas_id
            self.ui.update_object_list()
            self.clear_selection()
            self.selected_object = obj
            self.highlight_object(obj)
            self.ui.update_controls()

    def update_image_properties(self, obj, border_width=None, border_color=None, 
                               round_radius=None, alpha=None, flip_h=None, flip_v=None,
                               width=None, height=None):
        """Cập nhật thuộc tính của đối tượng hình ảnh bằng ImageEditor"""
        if obj["type"] == "image" and obj.get("original_image"):
            # Cập nhật thuộc tính
            if border_width is not None:
                obj["border_width"] = border_width
            if border_color is not None:
                obj["border_color"] = border_color
            if round_radius is not None:
                obj["round_radius"] = round_radius
                obj["round"] = round_radius > 0
            if alpha is not None:
                obj["alpha"] = alpha
            if flip_h is not None:
                obj["flip_h"] = flip_h
            if flip_v is not None:
                obj["flip_v"] = flip_v
            if width is not None:
                obj["width"] = width
            if height is not None:
                obj["height"] = height
            
            # Áp dụng các thay đổi
            editor = ImageEditor()
            editor.set_image(obj["original_image"].copy())
            
            # Resize image first
            editor.resize_image(obj["width"], obj["height"])
            
            # Áp dụng lật ngang/dọc
            if obj["flip_h"]:
                editor.flip_horizontal()
            if obj["flip_v"]:
                editor.flip_vertical()
            
            # Áp dụng bo tròn góc
            if obj["round"] and obj["round_radius"] > 0:
                editor.round_corners(obj["round_radius"])
            
            # Áp dụng độ trong suốt
            editor.set_transparency(obj["alpha"])
            
            # Áp dụng border
            editor.add_border(obj["border_width"], obj["border_color"])
            
            # Cập nhật image
            new_image = editor.get_image()
            self.update_object_image(obj, new_image)

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
                    "locked": False,
                    **defaults[type]
                }
                self.objects.append(obj)
                
                # Sử dụng TextEditor để render text
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
                    self.ui.update_object_list()
                    self.clear_selection()
                    self.selected_object = obj
                    self.highlight_object(obj)
                    self.ui.update_controls()
                dialog.destroy()

        ttk.Button(dialog, text="OK", command=submit).pack(pady=10)
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

    def update_text_properties(self, obj, text=None, font_name=None, font_size=None, 
                              font_bold=None, font_italic=None, font_underline=None,
                              text_color=None, stroke_width=None, stroke_color=None,
                              alignment=None, alpha=None):
        """Cập nhật thuộc tính của đối tượng văn bản bằng TextEditor"""
        if obj["type"] == "text":
            # Cập nhật thuộc tính nếu có
            if text is not None:
                obj["text"] = text
            if font_name is not None:
                obj["font_name"] = font_name
            if font_size is not None:
                obj["font_size"] = font_size
            if font_bold is not None:
                obj["font_bold"] = font_bold
            if font_italic is not None:
                obj["font_italic"] = font_italic
            if font_underline is not None:
                obj["font_underline"] = font_underline
            if text_color is not None:
                obj["text_color"] = text_color
            if stroke_width is not None:
                obj["stroke_width"] = stroke_width
            if stroke_color is not None:
                obj["stroke_color"] = stroke_color
            if alignment is not None:
                obj["alignment"] = alignment
            if alpha is not None:
                obj["alpha"] = alpha
            
            # Sử dụng TextEditor để render lại
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
            new_image = editor.render_text()
            self.update_object_image(obj, new_image)

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
                "width": 100,  #px
                "height": 100,  #px
                "width_cm": 5.0,
                "height_cm": 5.0,
                "border_color": "black",
                "fill_color": "white",
                "border_width": 2,
                "corner_radius": 0,
                "alpha": 1.0,
                "x": 50,
                "y": 50,
                "locked": False
            }
            self.objects.append(obj)
            
            # Sử dụng ShapeEditor để render hình
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
                self.ui.update_object_list()
                self.clear_selection()
                self.selected_object = obj
                self.highlight_object(obj)
                self.ui.update_controls()
            dialog.destroy()

        ttk.Button(dialog, text="OK", command=submit).pack(pady=10)
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

    def update_shape_properties(self, obj, shape_type=None, width=None, height=None,
                               border_color=None, fill_color=None, border_width=None,
                               corner_radius=None, alpha=None):
        """Cập nhật thuộc tính của đối tượng hình dạng bằng ShapeEditor"""
        if obj["type"] == "shape":
            # Cập nhật thuộc tính nếu có
            if shape_type is not None:
                obj["shape_type"] = shape_type
            if width is not None:
                obj["width"] = width
                obj["width_cm"] = width / 37.8  # Chuyển pixel sang cm
            if height is not None:
                obj["height"] = height
                obj["height_cm"] = height / 37.8  # Chuyển pixel sang cm
            if border_color is not None:
                obj["border_color"] = border_color
            if fill_color is not None:
                obj["fill_color"] = fill_color
            if border_width is not None:
                obj["border_width"] = border_width
            if corner_radius is not None:
                obj["corner_radius"] = corner_radius
            if alpha is not None:
                obj["alpha"] = alpha
            
            # Sử dụng ShapeEditor để render lại
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
            new_image = editor.render_shape()
            self.update_object_image(obj, new_image)

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
            self.ui.update_controls()

    # --- Thêm phương thức để chọn object từ instance (dùng cho listbox) ---
    def select_object_by_instance(self, obj_instance):
        """Chọn một đối tượng cụ thể dựa trên instance của nó."""
        if obj_instance in self.objects:
            self.clear_selection()
            self.selected_object = obj_instance
            self.highlight_object(obj_instance)
            self.ui.update_controls() # Gọi update_controls để cập nhật cả UI và listbox highlight
        else:
            self.clear_selection() # Nếu object không tồn tại, xóa lựa chọn

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
            # Sử dụng màu xanh lá cho đối tượng đã khóa, màu đỏ cho đối tượng thường
            outline_color = "green" if obj.get("locked", False) else "red"
            self.selection_rect = self.ui.canvas.create_rectangle(x-2, y-2, x+w+2, y+h+2, outline=outline_color, width=2)

    def drag_object(self, event):
        """Kéo đối tượng được chọn"""
        if (self.selected_object and self.start_x is not None and 
            self.start_y is not None and not self.selected_object.get("locked", False)):
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
        self.start_x, self.start_y = None, None

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

    def lock_object(self):
        """Khóa hoặc mở khóa đối tượng được chọn"""
        if self.selected_object:
            # Toggle the locked status
            locked = self.selected_object.get("locked", False)
            self.selected_object["locked"] = not-locked
            
            # Highlight using different color if locked
            if self.selection_rect:
                self.ui.canvas.delete(self.selection_rect)
            
            if self.selected_object["locked"]:
                # Use a different color (green) for locked objects
                x, y = self.selected_object["x"], self.selected_object["y"]
                w, h = self.selected_object["image"].width, self.selected_object["image"].height
                self.selection_rect = self.ui.canvas.create_rectangle(x-2, y-2, x+w+2, y+h+2, outline="green", width=2)
            else:
                # Use normal color (red) for unlocked objects
                self.highlight_object(self.selected_object)
            
            # Update controls in UI
            self.ui.update_controls()

    def delete_selected_object(self):
        """Xóa đối tượng được chọn khỏi canvas"""
        if self.selected_object:
            # Check if object is locked before deleting
            if self.selected_object.get("locked", False):
                return  # Don't delete locked objects
                
            # Xóa đối tượng khỏi canvas
            self.ui.canvas.delete(self.selected_object["canvas_id"])
            
            # Xóa khung chọn nếu có
            if self.selection_rect:
                self.ui.canvas.delete(self.selection_rect)
                self.selection_rect = None
                
            # Xóa đối tượng khỏi danh sách
            self.objects.remove(self.selected_object)
            
            # Đặt selected_object về None
            self.selected_object = None
            # Remove from list
            self.ui.update_object_list() 
            # Cập nhật giao diện
            self.ui.update_controls()

    def duplicate_selected_object(self):
        """Tạo bản sao của đối tượng được chọn"""
        if self.selected_object:
            # Check if object is locked before duplicating
            if self.selected_object.get("locked", False):
                return  # Don't duplicate locked objects
                
            obj = self.selected_object
            new_obj = obj.copy()  # Tạo bản sao của đối tượng
            new_obj["id"] = str(uuid.uuid4())  # ID mới
            new_obj["x"] += 20  # Dịch chuyển một chút để phân biệt
            new_obj["y"] += 20
            new_obj["locked"] = False  # Ensure the new object is unlocked
            
            # Tạo bản sao của hình ảnh nếu có
            if obj.get("image"):
                if obj["type"] == "image":
                    new_obj["original_image"] = obj["original_image"].copy()
                new_obj["image"] = obj["image"].copy()
                new_obj["photo"] = ImageTk.PhotoImage(new_obj["image"])
            
            # Thêm vào canvas
            self.objects.append(new_obj)
            canvas_id = self.ui.canvas.create_image(new_obj["x"], new_obj["y"], image=new_obj["photo"], anchor="nw")
            new_obj["canvas_id"] = canvas_id
            self.ui.update_object_list()
            # Chọn đối tượng mới
            self.clear_selection()
            self.selected_object = new_obj
            self.highlight_object(new_obj)
            self.ui.update_controls()

    def move_forward(self):
        """Di chuyển đối tượng được chọn lên một lớp (forward)"""
        if self.selected_object and not self.selected_object.get("locked", False):
            idx = self.objects.index(self.selected_object)
            if idx < len(self.objects) - 1:  # Không phải là đối tượng trên cùng
                # Hoán đổi vị trí trong danh sách objects
                next_object = self.objects[idx + 1]
                self.objects[idx], self.objects[idx + 1] = self.objects[idx + 1], self.objects[idx]
                # Sắp xếp lại trên canvas theo thứ tự chính xác
                canvas = self.ui.canvas
                # Đặt đối tượng ở trên một cách tường minh
                canvas.tag_raise(self.selected_object["canvas_id"], next_object["canvas_id"])
                # Debug để kiểm tra thứ tự hiện tại
                print("Current object order after move_forward:")
                for i, obj in enumerate(self.objects):
                    print(f"{i+1}. {obj.get('type', 'Unknown')} - {obj.get('fill_color', 'No color')}")
                # Cập nhật giao diện
                self.ui.update_object_list()
                self.ui.update_controls()

    def move_backward(self):
        """Di chuyển đối tượng được chọn xuống một lớp (backward)"""
        if self.selected_object and not self.selected_object.get("locked", False):
            idx = self.objects.index(self.selected_object)
            if idx > 0:  # Không phải là đối tượng dưới cùng
                # Hoán đổi vị trí trong danh sách objects
                prev_object = self.objects[idx - 1]
                self.objects[idx], self.objects[idx - 1] = self.objects[idx - 1], self.objects[idx]
                # Sắp xếp lại trên canvas theo thứ tự chính xác
                # Lấy ra đối tượng ở vị trí trước và sau của selected_object trong danh sách mới
                canvas = self.ui.canvas
                # Đặt đối tượng ở dưới một cách tường minh
                canvas.tag_lower(self.selected_object["canvas_id"], prev_object["canvas_id"])
                # Debug để kiểm tra thứ tự hiện tại
                print("Current object order after move_backward:")
                for i, obj in enumerate(self.objects):
                    print(f"{i+1}. {obj.get('type', 'Unknown')} - {obj.get('fill_color', 'No color')}")
                # Cập nhật giao diện
                self.ui.update_object_list()
                self.ui.update_controls()

    def move_to_front(self):
        """Di chuyển đối tượng được chọn lên lớp trên cùng (to front)"""
        if self.selected_object and not self.selected_object.get("locked", False):
            idx = self.objects.index(self.selected_object)
            if idx < len(self.objects) - 1:  # Không phải là đối tượng trên cùng
                # Di chuyển đối tượng lên cuối danh sách objects
                self.objects.append(self.objects.pop(idx))
                # Nâng đối tượng lên trên cùng canvas
                self.ui.canvas.tag_raise(self.selected_object["canvas_id"])
                if self.selection_rect:
                    self.ui.canvas.tag_raise(self.selection_rect)
                self.ui.update_object_list()
                self.ui.update_controls()

    def move_to_back(self):
        """Di chuyển đối tượng được chọn xuống lớp dưới cùng (to back)"""
        if self.selected_object and not self.selected_object.get("locked", False):
            idx = self.objects.index(self.selected_object)
            if idx > 0:  # Không phải là đối tượng dưới cùng
                # Di chuyển đối tượng xuống đầu danh sách objects
                self.objects.insert(0, self.objects.pop(idx))
                # Hạ đối tượng xuống dưới cùng canvas
                self.ui.canvas.tag_lower(self.selected_object["canvas_id"])
                if self.selection_rect:
                    self.ui.canvas.tag_lower(self.selection_rect)
                self.ui.update_object_list()
                self.ui.update_controls()

    def save_canvas(self, filename):
        """Lưu tiến trình canvas vào file JSON"""
        save_data = {
            "objects": []
        }
        for obj in self.objects:
            obj_data = obj.copy()  # Sao chép đối tượng
            # Xử lý hình ảnh để lưu dưới dạng base64
            try:
                if obj["type"] == "image":
                    if obj.get("original_image") and hasattr(obj["original_image"], "save"):
                        buffered = BytesIO()
                        obj["original_image"].save(buffered, format="PNG")
                        obj_data["original_image"] = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    if obj.get("image") and hasattr(obj["image"], "save"):
                        buffered = BytesIO()
                        obj["image"].save(buffered, format="PNG")
                        obj_data["image"] = base64.b64encode(buffered.getvalue()).decode("utf-8")
                elif obj["type"] in ["text", "shape"]:
                    if obj.get("image") and hasattr(obj["image"], "save"):
                        buffered = BytesIO()
                        obj["image"].save(buffered, format="PNG")
                        obj_data["image"] = base64.b64encode(buffered.getvalue()).decode("utf-8")
            except Exception as e:
                print(f"Error encoding image for object {obj['id']}: {e}")
                continue  # Bỏ qua đối tượng nếu có lỗi, hoặc xử lý theo cách khác
            
            # Xóa các trường không cần thiết hoặc không thể serialize
            obj_data.pop("photo", None)  # PhotoImage không thể serialize
            obj_data.pop("canvas_id", None)  # Canvas ID sẽ được tạo lại
            save_data["objects"].append(obj_data)
        
        # Lưu vào file
        try:
            with open(filename, "w") as f:
                json.dump(save_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    def load_canvas(self, filename):
        """Mở file JSON và khôi phục canvas"""
        try:
            with open(filename, "r") as f:
                save_data = json.load(f)
            
            # Xóa canvas hiện tại
            self.clear_canvas()
            
            # Tái tạo các đối tượng
            for obj_data in save_data["objects"]:
                obj = obj_data.copy()
                try:
                    # Khôi phục hình ảnh từ base64
                    if obj["type"] == "image":
                        if obj.get("original_image"):
                            img_data = base64.b64decode(obj["original_image"])
                            obj["original_image"] = Image.open(BytesIO(img_data))
                        if obj.get("image"):
                            img_data = base64.b64decode(obj["image"])
                            obj["image"] = Image.open(BytesIO(img_data))
                    elif obj["type"] in ["text", "shape"]:
                        if obj.get("image"):
                            img_data = base64.b64decode(obj["image"])
                            obj["image"] = Image.open(BytesIO(img_data))
                    
                    # Tạo PhotoImage và thêm vào canvas
                    if obj.get("image") and isinstance(obj["image"], Image.Image):
                        obj["photo"] = ImageTk.PhotoImage(obj["image"])
                        canvas_id = self.ui.canvas.create_image(obj["x"], obj["y"], image=obj["photo"], anchor="nw")
                        obj["canvas_id"] = canvas_id
                    
                    self.objects.append(obj)
                except Exception as e:
                    print(f"Error loading object {obj.get('id', 'unknown')}: {e}")
                    continue  # Bỏ qua đối tượng nếu có lỗi
            
            # Cập nhật danh sách đối tượng và giao diện
            self.ui.update_object_list()
            self.clear_selection()
            self.ui.update_controls()
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def clear_canvas(self):
        """Xóa tất cả đối tượng trên canvas"""
        for obj in self.objects:
            self.ui.canvas.delete(obj["canvas_id"])
        self.objects.clear()
        self.clear_selection()

    def export_canvas_to_image(self, file_format="PNG"):
        """Export toàn bộ nội dung trên canvas thành file ảnh."""
        # Kiểm tra xem canvas có đối tượng không
        if not self.objects:
            tk.messagebox.showwarning("Warning", "Canvas is empty. Nothing to export.")
            return False
        
        # Kiểm tra xem có đối tượng nào có hình ảnh không
        valid_objects = [obj for obj in self.objects if obj.get("image") is not None]
        if not valid_objects:
            tk.messagebox.showwarning("Warning", "No visible objects found on canvas.")
            return False
        
        try:
            # Tìm bounding box của tất cả các đối tượng
            min_x = min(obj["x"] for obj in valid_objects)
            min_y = min(obj["y"] for obj in valid_objects)
            max_x = max(obj["x"] + obj["image"].width for obj in valid_objects)
            max_y = max(obj["y"] + obj["image"].height for obj in valid_objects)
            
            # Tính kích thước của hình ảnh xuất và đảm bảo kích thước dương
            export_width = max(1, int(max_x - min_x))
            export_height = max(1, int(max_y - min_y))
            
            # Tạo hình ảnh mới với nền trong suốt
            export_image = Image.new("RGBA", (export_width, export_height), (0, 0, 0, 0))
            
            # Vẽ từng đối tượng lên hình ảnh xuất theo thứ tự z-index
            for obj in self.objects:
                if obj.get("image"):
                    obj_image = obj["image"].convert("RGBA")  # Đảm bảo chế độ RGBA
                    # Tính vị trí tương đối so với bounding box
                    paste_x = max(0, int(obj["x"] - min_x))
                    paste_y = max(0, int(obj["y"] - min_y))
                    
                    # Đảm bảo obj_image nằm trong kích thước export_image
                    if paste_x + obj_image.width > export_width or paste_y + obj_image.height > export_height:
                        # Cắt obj_image nếu cần thiết
                        crop_width = min(obj_image.width, export_width - paste_x)
                        crop_height = min(obj_image.height, export_height - paste_y)
                        if crop_width > 0 and crop_height > 0:
                            obj_image = obj_image.crop((0, 0, crop_width, crop_height))
                        else:
                            continue  # Bỏ qua đối tượng nếu nằm hoàn toàn ngoài khung
                    
                    # Paste với alpha mask
                    export_image.paste(obj_image, (paste_x, paste_y), obj_image)
            
            # Mở hộp thoại lưu file
            file_format = file_format.upper()
            extensions = {
                "PNG": ".png",
                "JPEG": ".jpg",
                "BMP": ".bmp",
                "GIF": ".gif"
            }
            default_ext = extensions.get(file_format, ".png")
            
            filetypes = []
            if file_format == "PNG":
                filetypes = [("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            elif file_format == "JPEG":
                filetypes = [("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
            else:
                filetypes = [(f"{file_format} files", f"*{default_ext}"), ("All files", "*.*")]
            
            filename = filedialog.asksaveasfilename(
                defaultextension=default_ext,
                filetypes=filetypes
            )
            
            if not filename:
                return False  # Người dùng đã hủy bỏ
            
            # Xử lý lưu file theo định dạng
            if file_format == "JPEG":
                # Chuyển sang RGB cho JPEG (loại bỏ kênh alpha)
                bg = Image.new("RGB", export_image.size, (255, 255, 255))
                bg.paste(export_image, mask=export_image.split()[3])  # Sử dụng alpha làm mask
                bg.save(filename, "JPEG", quality=95)
            else:
                export_image.save(filename, file_format)
            
            tk.messagebox.showinfo("Success", f"Canvas exported successfully to {filename}")
            return True
        
        except (ValueError, AttributeError) as e:
            tk.messagebox.showerror("Error", f"Failed to calculate export dimensions: {e}")
            return False
        except IOError as e:
            tk.messagebox.showerror("Error", f"Failed to save image: {e}\nPlease check if the destination is writable.")
            return False
        except Exception as e:
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            return False
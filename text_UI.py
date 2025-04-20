import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, font
from PIL import Image, ImageTk
from function import CanvasEditorLogic
from text import TextEditor, TextLogic
from shape import ShapeEditor, ShapeLogic
from image import ImageEditor, ImageLogic

class EditorApp:
    def __init__(self, root, logic):
        self.root = root
        self.root.title("Text, Image, and Shape Editor")
        self.canvas_logic = CanvasEditorLogic(self)
        self.text_logic = TextLogic(self, self.canvas_logic)
        self.shape_logic = ShapeLogic(self, self.canvas_logic)
        self.image_logic = ImageLogic(self, self.canvas_logic)
        self.current_font_size = tk.DoubleVar(value=20)
        self.current_stroke_width = tk.DoubleVar(value=0)
        self.current_transparency = tk.DoubleVar(value=255)
        self.current_corner_radius = tk.DoubleVar(value=0)
        self.current_border_width = tk.DoubleVar(value=0)
        self.current_shape_width_cm = tk.DoubleVar(value="5.0")
        self.current_shape_height_cm = tk.DoubleVar(value="5.0")
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

        # Create a frame for the top buttons
        self.top_button_frame = ttk.Frame(self.main_frame)
        self.top_button_frame.grid(row=1, column=0, columnspan=3, pady=5)
        self.load_button = ttk.Button(self.top_button_frame, text="Load Image", command=self.canvas_logic.upload_image)
        self.load_button.grid(row=0, column=0, padx=5)
        self.add_text_button = ttk.Button(self.top_button_frame, text="Add Text", command=self.canvas_logic.add_text)
        self.add_text_button.grid(row=0, column=1, padx=5)
        self.add_shape_button = ttk.Button(self.top_button_frame, text="Add Shape", command=self.canvas_logic.add_shape)
        self.add_shape_button.grid(row=0, column=2, padx=5)

        # Buttons for object manipulation

        self.manipulation_frame = ttk.Frame(self.main_frame)
        self.manipulation_frame.grid(row=1, column=3, pady=5)

        self.duplicate_button = ttk.Button(self.manipulation_frame, text="Duplicate", command=self.canvas_logic.duplicate_selected_object, state=tk.DISABLED)
        self.duplicate_button.grid(row=0, column=0, padx=5)

        self.delete_button = ttk.Button(self.manipulation_frame, text="Delete", command=self.canvas_logic.delete_selected_object, state=tk.DISABLED)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.lock_button = ttk.Button(self.manipulation_frame, text="Lock/Unlock", command=self.canvas_logic.lock_object)
        self.lock_button.grid(row=0, column=2, padx=5)
        self.edit_frame = ttk.LabelFrame(self.main_frame, text="Edit Properties", padding="5")
        self.edit_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))

        # Text controls
        self.text_label = ttk.Label(self.edit_frame, text="Text Content:")
        self.text_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.text_entry = ttk.Entry(self.edit_frame)
        self.text_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.text_entry.bind("<Return>", self.text_logic.update_text_content)

        self.font_label = ttk.Label(self.edit_frame, text="Font:")
        self.font_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        available_fonts = ["Arial", "Times New Roman", "Courier New"]
        self.font_combo = ttk.Combobox(self.edit_frame, values=available_fonts, state="readonly")
        self.font_combo.set("Arial")
        self.font_combo.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.font_combo.bind("<<ComboboxSelected>>", self.text_logic.update_font)

        self.font_size_label = ttk.Label(self.edit_frame, text="Font Size: 20")
        self.font_size_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        self.font_size_scale = ttk.Scale(self.edit_frame, from_=10, to=100, orient=tk.HORIZONTAL, variable=self.current_font_size, command=self.text_logic.update_font_size)
        self.font_size_scale.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.bold_check = ttk.Checkbutton(self.edit_frame, text="Bold", variable=self.font_bold, command=self.text_logic.update_font_style)
        self.bold_check.grid(row=3, column=0, pady=2)
        self.italic_check = ttk.Checkbutton(self.edit_frame, text="Italic", variable=self.font_italic, command=self.text_logic.update_font_style)
        self.italic_check.grid(row=3, column=1, pady=2)
        self.underline_check = ttk.Checkbutton(self.edit_frame, text="Underline", variable=self.font_underline, command=self.text_logic.update_font_style)
        self.underline_check.grid(row=3, column=2, pady=2)

        self.text_color_button = ttk.Button(self.edit_frame, text="Pick Text Color", command=self.text_logic.pick_text_color)
        self.text_color_button.grid(row=4, column=0, columnspan=3, pady=2)

        self.stroke_width_label = ttk.Label(self.edit_frame, text="Stroke Width: 0")
        self.stroke_width_label.grid(row=5, column=0, sticky=tk.W, pady=2)
        self.stroke_width_scale = ttk.Scale(self.edit_frame, from_=0, to=5, orient=tk.HORIZONTAL, variable=self.current_stroke_width, command=self.text_logic.update_stroke_width)
        self.stroke_width_scale.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.stroke_color_button = ttk.Button(self.edit_frame, text="Pick Stroke Color", command=self.text_logic.pick_stroke_color)
        self.stroke_color_button.grid(row=6, column=0, columnspan=3, pady=2)

        self.align_label = ttk.Label(self.edit_frame, text="Alignment:")
        self.align_label.grid(row=7, column=0, sticky=tk.W, pady=2)
        self.align_combo = ttk.Combobox(self.edit_frame, values=["left", "center", "right"], state="readonly")
        self.align_combo.set("center")
        self.align_combo.grid(row=7, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.align_combo.bind("<<ComboboxSelected>>", self.text_logic.update_alignment)

        self.transparency_label = ttk.Label(self.edit_frame, text="Transparency: 255")
        self.transparency_label.grid(row=8, column=0, sticky=tk.W, pady=2)
        self.transparency_scale = ttk.Scale(self.edit_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.current_transparency, command=self.update_transparency)
        self.transparency_scale.grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Shape controls
        self.shape_width_label = ttk.Label(self.edit_frame, text="Shape Width (cm):")
        self.shape_width_label.grid(row=9, column=0, sticky=tk.W, pady=2)
        self.shape_width_scale = ttk.Scale(self.edit_frame, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.current_shape_width_cm, command=self.shape_logic.update_shape_size)
        self.shape_width_scale.grid(row=9, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.shape_height_label = ttk.Label(self.edit_frame, text="Shape Height (cm):")
        self.shape_height_label.grid(row=10, column=0, sticky=tk.W, pady=2)
        self.shape_height_scale = ttk.Scale(self.edit_frame, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.current_shape_height_cm, command=self.shape_logic.update_shape_size)
        self.shape_height_scale.grid(row=10, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.apply_size_button = ttk.Button(self.edit_frame, text="Apply Size", command=self.shape_logic.update_shape_size)
        self.apply_size_button.grid(row=11, column=0, columnspan=3, pady=2)

        self.shape_border_color_button = ttk.Button(self.edit_frame, text="Pick Border Color", command=self.shape_logic.pick_shape_border_color)
        self.shape_border_color_button.grid(row=12, column=0, columnspan=3, pady=2)

        self.shape_fill_color_button = ttk.Button(self.edit_frame, text="Pick Fill Color", command=self.shape_logic.pick_shape_fill_color)
        self.shape_fill_color_button.grid(row=13, column=0, columnspan=3, pady=2)

        self.shape_border_width_label = ttk.Label(self.edit_frame, text="Border Width: 0")
        self.shape_border_width_label.grid(row=14, column=0, sticky=tk.W, pady=2)
        self.shape_border_width_scale = ttk.Scale(self.edit_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.current_border_width, command=self.shape_logic.update_shape_border_width)
        self.shape_border_width_scale.grid(row=14, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.shape_corner_label = ttk.Label(self.edit_frame, text="Corner Radius: 0")
        self.shape_corner_label.grid(row=15, column=0, sticky=tk.W, pady=2)
        self.shape_corner_scale = ttk.Scale(self.edit_frame, from_=0, to=self.max_radius, orient=tk.HORIZONTAL, variable=self.current_corner_radius, command=self.shape_logic.update_shape_corner)
        self.shape_corner_scale.grid(row=15, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Image controls
        self.image_corner_label = ttk.Label(self.edit_frame, text="Corner Radius: 0")
        self.image_corner_label.grid(row=16, column=0, sticky=tk.W, pady=2)
        self.image_corner_scale = ttk.Scale(self.edit_frame, from_=0, to=self.max_radius, orient=tk.HORIZONTAL, variable=self.current_corner_radius, command=self.image_logic.update_image_corner)
        self.image_corner_scale.grid(row=16, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.image_border_width_label = ttk.Label(self.edit_frame, text="Border Width: 0")
        self.image_border_width_label.grid(row=17, column=0, sticky=tk.W, pady=2)
        self.image_border_width_scale = ttk.Scale(self.edit_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.current_border_width, command=self.image_logic.update_image_border_width)
        self.image_border_width_scale.grid(row=17, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.image_border_color_button = ttk.Button(self.edit_frame, text="Pick Border Color", command=self.image_logic.pick_image_border_color)
        self.image_border_color_button.grid(row=18, column=0, columnspan=3, pady=2)

        self.flip_h_button = ttk.Button(self.edit_frame, text="Flip Horizontal", command=self.image_logic.flip_horizontal)
        self.flip_h_button.grid(row=19, column=0, pady=2)
        self.flip_v_button = ttk.Button(self.edit_frame, text="Flip Vertical", command=self.image_logic.flip_vertical)
        self.flip_v_button.grid(row=19, column=1, pady=2)

        self.canvas.bind("<Button-1>", self.canvas_logic.select_object)
        self.canvas.bind("<B1-Motion>", self.canvas_logic.drag_object)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_logic.release_object)

        self.hide_all_controls()

    def hide_all_controls(self):
        """Ẩn tất cả các điều khiển chỉnh sửa"""
        for widget in self.edit_frame.winfo_children():
            widget.grid_remove()
        
        # Disable manipulation buttons when no object is selected
        self.duplicate_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.lock_button.config(state=tk.DISABLED)
        self.lock_button.config(text="Lock/Unlock")

    def update_controls(self):
        """Cập nhật giao diện điều khiển dựa trên đối tượng được chọn"""
        self.hide_all_controls()
        selected_obj = self.canvas_logic.get_selected_object()
        # Enable/disable buttons based on selection and lock status
        if selected_obj:
            # For locked objects, only allow unlock action
            is_locked = selected_obj.get("locked", False)
            # Always enable lock button
            self.lock_button.config(state=tk.NORMAL)
            self.lock_button.config(text="Unlock" if is_locked else "Lock")
            # Enable duplicate and delete only for unlocked objects
            if is_locked:
                self.duplicate_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
            else:
                self.duplicate_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.NORMAL)
        else:
            self.duplicate_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.lock_button.config(state=tk.DISABLED)
            self.lock_button.config(text="Lock/Unlock")
        if selected_obj:
            # Disable all editing controls if object is locked
            is_locked = selected_obj.get("locked", False)
            control_state = tk.DISABLED if is_locked else tk.NORMAL
            if selected_obj["type"] == "text":
                # Setup text controls
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

                # Show text controls
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
                # Set control state based on lock status
                if is_locked:
                    self.text_entry.config(state=tk.DISABLED)
                    self.font_combo.config(state=tk.DISABLED)
                    self.font_size_scale.config(state=tk.DISABLED)
                    self.bold_check.config(state=tk.DISABLED)
                    self.italic_check.config(state=tk.DISABLED)
                    self.underline_check.config(state=tk.DISABLED)
                    self.text_color_button.config(state=tk.DISABLED)
                    self.stroke_width_scale.config(state=tk.DISABLED)
                    self.stroke_color_button.config(state=tk.DISABLED)
                    self.align_combo.config(state=tk.DISABLED)
                    self.transparency_scale.config(state=tk.DISABLED)
                else:
                    self.text_entry.config(state=tk.NORMAL)
                    self.font_combo.config(state="readonly")
                    self.font_size_scale.config(state=tk.NORMAL)
                    self.bold_check.config(state=tk.NORMAL)
                    self.italic_check.config(state=tk.NORMAL)
                    self.underline_check.config(state=tk.NORMAL)
                    self.text_color_button.config(state=tk.NORMAL)
                    self.stroke_width_scale.config(state=tk.NORMAL)
                    self.stroke_color_button.config(state=tk.NORMAL)
                    self.align_combo.config(state="readonly")
                    self.transparency_scale.config(state=tk.NORMAL)
            elif selected_obj["type"] == "shape":
                # Setup shape controls
                self.current_shape_width_cm.set(selected_obj.get("width_cm", 5.0))
                self.current_shape_height_cm.set(selected_obj.get("height_cm", 5.0))
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
                self.shape_width_label.config(text=f"Width (cm): {float(self.current_shape_width_cm.get()):.1f}")
                self.shape_height_label.config(text=f"Height (cm): {float(self.current_shape_height_cm.get()):.1f}")
                # Show shape controls
                self.shape_width_label.grid()
                self.shape_width_scale.grid()
                self.shape_height_label.grid()
                self.shape_height_scale.grid()
                self.apply_size_button.grid()
                self.shape_border_color_button.grid()
                self.shape_fill_color_button.grid()
                self.shape_border_width_label.grid()
                self.shape_border_width_scale.grid()

                # Set control state based on lock status
                if is_locked:
                    self.shape_width_scale.config(state=tk.DISABLED)
                    self.shape_height_scale.config(state=tk.DISABLED)
                    self.apply_size_button.config(state=tk.DISABLED)
                    self.shape_border_color_button.config(state=tk.DISABLED)
                    self.shape_fill_color_button.config(state=tk.DISABLED)
                    self.shape_border_width_scale.config(state=tk.DISABLED)
                    self.shape_corner_scale.config(state=tk.DISABLED)
                    self.transparency_scale.config(state=tk.DISABLED)
                else:
                    self.shape_width_scale.config(state=tk.NORMAL)
                    self.shape_height_scale.config(state=tk.NORMAL)
                    self.apply_size_button.config(state=tk.NORMAL)
                    self.shape_border_color_button.config(state=tk.NORMAL)
                    self.shape_fill_color_button.config(state=tk.NORMAL)
                    self.shape_border_width_scale.config(state=tk.NORMAL)
                    self.shape_corner_scale.config(state=tk.NORMAL)
                    self.transparency_scale.config(state=tk.NORMAL)

                # Chỉ hiển thị bo góc cho rectangle và square
                if selected_obj["shape_type"] in ["rectangle", "square"]:
                    self.shape_corner_label.grid()
                    self.shape_corner_scale.grid()
                self.transparency_label.grid()
                self.transparency_scale.grid()
            else:  # image
                # Setup image controls
                self.current_transparency.set(selected_obj.get("alpha", 1.0) * 255)
                self.current_corner_radius.set(selected_obj.get("round_radius", 0))
                self.current_border_width.set(selected_obj.get("border_width", 0))
                self.border_color = selected_obj.get("border_color", "blue")
                self.transparency_label.config(text=f"Transparency: {int(self.current_transparency.get())}")
                self.max_radius = min(selected_obj["image"].size[0], selected_obj["image"].size[1]) // 2
                self.image_corner_scale.configure(to=self.max_radius)
                self.image_corner_label.config(text=f"Corner Radius: {int(self.current_corner_radius.get())} (Max: {self.max_radius})")
                self.image_border_width_label.config(text=f"Border Width: {int(self.current_border_width.get())}")
                 # Show image controls
                self.transparency_label.grid()
                self.transparency_scale.grid()
                self.image_corner_label.grid()
                self.image_corner_scale.grid()
                self.image_border_width_label.grid()
                self.image_border_width_scale.grid()
                self.image_border_color_button.grid()
                self.flip_h_button.grid()
                self.flip_v_button.grid()
                # Set control state based on lock status
                if is_locked:
                    self.transparency_scale.config(state=tk.DISABLED)
                    self.image_corner_scale.config(state=tk.DISABLED)
                    self.image_border_width_scale.config(state=tk.DISABLED)
                    self.image_border_color_button.config(state=tk.DISABLED)
                    self.flip_h_button.config(state=tk.DISABLED)
                    self.flip_v_button.config(state=tk.DISABLED)
                else:
                    self.transparency_scale.config(state=tk.NORMAL)
                    self.image_corner_scale.config(state=tk.NORMAL)
                    self.image_border_width_scale.config(state=tk.NORMAL)
                    self.image_border_color_button.config(state=tk.NORMAL)
                    self.flip_h_button.config(state=tk.NORMAL)
                    self.flip_v_button.config(state=tk.NORMAL)

    def update_transparency(self, value=None):
        """Cập nhật độ trong suốt"""
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj:
            alpha = self.current_transparency.get() / 255
            selected_obj["alpha"] = alpha
            self.transparency_label.config(text=f"Transparency: {int(self.current_transparency.get())}")
            if selected_obj["type"] == "text":
                self.text_logic.apply_text_edits(selected_obj)
            elif selected_obj["type"] == "shape":
                self.shape_logic.apply_shape_edits(selected_obj)
            else:
                self.image_logic.apply_image_edits(selected_obj)

if __name__ == "__main__":
    root = tk.Tk()
    app = EditorApp(root)
    root.mainloop()
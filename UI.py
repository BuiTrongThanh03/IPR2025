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
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.root.title("Text, Image, and Shape Editor")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Thiết lập kích thước cửa sổ ban đầu
        window_width = 1000
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

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
        self.current_image_width = tk.DoubleVar(value=100)
        self.current_image_height = tk.DoubleVar(value=100)
        self.font_bold = tk.BooleanVar(value=False)
        self.font_italic = tk.BooleanVar(value=False)
        self.font_underline = tk.BooleanVar(value=False)
        self.text_color = "black"
        self.stroke_color = "black"
        self.border_color = "black"
        self.fill_color = "white"
        self.max_radius = 50
        self.DPI = 96
        self.CM_TO_PIXEL = self.DPI / 2.54

        # Tạo menu "File"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_project)
        self.file_menu.add_command(label="Save", command=self.save_project)
        self.file_menu.add_command(label="Export as PNG", command=lambda: self.canvas_logic.export_canvas_to_image("PNG"))
        self.file_menu.add_command(label="Export as JPEG", command=lambda: self.canvas_logic.export_canvas_to_image("JPEG"))
        self.file_menu.add_command(label="Export as BMP", command=lambda: self.canvas_logic.export_canvas_to_image("BMP"))
        self.file_menu.add_command(label="Export as GIF", command=lambda: self.canvas_logic.export_canvas_to_image("GIF"))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)

        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=(0, 5))

        self.object_list_frame = ttk.Frame(self.main_frame, width=100)
        self.object_list_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), padx=5, pady=5)
        self.main_frame.grid_rowconfigure(0, weight=6)
        self.main_frame.grid_columnconfigure(1, weight=0)
        

        self.object_listbox = tk.Listbox(self.object_list_frame, selectmode=tk.SINGLE, exportselection=False)
        self.list_scrollbar = ttk.Scrollbar(self.object_list_frame, orient=tk.VERTICAL, command=self.object_listbox.yview)
        self.object_listbox.config(yscrollcommand=self.list_scrollbar.set)
        self.list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.object_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.object_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

        self.top_button_frame = ttk.Frame(self.main_frame)
        self.top_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(5, 0), pady=(0, 5))

        self.top_button_frame.grid_columnconfigure(0, weight=1)
        self.top_button_frame.grid_columnconfigure(1, weight=1)
        self.top_button_frame.grid_columnconfigure(2, weight=1)

        self.load_button = ttk.Button(self.top_button_frame, text="Load Image", command=self.canvas_logic.upload_image)
        self.load_button.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.add_text_button = ttk.Button(self.top_button_frame, text="Add Text", command=self.canvas_logic.add_text)
        self.add_text_button.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.add_shape_button = ttk.Button(self.top_button_frame, text="Add Shape", command=self.canvas_logic.add_shape)
        self.add_shape_button.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.export_button = ttk.Button(self.top_button_frame, text="Export Image", command=self.show_export_options)
        self.export_button.grid(row=0, column=3, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.manipulation_frame = ttk.Frame(self.main_frame)
        self.manipulation_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.manipulation_frame.grid_columnconfigure(0, weight=3)
        self.manipulation_frame.grid_columnconfigure(1, weight=3)
        self.manipulation_frame.grid_columnconfigure(2, weight=3)
        self.manipulation_frame.grid_columnconfigure(3, weight=3)
        self.manipulation_frame.grid_columnconfigure(4, weight=3)

        self.duplicate_button = ttk.Button(self.manipulation_frame, text="Duplicate", command=self.canvas_logic.duplicate_selected_object, state=tk.DISABLED)
        self.duplicate_button.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.delete_button = ttk.Button(self.manipulation_frame, text="Delete", command=self.canvas_logic.delete_selected_object, state=tk.DISABLED)
        self.delete_button.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.lock_button = ttk.Button(self.manipulation_frame, text="Lock/Unlock", command=self.canvas_logic.lock_object)
        self.lock_button.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.forward_button = ttk.Button(self.manipulation_frame, text="Forward", command=self.canvas_logic.move_forward, state=tk.DISABLED)
        self.forward_button.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.backward_button = ttk.Button(self.manipulation_frame, text="Backward", command=self.canvas_logic.move_backward, state=tk.DISABLED)
        self.backward_button.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.to_front_button = ttk.Button(self.manipulation_frame, text="To Front", command=self.canvas_logic.move_to_front, state=tk.DISABLED)
        self.to_front_button.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.to_back_button = ttk.Button(self.manipulation_frame, text="To Back", command=self.canvas_logic.move_to_back, state=tk.DISABLED)
        self.to_back_button.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.edit_frame = ttk.LabelFrame(self.main_frame, text="Edit Properties", padding="5")
        self.edit_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.root.bind("<Configure>", self.on_window_resize)

        # Text controls
        self.text_label = ttk.Label(self.edit_frame, text="Text Content:")
        self.text_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.text_entry = ttk.Entry(self.edit_frame)
        self.text_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.text_entry.bind("<Return>", self.text_logic.update_text_content)

        self.font_label = ttk.Label(self.edit_frame, text="Font:")
        self.font_label.grid(row=0, column=4, sticky=tk.W, pady=2)
        available_fonts = ["Arial", "Times New Roman", "Courier New"]
        self.font_combo = ttk.Combobox(self.edit_frame, values=available_fonts, state="readonly")
        self.font_combo.set("Arial")
        self.font_combo.grid(row=0, column=5, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.font_combo.bind("<<ComboboxSelected>>", self.text_logic.update_font)

        self.font_size_label = ttk.Label(self.edit_frame, text="Font Size: 20")
        self.font_size_label.grid(row=0, column=7, sticky=tk.W, pady=2)
        self.font_size_scale = ttk.Scale(self.edit_frame, from_=10, to=100, orient=tk.HORIZONTAL, variable=self.current_font_size, command=self.text_logic.update_font_size)
        self.font_size_scale.grid(row=0, column=8, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.bold_check = ttk.Checkbutton(self.edit_frame, text="Bold", variable=self.font_bold, command=self.text_logic.update_font_style)
        self.bold_check.grid(row=1, column=0, pady=2)
        self.italic_check = ttk.Checkbutton(self.edit_frame, text="Italic", variable=self.font_italic, command=self.text_logic.update_font_style)
        self.italic_check.grid(row=1, column=1, pady=2)
        self.underline_check = ttk.Checkbutton(self.edit_frame, text="Underline", variable=self.font_underline, command=self.text_logic.update_font_style)
        self.underline_check.grid(row=1, column=2, pady=2)

        self.text_color_button = ttk.Button(self.edit_frame, text="Pick Text Color", command=self.text_logic.pick_text_color)
        self.text_color_button.grid(row=1, column=3, columnspan=3, pady=2)

        self.stroke_width_label = ttk.Label(self.edit_frame, text="Stroke Width: 0")
        self.stroke_width_label.grid(row=1, column=6, sticky=tk.W, pady=2)
        self.stroke_width_scale = ttk.Scale(self.edit_frame, from_=0, to=5, orient=tk.HORIZONTAL, variable=self.current_stroke_width, command=self.text_logic.update_stroke_width)
        self.stroke_width_scale.grid(row=1, column=7, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        self.stroke_color_button = ttk.Button(self.edit_frame, text="Pick Stroke Color", command=self.text_logic.pick_stroke_color)
        self.stroke_color_button.grid(row=1, column=10, columnspan=3, pady=2)

        # Transparency for shape and image
        self.transparency_label = ttk.Label(self.edit_frame, text="Transparency: 255")
        self.transparency_label.grid(row=7, column=0, sticky=tk.W, pady=2)
        self.transparency_scale = ttk.Scale(self.edit_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.current_transparency, command=self.update_transparency)
        self.transparency_scale.grid(row=7, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Shape controls
        self.shape_border_color_button = ttk.Button(self.edit_frame, text="Pick Border Color", command=self.shape_logic.pick_shape_border_color)
        self.shape_border_color_button.grid(row=7, column=4, columnspan=3, pady=2)

        self.shape_fill_color_button = ttk.Button(self.edit_frame, text="Pick Fill Color", command=self.shape_logic.pick_shape_fill_color)
        self.shape_fill_color_button.grid(row=7, column=7, columnspan=3, pady=2)

        self.shape_width_label = ttk.Label(self.edit_frame, text="Shape Width (cm):")
        self.shape_width_label.grid(row=8, column=0, sticky=tk.W, pady=2)
        self.shape_width_scale = ttk.Scale(self.edit_frame, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.current_shape_width_cm, command=lambda value: self.shape_logic.update_shape_size())
        self.shape_width_scale.grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.shape_height_label = ttk.Label(self.edit_frame, text="Shape Height (cm):")
        self.shape_height_label.grid(row=8, column=4, sticky=tk.W, pady=2)
        self.shape_height_scale = ttk.Scale(self.edit_frame, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.current_shape_height_cm, command=lambda value: self.shape_logic.update_shape_size())
        self.shape_height_scale.grid(row=8, column=5, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.shape_border_width_label = ttk.Label(self.edit_frame, text="Border Width: 0")
        self.shape_border_width_label.grid(row=8, column=7, sticky=tk.W, pady=2)
        self.shape_border_width_scale = ttk.Scale(self.edit_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.current_border_width, command=self.shape_logic.update_shape_border_width)
        self.shape_border_width_scale.grid(row=8, column=8, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.apply_size_button = ttk.Button(self.edit_frame, text="Apply Size", command=self.shape_logic.update_shape_size)
        self.apply_size_button.grid(row=9, column=0, columnspan=3, pady=2)

        self.shape_corner_label = ttk.Label(self.edit_frame, text="Corner Radius: 0")
        self.shape_corner_label.grid(row=14, column=0, sticky=tk.W, pady=2)
        self.shape_corner_scale = ttk.Scale(self.edit_frame, from_=0, to=self.max_radius, orient=tk.HORIZONTAL, variable=self.current_corner_radius, command=self.shape_logic.update_shape_corner)
        self.shape_corner_scale.grid(row=14, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        # Image controls
        self.image_border_color_button = ttk.Button(self.edit_frame, text="Pick Border Color", command=self.image_logic.pick_image_border_color)
        self.image_border_color_button.grid(row=7, column=3, pady=2)
        self.flip_h_button = ttk.Button(self.edit_frame, text="Flip Horizontal", command=self.image_logic.flip_horizontal)
        self.flip_h_button.grid(row=7, column=4, pady=2)
        self.flip_v_button = ttk.Button(self.edit_frame, text="Flip Vertical", command=self.image_logic.flip_vertical)
        self.flip_v_button.grid(row=7, column=5, pady=2)

        self.image_width_label = ttk.Label(self.edit_frame, text="Image Width (px):")
        self.image_width_label.grid(row=15, column=0, sticky=tk.W, pady=2)
        self.image_width_scale = ttk.Scale(self.edit_frame, from_=10, to=2000, orient=tk.HORIZONTAL, variable=self.current_image_width, command=self.image_logic.update_image_size)
        self.image_width_scale.grid(row=15, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.image_height_label = ttk.Label(self.edit_frame, text="Image Height (px):")
        self.image_height_label.grid(row=15, column=3, sticky=tk.W, pady=2)
        self.image_height_scale = ttk.Scale(self.edit_frame, from_=10, to=2000, orient=tk.HORIZONTAL, variable=self.current_image_height, command=self.image_logic.update_image_size)
        self.image_height_scale.grid(row=15, column=4, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.image_corner_label = ttk.Label(self.edit_frame, text="Corner Radius: 0")
        self.image_corner_label.grid(row=16, column=0, sticky=tk.W, pady=2)
        self.image_corner_scale = ttk.Scale(self.edit_frame, from_=0, to=self.max_radius, orient=tk.HORIZONTAL, variable=self.current_corner_radius, command=self.image_logic.update_image_corner)
        self.image_corner_scale.grid(row=16, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.image_border_width_label = ttk.Label(self.edit_frame, text="Border Width: 0")
        self.image_border_width_label.grid(row=16, column=3, sticky=tk.W, pady=2)
        self.image_border_width_scale = ttk.Scale(self.edit_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.current_border_width, command=self.image_logic.update_image_border_width)
        self.image_border_width_scale.grid(row=16, column=4, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        self.canvas.bind("<Button-1>", self.canvas_logic.select_object)
        self.canvas.bind("<B1-Motion>", self.canvas_logic.drag_object)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_logic.release_object)

        self.hide_all_controls()

    def update_object_list(self):
        """Cập nhật danh sách đối tượng trong Listbox"""
        selected_index = self.object_listbox.curselection()
        self.object_listbox.delete(0, tk.END)
        for i, obj in enumerate(self.canvas_logic.objects):
            display_text = f"{i+1}. {obj['type'].capitalize()}"
            if obj['type'] == 'text':
                display_text += f": {obj.get('text', '')[:15]}"
            elif obj['type'] == 'image':
                pass
            elif obj['type'] == 'shape':
                display_text += f" ({obj.get('shape_type', '')})"

            if obj.get("locked", False):
                display_text += " (Locked)"

            self.object_listbox.insert(tk.END, display_text)

        if selected_index and selected_index[0] < self.object_listbox.size():
            self.object_listbox.selection_set(selected_index[0])
            self.object_listbox.activate(selected_index[0])
            self.object_listbox.see(selected_index[0])
        elif self.canvas_logic.selected_object:
            try:
                idx = self.canvas_logic.objects.index(self.canvas_logic.selected_object)
                self.object_listbox.selection_set(idx)
                self.object_listbox.activate(idx)
                self.object_listbox.see(idx)
            except ValueError:
                pass

    def on_listbox_select(self, event):
        """Xử lý khi một mục trong Listbox được chọn"""
        widget = event.widget
        selected_indices = widget.curselection()
        if selected_indices:
            index = selected_indices[0]
            if 0 <= index < len(self.canvas_logic.objects):
                obj_to_select = self.canvas_logic.objects[index]
                if obj_to_select != self.canvas_logic.selected_object:
                    self.canvas_logic.select_object_by_instance(obj_to_select)

    def on_window_resize(self, event):
        if event.widget == self.root:
            width = event.width - 40
            height = event.height - 250
            if width > 0 and height > 0:
                self.canvas.config(width=width, height=height)

    def hide_all_controls(self):
        """Ẩn tất cả các điều khiển chỉnh sửa"""
        for widget in self.edit_frame.winfo_children():
            widget.grid_remove()

        self.duplicate_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.lock_button.config(state=tk.DISABLED)
        self.lock_button.config(text="Lock/Unlock")

    def update_controls(self):
        """Cập nhật giao diện điều khiển dựa trên đối tượng được chọn"""
        self.update_object_list()
        self.hide_all_controls()
        selected_obj = self.canvas_logic.get_selected_object()
        if selected_obj:
            try:
                idx = self.canvas_logic.objects.index(selected_obj)
                current_list_sel = self.object_listbox.curselection()
                if not current_list_sel or current_list_sel[0] != idx:
                    self.object_listbox.selection_clear(0, tk.END)
                    self.object_listbox.selection_set(idx)
                    self.object_listbox.activate(idx)
                    self.object_listbox.see(idx)
            except ValueError:
                self.object_listbox.selection_clear(0, tk.END)
        else:
            self.object_listbox.selection_clear(0, tk.END)

        if selected_obj:
            is_locked = selected_obj.get("locked", False)
            self.lock_button.config(state=tk.NORMAL)
            self.lock_button.config(text="Unlock" if is_locked else "Lock")
            if is_locked:
                self.duplicate_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
                self.forward_button.config(state=tk.DISABLED)
                self.backward_button.config(state=tk.DISABLED)
                self.to_front_button.config(state=tk.DISABLED)
                self.to_back_button.config(state=tk.DISABLED)
            else:
                self.duplicate_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.NORMAL)
                self.forward_button.config(state=tk.NORMAL)
                self.backward_button.config(state=tk.NORMAL)
                self.to_front_button.config(state=tk.NORMAL)
                self.to_back_button.config(state=tk.NORMAL)
        else:
            self.duplicate_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.lock_button.config(state=tk.DISABLED)
            self.lock_button.config(text="Lock/Unlock")
            self.forward_button.config(state=tk.DISABLED)
            self.backward_button.config(state=tk.DISABLED)
            self.to_front_button.config(state=tk.DISABLED)
            self.to_back_button.config(state=tk.DISABLED)

        if selected_obj:
            is_locked = selected_obj.get("locked", False)
            control_state = tk.DISABLED if is_locked else tk.NORMAL
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
                # self.transparency_label.grid()
                # self.transparency_scale.grid()

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
                    self.transparency_scale.config(state=tk.NORMAL)
            elif selected_obj["type"] == "shape":
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

                self.shape_width_label.grid()
                self.shape_width_scale.grid()
                self.shape_height_label.grid()
                self.shape_height_scale.grid()
                self.shape_border_color_button.grid()
                self.shape_fill_color_button.grid()
                self.shape_border_width_label.grid()
                self.shape_border_width_scale.grid()

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

                if selected_obj["shape_type"] in ["rectangle", "square"]:
                    self.shape_corner_label.grid()
                    self.shape_corner_scale.grid()
                self.transparency_label.grid()
                self.transparency_scale.grid()
            else:
                self.current_transparency.set(selected_obj.get("alpha", 1.0) * 255)
                self.current_corner_radius.set(selected_obj.get("round_radius", 0))
                self.current_border_width.set(selected_obj.get("border_width", 0))
                self.current_image_width.set(selected_obj.get("width", selected_obj["image"].size[0]))
                self.current_image_height.set(selected_obj.get("height", selected_obj["image"].size[1]))
                self.border_color = selected_obj.get("border_color", "blue")
                self.transparency_label.config(text=f"Transparency: {int(self.current_transparency.get())}")
                self.max_radius = min(selected_obj["image"].size[0], selected_obj["image"].size[1]) // 2
                self.image_corner_scale.configure(to=self.max_radius)
                self.image_corner_label.config(text=f"Corner Radius: {int(self.current_corner_radius.get())} (Max: {self.max_radius})")
                self.image_border_width_label.config(text=f"Border Width: {int(self.current_border_width.get())}")
                self.image_width_label.config(text=f"Image Width (px): {int(self.current_image_width.get())}")
                self.image_height_label.config(text=f"Image Height (px): {int(self.current_image_height.get())}")

                self.transparency_label.grid()
                self.transparency_scale.grid()
                self.image_width_label.grid()
                self.image_width_scale.grid()
                self.image_height_label.grid()
                self.image_height_scale.grid()
                self.image_corner_label.grid()
                self.image_corner_scale.grid()
                self.image_border_width_label.grid()
                self.image_border_width_scale.grid()
                self.image_border_color_button.grid()
                self.flip_h_button.grid()
                self.flip_v_button.grid()

                if is_locked:
                    self.transparency_scale.config(state=tk.DISABLED)
                    self.image_width_scale.config(state=tk.DISABLED)
                    self.image_height_scale.config(state=tk.DISABLED)
                    self.image_corner_scale.config(state=tk.DISABLED)
                    self.image_border_width_scale.config(state=tk.DISABLED)
                    self.image_border_color_button.config(state=tk.DISABLED)
                    self.flip_h_button.config(state=tk.DISABLED)
                    self.flip_v_button.config(state=tk.DISABLED)
                else:
                    self.transparency_scale.config(state=tk.NORMAL)
                    self.image_width_scale.config(state=tk.NORMAL)
                    self.image_height_scale.config(state=tk.NORMAL)
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

    def new_file(self):
        # Logic để tạo file mới (ví dụ: xóa tất cả đối tượng trên canvas)
        self.canvas_logic.objects.clear()
        self.canvas_logic.clear_selection()
        self.update_object_list()
        self.update_controls()

    def save_project(self):
        """Mở hộp thoại để lưu file dự án"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".edt",
            filetypes=[("Editing File", "*.edt"), ("All files", "*.*")]
        )
        if filename:
            success = self.canvas_logic.save_canvas(filename)
            if success:
                self.root.title(f"Text, Image, and Shape Editor - {filename}")
            else:
                tk.messagebox.showerror("Error", "Failed to save the project.")
    
    def open_project(self):
        """Mở hộp thoại để mở file dự án"""
        filename = filedialog.askopenfilename(
            filetypes=[("Editing File", "*.edt"), ("All files", "*.*")]
        )
        if filename:
            success = self.canvas_logic.load_canvas(filename)
            if success:
                self.root.title(f"Text, Image, and Shape Editor - {filename}")
            else:
                tk.messagebox.showerror("Error", "Failed to open the project.")
    
    def show_export_options(self):
        """Hiển thị menu chọn định dạng xuất ảnh"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Export as PNG", command=lambda: self.canvas_logic.export_canvas_to_image("PNG"))
        menu.add_command(label="Export as JPEG", command=lambda: self.canvas_logic.export_canvas_to_image("JPEG"))
        menu.add_command(label="Export as BMP", command=lambda: self.canvas_logic.export_canvas_to_image("BMP"))
        menu.add_command(label="Export as GIF", command=lambda: self.canvas_logic.export_canvas_to_image("GIF"))
        menu.post(self.export_button.winfo_rootx(), self.export_button.winfo_rooty() + self.export_button.winfo_height())
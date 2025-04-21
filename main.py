```python
import sys
import os
from pathlib import Path
from PyQt6 import QtCore, QtGui, QtWidgets
from PIL import Image
import numpy as np
from collections import deque
import tkinter as tk
from function import CanvasEditorLogic
from text_UI import EditorApp

# Code from Main_wd.py integrated here
class Ui_MainWindow(object):
    """Lớp định nghĩa giao diện người dùng chính."""
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Header frame (left)
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 300, 100))
        self.frame.setMinimumSize(QtCore.QSize(300, 100))
        self.frame.setMaximumSize(QtCore.QSize(300, 100))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame.setLineWidth(2)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(280, 80))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)

        # Header frame (right)
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(300, 0, 1066, 100))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame_2.setLineWidth(2)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(966, 32, 80, 35))
        icon = QtGui.QIcon()
        icon_path = "D:/QT_Designer/IPR_Templated.io-main/Downloads/IPR img/Icons/login.png"
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setToolTip("Log in to your account")

        # Scroll area for content
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(300, 100, 1066, 668))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.scrollAreaWidgetContents)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1066, 668))
        self.stackedWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.stackedWidget.setObjectName("stackedWidget")

        # Page 1: New template
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.New_template = QtWidgets.QGroupBox(parent=self.page)
        self.New_template.setGeometry(QtCore.QRect(7, 0, 1046, 668))
        self.New_template.setObjectName("New_template")

        # Header bar
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 1026, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.headerBar = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.headerBar.setContentsMargins(0, 0, 0, 0)
        self.Logo = QtWidgets.QToolButton(parent=self.horizontalLayoutWidget)
        self.Logo.setObjectName("Logo")
        self.headerBar.addWidget(self.Logo)
        self.ImageName = QtWidgets.QLineEdit(parent=self.horizontalLayoutWidget)
        self.ImageName.setObjectName("ImageName")
        self.headerBar.addWidget(self.ImageName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.headerBar.addItem(spacerItem)
        self.btnUpload = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.btnUpload.setStyleSheet("""
            QPushButton { 
                background-color: #4CAF50; 
                color: white; 
                border-radius: 5px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #45a049; 
            }""")
        self.btnUpload.setObjectName("btnUpload")
        self.btnUpload.setToolTip("Upload an image file")
        self.headerBar.addWidget(self.btnUpload)

        # Preview area
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 110, 1026, 448))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidgetDeleted")
        self.LogoLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.LogoLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetPreview = QtWidgets.QWidget(parent=self.horizontalLayoutWidget_2)
        self.widgetPreview.setObjectName("widgetPreview")
        self.labelPreview = QtWidgets.QLabel(parent=self.widgetPreview)
        self.labelPreview.setGeometry(QtCore.QRect(10, 10, 1006, 428))
        self.labelPreview.setObjectName("labelPreview")
        self.labelPreview.setScaledContents(True)
        self.labelPreview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LogoLayout.addWidget(self.widgetPreview)

        # Toolbar
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 558, 1026, 50))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.toolbarLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.toolbarLayout.setContentsMargins(0, 0, 0, 0)
        self.btnRotate = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnRotate.setStyleSheet("""
            QPushButton { 
                background-color: #2196F3; 
                color: white; 
                border-radius: 5px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #1e88e5; 
            }""")
        self.btnRotate.setObjectName("btnRotate")
        self.btnRotate.setToolTip("Rotate image 90° clockwise (Ctrl+R)")
        self.toolbarLayout.addWidget(self.btnRotate)
        self.btnCrop = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnCrop.setStyleSheet("""
            QPushButton { 
                background-color: #2196F3; 
                color: white; 
                border-radius: 5px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #1e88e5; 
            }""")
        self.btnCrop.setObjectName("btnCrop")
        self.btnCrop.setToolTip("Crop image by dragging (Ctrl+C)")
        self.toolbarLayout.addWidget(self.btnCrop)
        self.btnSave = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnSave.setStyleSheet("""
            QPushButton { 
                background-color: #2196F3; 
                color: white; 
                border-radius: 5px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #1e88e5; 
            }""")
        self.btnSave.setObjectName("btnSave")
        self.btnSave.setToolTip("Save edited image and switch to Tkinter (Ctrl+S)")
        self.toolbarLayout.addWidget(self.btnSave)
        self.btnDelete = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnDelete.setStyleSheet("""
            QPushButton { 
                background-color: #f44336; 
                color: white; 
                border-radius: 5px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #d32f2f; 
            }""")
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setToolTip("Delete current image (Ctrl+D)")
        self.toolbarLayout.addWidget(self.btnDelete)
        self.btnUndo = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnUndo.setStyleSheet("""
            QPushButton { 
                background-color: #ff9800; 
                color: white; 
                border-radius: 5px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #fb8c00; 
            }""")
        self.btnUndo.setObjectName("btnUndo")
        self.btnUndo.setToolTip("Undo last action (Ctrl+Z)")
        self.toolbarLayout.addWidget(self.btnUndo)

        # Footer
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 608, 1026, 50))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.FooterLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.FooterLayout.setContentsMargins(0, 0, 0, 0)
        self.FooterEdit = QtWidgets.QLineEdit(parent=self.horizontalLayoutWidget_4)
        self.FooterEdit.setObjectName("FooterEdit")
        self.FooterEdit.setToolTip("Enter footer text")
        self.FooterLayout.addWidget(self.FooterEdit)
        self.stackedWidget.addWidget(self.page)

        # Page 2: Placeholder
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Sidebar
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 100, 300, 668))
        self.listWidget.setObjectName("listWidget")
        icon_paths = [
            "C:/Users/Admin/Downloads/IPR img/Icons/template.png",
            "C:/Users/Admin/Downloads/IPR img/Icons/API.png",
            "C:/Users/Admin/Downloads/IPR img/Icons/file.png",
            "C:/Users/Admin/Downloads/IPR img/Icons/rendering.png",
            ""
        ]
        items = ["My templates", "API integration", "Render", "Embed", "Playground"]
        for i, (icon_path, text) in enumerate(zip(icon_paths, items)):
            item = QtWidgets.QListWidgetItem()
            if icon_path and os.path.exists(icon_path):
                item.setIcon(QtGui.QIcon(icon_path))
            item.setText(text)
            self.listWidget.addItem(item)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Editor"))
        self.label_2.setText(_translate("MainWindow", "_Templated.io"))
        self.pushButton.setText(_translate("MainWindow", "Log In"))
        self.New_template.setTitle(_translate("MainWindow", "Create a new template"))
        self.Logo.setText(_translate("MainWindow", "..."))
        self.ImageName.setText(_translate("MainWindow", "ImageName"))
        self.btnUpload.setText(_translate("MainWindow", "Upload"))
        self.labelPreview.setText(_translate("MainWindow", "Logo Preview"))
        self.btnRotate.setText(_translate("MainWindow", "Rotate"))
        self.btnCrop.setText(_translate("MainWindow", "Crop"))
        self.btnSave.setText(_translate("MainWindow", "Save"))
        self.btnDelete.setText(_translate("MainWindow", "Delete"))
        self.btnUndo.setText(_translate("MainWindow", "Undo"))
        self.FooterEdit.setText(_translate("MainWindow", "Footer"))

class CropLabel(QtWidgets.QLabel):
    """Lớp QLabel tùy chỉnh hỗ trợ cắt ảnh với phản hồi trực quan."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.start_pos = None
        self.end_pos = None
        self.cropping = False
        self.crop_mode = False
        self.parent_window = parent
        self.scale_factor = 1.0
        self.setAcceptDrops(True)

    def enter_crop_mode(self):
        self.crop_mode = True
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        self.update()

    def exit_crop_mode(self):
        self.crop_mode = False
        self.cropping = False
        self.start_pos = None
        self.end_pos = None
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.parent_window.current_image and self.crop_mode:
            self.cropping = True
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
            self.update()

    def mouseMoveEvent(self, event):
        if self.cropping:
            self.end_pos = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.cropping:
            self.cropping = False
            self.apply_crop()
            self.exit_crop_mode()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape and self.crop_mode:
            self.exit_crop_mode()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        if self.crop_mode and not self.cropping:
            painter.setOpacity(0.5)
            painter.setBrush(QtGui.QColor(0, 0, 0, 128))
            painter.drawRect(self.rect())
            painter.setOpacity(1.0)
            painter.setFont(QtGui.QFont("Arial", 16))
            painter.setPen(QtGui.QColor(255, 255, 255))
            text = "Drag to crop"
            text_rect = painter.fontMetrics().boundingRect(text)
            text_pos = QtCore.QPoint(
                (self.width() - text_rect.width()) // 2,
                (self.height() - text_rect.height()) // 2
            )
            painter.drawText(text_pos, text)
        if self.cropping and self.start_pos and self.end_pos:
            painter.setOpacity(1.0)
            pen = QtGui.QPen(QtGui.QColor(255, 0, 0), 3, QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            rect = QtCore.QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)

    def wheelEvent(self, event):
        if self.parent_window.current_image:
            angle = event.angleDelta().y()
            if angle > 0:
                self.scale_factor *= 1.1
            else:
                self.scale_factor /= 1.1
            self.scale_factor = max(0.1, min(self.scale_factor, 5.0))
            self.parent_window.display_image()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                self.parent_window.load_image(file_path)
                break

    def apply_crop(self):
        if not self.parent_window.current_image:
            return
        label_size = self.size()
        image_size = self.parent_window.current_image.size
        pixmap = self.pixmap()
        if not pixmap:
            return
        pixmap_size = pixmap.size()
        scale_x = image_size[0] / pixmap_size.width()
        scale_y = image_size[1] / pixmap_size.height()
        left = int(min(self.start_pos.x(), self.end_pos.x()) * scale_x)
        top = int(min(self.start_pos.y(), self.end_pos.y()) * scale_y)
        right = int(max(self.start_pos.x(), self.end_pos.x()) * scale_x)
        bottom = int(max(self.start_pos.y(), self.end_pos.y()) * scale_y)
        left = max(0, min(left, image_size[0]))
        top = max(0, min(top, image_size[1]))
        right = max(0, min(right, image_size[0]))
        bottom = max(0, min(bottom, image_size[1]))
        if left < right and top < bottom:
            self.parent_window.history.append(self.parent_window.current_image.copy())
            self.current_image = self.parent_window.current_image.crop((left, top, right, bottom))
            self.parent_window.display_image()

class MainWindow(QtWidgets.QMainWindow):
    """Lớp chính xử lý logic và sự kiện của ứng dụng PyQt6."""
    def __init__(self, on_save_callback):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.on_save_callback = on_save_callback

        # Thay labelPreview bằng CropLabel
        self.ui.labelPreview.deleteLater()
        self.labelPreview = CropLabel(self.ui.widgetPreview)
        self.labelPreview.setObjectName("labelPreview")
        self.labelPreview.setScaledContents(True)
        self.labelPreview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelPreview.setText("Logo Preview")
        self.labelPreview.setGeometry(10, 10, 1006, 428)
        self.labelPreview.parent_window = self
        self.labelPreview.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        # Khởi tạo biến
        self.original_image = None
        self.current_image = None
        self.image_path = None
        self.history = deque(maxlen=10)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

        # Kết nối sự kiện
        self.ui.btnUpload.clicked.connect(self.upload_image)
        self.ui.btnRotate.clicked.connect(self.rotate_image)
        self.ui.btnCrop.clicked.connect(self.start_crop)
        self.ui.btnSave.clicked.connect(self.save_image)
        self.ui.btnDelete.clicked.connect(self.delete_image)
        self.ui.btnUndo.clicked.connect(self.undo)
        self.ui.pushButton.clicked.connect(self.show_login_message)
        self.ui.listWidget.itemClicked.connect(self.switch_page)

        # Phím tắt
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, self.rotate_image)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"), self, self.start_crop)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, self.save_image)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+D"), self, self.delete_image)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self, self.undo)

        # Điều chỉnh kích thước cửa sổ
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.resize(int(min(screen.width() * 0.9, 1366)), int(min(screen.height() * 0.9, 768)))
        self.fix_missing_icons()
        self.debug_buttons()

    def debug_buttons(self):
        buttons = {
            "btnUpload": self.ui.btnUpload,
            "btnRotate": self.ui.btnRotate,
            "btnCrop": self.ui.btnCrop,
            "btnSave": self.ui.btnSave,
            "btnDelete": self.ui.btnDelete,
            "btnUndo": self.ui.btnUndo,
        }
        for name, button in buttons.items():
            try:
                print(f"{name}: Visible={button.isVisible()}, Enabled={button.isEnabled()}, Geometry={button.geometry()}")
            except AttributeError:
                print(f"Error: {name} not found in UI.")

    def fix_missing_icons(self):
        icon_paths = []
        for widget_name, path in icon_paths:
            if not os.path.exists(path):
                print(f"Warning: Icon not found at {path}")
                if widget_name == "pushButton":
                    self.ui.pushButton.setIcon(QtGui.QIcon())
                elif widget_name == "listWidget":
                    for i in range(self.ui.listWidget.count()):
                        self.ui.listWidget.item(i).setIcon(QtGui.QIcon())

    def switch_page(self, item):
        index = self.ui.listWidget.row(item)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page if index == 0 else self.ui.page_2)
        print(f"Switched to page index: {self.ui.stackedWidget.currentIndex()}")

    def upload_image(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        try:
            progress = QtWidgets.QProgressDialog("Loading image...", "Cancel", 0, 100, self)
            progress.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
            progress.setAutoClose(True)
            progress.show()
            QtCore.QCoreApplication.processEvents()
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            if self.original_image.mode not in ('RGB', 'L'):
                self.original_image = self.original_image.convert('RGB')
            self.current_image = self.original_image.copy()
            self.history.clear()
            self.display_image()
            file_name = os.path.basename(file_path)
            self.ui.ImageName.setText(file_name)
            progress.setValue(100)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def display_image(self):
        if self.current_image:
            image_array = np.array(self.current_image)
            height, width = image_array.shape[:2]
            bytes_per_line = 3 * width if len(image_array.shape) == 3 else width
            format_type = QtGui.QImage.Format.Format_RGB888 if len(image_array.shape) == 3 else QtGui.QImage.Format.Format_Grayscale8
            q_image = QtGui.QImage(image_array.data, width, height, bytes_per_line, format_type)
            pixmap = QtGui.QPixmap.fromImage(q_image)
            scaled_size = self.labelPreview.size() * self.labelPreview.scale_factor
            scaled_pixmap = pixmap.scaled(
                scaled_size,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            self.labelPreview.setPixmap(scaled_pixmap)

    def rotate_image(self):
        if self.current_image:
            self.history.append(self.current_image.copy())
            self.current_image = self.current_image.rotate(-90, expand=True)
            self.display_image()

    def start_crop(self):
        if self.current_image:
            self.labelPreview.enter_crop_mode()

    def save_image(self):
        """Lưu ảnh và chuyển sang giao diện Tkinter."""
        if self.current_image:
            file_dialog = QtWidgets.QFileDialog(self)
            file_path, _ = file_dialog.getSaveFileName(
                self, "Save Image", self.ui.ImageName.text(), "Images (*.png *.jpg *.jpeg)"
            )
            if file_path:
                try:
                    progress = QtWidgets.QProgressDialog("Saving image...", "Cancel", 0, 100, self)
                    progress.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
                    progress.setAutoClose(True)
                    progress.show()
                    QtCore.QCoreApplication.processEvents()
                    self.current_image.save(file_path)
                    progress.setValue(100)
                    QtWidgets.QMessageBox.information(self, "Success", "Image saved successfully!")
                    # Gọi callback để đóng PyQt6 và mở Tkinter
                    self.on_save_callback(file_path)
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")

    def delete_image(self):
        self.current_image = None
        self.original_image = None
        self.image_path = None
        self.history.clear()
        self.labelPreview.clear()
        self.labelPreview.setText("Logo Preview")
        self.ui.ImageName.setText("ImageName")
        self.ui.FooterEdit.setText("Footer")
        self.labelPreview.scale_factor = 1.0
        self.labelPreview.exit_crop_mode()

    def undo(self):
        if self.history:
            self.current_image = self.history.pop()
            self.display_image()
        else:
            QtWidgets.QMessageBox.information(self, "Undo", "No actions to undo.")

    def show_login_message(self):
        QtWidgets.QMessageBox.information(self, "Login", "Login functionality not implemented yet.")

    def resizeEvent(self, event):
        window_size = self.centralWidget().size()
        window_width = window_size.width()
        window_height = window_size.height()
        header_height = 100
        sidebar_width = window_width // 4
        content_width = window_width - sidebar_width
        self.ui.frame.setGeometry(0, 0, sidebar_width, header_height)
        self.ui.frame_2.setGeometry(sidebar_width, 0, content_width, header_height)
        self.ui.pushButton.setGeometry(content_width - 100, (header_height - 35) // 2, 80, 35)
        content_height = window_height - header_height
        self.ui.listWidget.setGeometry(0, 100, sidebar_width, content_height)
        self.ui.scrollArea.setGeometry(sidebar_width, 100, content_width, content_height)
        self.ui.stackedWidget.setMinimumSize(content_width, content_height)
        self.ui.New_template.setGeometry(7, 0, content_width - 20, content_height - 10)
        self.ui.horizontalLayoutWidget.setGeometry(10, 30, content_width - 40, 80)
        self.ui.horizontalLayoutWidget_2.setGeometry(10, 110, content_width - 40, content_height - 220)
        self.ui.horizontalLayoutWidget_3.setGeometry(10, content_height - 110, content_width - 40, 50)
        self.ui.horizontalLayoutWidget_4.setGeometry(10, content_height - 60, content_width - 40, 50)
        self.labelPreview.setGeometry(10, 10, content_width - 60, content_height - 240)
        if self.current_image:
            self.display_image()
        super().resizeEvent(event)

def run_tkinter(saved_image_path=None):
    """Khởi động giao diện Tkinter."""
    root = tk.Tk()
    logic = CanvasEditorLogic(None)
    ui = EditorApp(root, logic)
    logic.ui = ui
    # Nếu có đường dẫn ảnh đã lưu, có thể truyền vào logic hoặc ui để xử lý
    if saved_image_path:
        # Giả sử CanvasEditorLogic có phương thức để tải ảnh
        try:
            logic.load_image(saved_image_path)
        except AttributeError:
            print(f"Warning: CanvasEditorLogic does not have load_image method. Saved image path: {saved_image_path}")
    root.mainloop()

def run_pyqt():
    """Khởi động ứng dụng PyQt6 và xử lý chuyển đổi sang Tkinter khi lưu."""
    app = QtWidgets.QApplication(sys.argv)
    
    def on_save_callback(file_path):
        # Đóng ứng dụng PyQt6
        window.close()
        app.quit()
        # Chạy Tkinter với đường dẫn ảnh đã lưu
        run_tkinter(file_path)
    
    window = MainWindow(on_save_callback)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    # Chạy PyQt6 trước
    run_pyqt()

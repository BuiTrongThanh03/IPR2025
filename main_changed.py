import sys
import os
from pathlib import Path
from PyQt6 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from collections import deque
import tkinter as tk
from function import CanvasEditorLogic
from UI import EditorApp

class Ui_MainWindow(object):
    """Lớp định nghĩa giao diện người dùng chính."""
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 700)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Header frame (left)
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 150, 80))
        self.frame.setMinimumSize(QtCore.QSize(150, 80))
        self.frame.setMaximumSize(QtCore.QSize(150, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame.setLineWidth(2)
        self.frame.setStyleSheet("background-color: #FFFFFF;")
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(130, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #000000;")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)

        # Header frame (right)
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(150, 0, 1050, 80))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame_2.setLineWidth(2)
        self.frame_2.setStyleSheet("background-color: #FFFFFF;")
        self.frame_2.setObjectName("frame_2")
        self.header_label = QtWidgets.QLabel(parent=self.frame_2)
        self.header_label.setGeometry(QtCore.QRect(0, 0, 1050, 80))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.header_label.setFont(font)
        self.header_label.setStyleSheet("color: #000000;")
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_label.setObjectName("header_label")

        # Scroll area for content
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(150, 80, 1050, 620))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.scrollAreaWidgetContents)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1050, 620))
        self.stackedWidget.setStyleSheet("background-color: #FFFFFF;")
        self.stackedWidget.setObjectName("stackedWidget")

        # Page 1: New template
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.New_template = QtWidgets.QGroupBox(parent=self.page)
        self.New_template.setGeometry(QtCore.QRect(7, 0, 1036, 620))
        self.New_template.setStyleSheet("background-color: #FFFFFF; color: #000000;")
        self.New_template.setObjectName("New_template")

        # Header bar
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 1016, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.headerBar = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.headerBar.setContentsMargins(0, 0, 0, 0)
        self.ImageName = QtWidgets.QLineEdit(parent=self.horizontalLayoutWidget)
        self.ImageName.setStyleSheet("color: #000000;")
        self.ImageName.setObjectName("ImageName")
        self.headerBar.addWidget(self.ImageName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.headerBar.addItem(spacerItem)
        self.btnUpload = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.btnUpload.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.btnUpload.setObjectName("btnUpload")
        self.btnUpload.setToolTip("Upload a background image")
        self.headerBar.addWidget(self.btnUpload)

        # Preview area
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 110, 816, 400))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.LogoLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.LogoLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetPreview = QtWidgets.QWidget(parent=self.horizontalLayoutWidget_2)
        self.widgetPreview.setObjectName("widgetPreview")
        self.labelPreview = QtWidgets.QLabel(parent=self.widgetPreview)
        self.labelPreview.setGeometry(QtCore.QRect(10, 10, 796, 380))
        self.labelPreview.setStyleSheet("color: #000000;")
        self.labelPreview.setObjectName("labelPreview")
        self.labelPreview.setScaledContents(False)
        self.labelPreview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LogoLayout.addWidget(self.widgetPreview)

        # Sidebar phụ với QTabWidget
        self.sidebarWidget = QtWidgets.QWidget(parent=self.New_template)
        self.sidebarWidget.setGeometry(QtCore.QRect(826, 110, 200, 400))
        self.sidebarWidget.setObjectName("sidebarWidget")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebarWidget)
        self.sidebarLayout.setContentsMargins(5, 5, 5, 5)

        self.tabWidget = QtWidgets.QTabWidget(parent=self.sidebarWidget)
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #D1D5DB; 
                top: -1px; 
                background-color: #FFFFFF;
            }
            QTabBar::tab { 
                background: #E5E7EB; 
                color: #000000;
                padding: 8px; 
                margin-right: 2px; 
            }
            QTabBar::tab:selected { 
                background: #FFFFFF;
                color: #000000;
                border-bottom: none; 
            }
        """)

        # Tab Header
        self.headerTab = QtWidgets.QWidget()
        self.headerTabLayout = QtWidgets.QFormLayout(self.headerTab)
        self.headerTabLayout.setSpacing(10)
        self.headerTabLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.headerTabLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.HeaderEdit = QtWidgets.QLineEdit(parent=self.headerTab)
        self.HeaderEdit.setStyleSheet("color: #000000;")
        self.HeaderEdit.setPlaceholderText("Enter header text")
        self.headerTabLayout.addRow("Text:", self.HeaderEdit)
        self.headerXSpinBox = QtWidgets.QSpinBox(parent=self.headerTab)
        self.headerXSpinBox.setStyleSheet("color: #000000;")
        self.headerXSpinBox.setRange(0, 800)
        self.headerXSpinBox.setValue(0)
        self.headerTabLayout.addRow("X:", self.headerXSpinBox)
        self.headerYSpinBox = QtWidgets.QSpinBox(parent=self.headerTab)
        self.headerYSpinBox.setStyleSheet("color: #000000;")
        self.headerYSpinBox.setRange(0, 600)
        self.headerYSpinBox.setValue(120)
        self.headerTabLayout.addRow("Y:", self.headerYSpinBox)
        self.headerFontCombo = QtWidgets.QComboBox(parent=self.headerTab)
        self.headerFontCombo.setStyleSheet("color: #000000;")
        self.headerFontCombo.addItems(["Arial", "Times New Roman", "Calibri", "Helvetica", "Comic Sans MS"])
        self.headerTabLayout.addRow("Font:", self.headerFontCombo)
        self.headerSizeSpinBox = QtWidgets.QSpinBox(parent=self.headerTab)
        self.headerSizeSpinBox.setStyleSheet("color: #000000;")
        self.headerSizeSpinBox.setRange(8, 72)
        self.headerSizeSpinBox.setValue(36)
        self.headerTabLayout.addRow("Size:", self.headerSizeSpinBox)
        self.headerColorButton = QtWidgets.QPushButton(parent=self.headerTab)
        self.headerColorButton.setText("Choose Color")
        self.headerColorButton.setMinimumSize(QtCore.QSize(100, 30))
        self.headerColorButton.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.headerTabLayout.addRow("Color:", self.headerColorButton)
        self.btnApplyHeader = QtWidgets.QPushButton(parent=self.headerTab)
        self.btnApplyHeader.setText("Apply Header")
        self.btnApplyHeader.setMinimumSize(QtCore.QSize(100, 30))
        self.btnApplyHeader.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.headerTabLayout.addRow(self.btnApplyHeader)
        self.tabWidget.addTab(self.headerTab, "Header")

        # Tab Footer
        self.footerTab = QtWidgets.QWidget()
        self.footerTabLayout = QtWidgets.QFormLayout(self.footerTab)
        self.footerTabLayout.setSpacing(10)
        self.footerTabLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.footerTabLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.FooterEdit = QtWidgets.QLineEdit(parent=self.footerTab)
        self.FooterEdit.setStyleSheet("color: #000000;")
        self.FooterEdit.setPlaceholderText("Enter footer text")
        self.footerTabLayout.addRow("Text:", self.FooterEdit)
        self.footerXSpinBox = QtWidgets.QSpinBox(parent=self.footerTab)
        self.footerXSpinBox.setStyleSheet("color: #000000;")
        self.footerXSpinBox.setRange(0, 800)
        self.footerXSpinBox.setValue(0)
        self.footerTabLayout.addRow("X:", self.footerXSpinBox)
        self.footerYSpinBox = QtWidgets.QSpinBox(parent=self.footerTab)
        self.footerYSpinBox.setStyleSheet("color: #000000;")
        self.footerYSpinBox.setRange(0, 600)
        self.footerYSpinBox.setValue(550)
        self.footerTabLayout.addRow("Y:", self.footerYSpinBox)
        self.footerFontCombo = QtWidgets.QComboBox(parent=self.footerTab)
        self.footerFontCombo.setStyleSheet("color: #000000;")
        self.footerFontCombo.addItems(["Arial", "Times New Roman", "Calibri", "Helvetica", "Comic Sans MS"])
        self.footerTabLayout.addRow("Font:", self.footerFontCombo)
        self.footerSizeSpinBox = QtWidgets.QSpinBox(parent=self.footerTab)
        self.footerSizeSpinBox.setStyleSheet("color: #000000;")
        self.footerSizeSpinBox.setRange(8, 72)
        self.footerSizeSpinBox.setValue(36)
        self.footerTabLayout.addRow("Size:", self.footerSizeSpinBox)
        self.footerColorButton = QtWidgets.QPushButton(parent=self.footerTab)
        self.footerColorButton.setText("Choose Color")
        self.footerColorButton.setMinimumSize(QtCore.QSize(100, 30))
        self.footerColorButton.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.footerTabLayout.addRow("Color:", self.footerColorButton)
        self.btnApplyFooter = QtWidgets.QPushButton(parent=self.footerTab)
        self.btnApplyFooter.setText("Apply Footer")
        self.btnApplyFooter.setMinimumSize(QtCore.QSize(100, 30))
        self.btnApplyFooter.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.footerTabLayout.addRow(self.btnApplyFooter)
        self.tabWidget.addTab(self.footerTab, "Footer")

        # Tab Logo
        self.logoTab = QtWidgets.QWidget()
        self.logoTabLayout = QtWidgets.QFormLayout(self.logoTab)
        self.logoTabLayout.setSpacing(10)
        self.logoTabLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.logoTabLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.btnUploadLogo = QtWidgets.QPushButton(parent=self.logoTab)
        self.btnUploadLogo.setText("Upload Logo")
        self.btnUploadLogo.setMinimumSize(QtCore.QSize(100, 30))
        self.btnUploadLogo.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.logoTabLayout.addRow(self.btnUploadLogo)
        self.logoXSpinBox = QtWidgets.QSpinBox(parent=self.logoTab)
        self.logoXSpinBox.setStyleSheet("color: #000000;")
        self.logoXSpinBox.setRange(0, 800)
        self.logoXSpinBox.setValue(10)
        self.logoTabLayout.addRow("X:", self.logoXSpinBox)
        self.logoYSpinBox = QtWidgets.QSpinBox(parent=self.logoTab)
        self.logoYSpinBox.setStyleSheet("color: #000000;")
        self.logoYSpinBox.setRange(0, 600)
        self.logoYSpinBox.setValue(10)
        self.logoTabLayout.addRow("Y:", self.logoYSpinBox)
        self.btnApplyLogo = QtWidgets.QPushButton(parent=self.logoTab)
        self.btnApplyLogo.setText("Apply Logo")
        self.btnApplyLogo.setMinimumSize(QtCore.QSize(100, 30))
        self.btnApplyLogo.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.logoTabLayout.addRow(self.btnApplyLogo)
        self.tabWidget.addTab(self.logoTab, "Logo")

        self.sidebarLayout.addWidget(self.tabWidget)
        self.sidebarLayout.addStretch()

        # Toolbar
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 510, 1016, 50))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.toolbarLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.toolbarLayout.setContentsMargins(0, 0, 0, 0)
        self.btnRotate = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnRotate.setStyleSheet("""
            QPushButton { 
                background-color: #6B7280; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #9CA3AF; 
            }""")
        self.btnRotate.setObjectName("btnRotate")
        self.btnRotate.setToolTip("Rotate image 90° clockwise (Ctrl+R)")
        self.toolbarLayout.addWidget(self.btnRotate)
        self.btnCrop = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnCrop.setStyleSheet("""
            QPushButton { 
                background-color: #6B7280; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #9CA3AF; 
            }""")
        self.btnCrop.setObjectName("btnCrop")
        self.btnCrop.setToolTip("Crop image by dragging (Ctrl+C)")
        self.toolbarLayout.addWidget(self.btnCrop)
        self.btnSave = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnSave.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.btnSave.setObjectName("btnSave")
        self.btnSave.setToolTip("Save template (Ctrl+S)")
        self.toolbarLayout.addWidget(self.btnSave)
        self.btnDelete = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnDelete.setStyleSheet("""
            QPushButton { 
                background-color: #DC143C; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #F08080; 
            }""")
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setToolTip("Delete template (Ctrl+D)")
        self.toolbarLayout.addWidget(self.btnDelete)
        self.btnUndo = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnUndo.setStyleSheet("""
            QPushButton { 
                background-color: #F4A261; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #F5B041; 
            }""")
        self.btnUndo.setObjectName("btnUndo")
        self.btnUndo.setToolTip("Undo last action (Ctrl+Z)")
        self.toolbarLayout.addWidget(self.btnUndo)
        self.btnHighQuality = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnHighQuality.setStyleSheet("""
            QPushButton { 
                background-color: #9370DB; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #BDA0E3; 
            }""")
        self.btnHighQuality.setObjectName("btnHighQuality")
        self.btnHighQuality.setToolTip("Toggle high quality preview")
        self.toolbarLayout.addWidget(self.btnHighQuality)

        self.stackedWidget.addWidget(self.page)

        # Page 2: Placeholder
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Sidebar trái (My template, Edit)
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 80, 150, 620))
        self.listWidget.setStyleSheet("background-color: #FFFFFF; color: #000000;")
        self.listWidget.setObjectName("listWidget")
        icon_paths = [
            "C:/Users/Admin/Downloads/IPR img/Icons/template.png",
            "C:/Users/Admin/Downloads/IPR img/Icons/edit.png",
        ]
        items = ["My template", "Edit"]
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Template Editor"))
        self.label_2.setText(_translate("MainWindow", "_Templated.io"))
        self.header_label.setText(_translate("MainWindow", "_Templated.io"))
        self.New_template.setTitle(_translate("MainWindow", "Create a new template"))
        self.ImageName.setText(_translate("MainWindow", "TemplateName"))
        self.btnUpload.setText(_translate("MainWindow", "Upload Background"))
        self.labelPreview.setText(_translate("MainWindow", "Template Preview"))
        self.btnRotate.setText(_translate("MainWindow", "Rotate"))
        self.btnCrop.setText(_translate("MainWindow", "Crop"))
        self.btnSave.setText(_translate("MainWindow", "Save"))
        self.btnDelete.setText(_translate("MainWindow", "Delete"))
        self.btnUndo.setText(_translate("MainWindow", "Undo"))
        self.btnHighQuality.setText(_translate("MainWindow", "High Quality"))

class CropLabel(QtWidgets.QLabel):
    """Lớp QLabel tùy chỉnh hỗ trợ cắt ảnh và kéo văn bản trực tiếp."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.start_pos = None
        self.end_pos = None
        self.cropping = False
        self.crop_mode = False
        self.dragging_text = None  # "header" hoặc "footer"
        self.parent_window = parent
        self.scale_factor = 1.0
        self.setAcceptDrops(True)
        self.header_bbox = None  # Vùng giới hạn của header
        self.footer_bbox = None  # Vùng giới hạn của footer
        self.preview_text = None
        self.preview_pos = None

    def enter_crop_mode(self):
        self.crop_mode = True
        self.dragging_text = None
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        self.update()

    def exit_modes(self):
        self.crop_mode = False
        self.dragging_text = None
        self.cropping = False
        self.start_pos = None
        self.end_pos = None
        self.preview_text = None
        self.preview_pos = None
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.parent_window.current_image:
            if self.crop_mode:
                self.cropping = True
                self.start_pos = event.position().toPoint()
                self.end_pos = self.start_pos
                self.update()
            else:
                pos = event.position().toPoint()
                text_type = self.get_text_at_position(pos)
                if text_type:
                    self.dragging_text = text_type
                    self.start_pos = pos
                    self.end_pos = pos
                    self.preview_text = self.parent_window.ui.HeaderEdit.text() if text_type == "header" else self.parent_window.ui.FooterEdit.text()
                    self.update()
                else:
                    QtWidgets.QMessageBox.information(self.parent_window, "Info", "Click on header or footer text to drag.")

    def mouseMoveEvent(self, event):
        if self.cropping or self.dragging_text:
            self.end_pos = event.position().toPoint()
            self.preview_pos = self.end_pos
            if self.dragging_text:
                self.update_spin_boxes()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.cropping:
                self.cropping = False
                self.apply_crop()
                self.exit_modes()
            elif self.dragging_text:
                self.apply_text_position()
                self.exit_modes()
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.exit_modes()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Escape and (self.crop_mode or self.dragging_text):
            self.exit_modes()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
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
            pen = QtGui.QPen(QtGui.QColor(70, 130, 180), 3, QtCore.Qt.PenStyle.SolidLine)  # SteelBlue
            painter.setPen(pen)
            rect = QtCore.QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect)
        if self.dragging_text and self.start_pos and self.end_pos:
            painter.setOpacity(0.5)
            pen = QtGui.QPen(QtGui.QColor(70, 130, 180), 3, QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.setFont(QtGui.QFont("Arial", 12))
            if self.preview_text and self.preview_pos:
                painter.drawText(self.preview_pos, self.preview_text)
                text_rect = painter.fontMetrics().boundingRect(self.preview_text)
                rect = QtCore.QRect(
                    self.preview_pos.x(), self.preview_pos.y(),
                    text_rect.width(), text_rect.height()
                )
                painter.drawRect(rect)
            painter.setOpacity(1.0)
            painter.setPen(QtGui.QColor(255, 255, 255))
            coords = f"x: {self.end_pos.x()}, y: {self.end_pos.y()}"
            painter.drawText(self.end_pos + QtCore.QPoint(10, -10), coords)

    def wheelEvent(self, event):
        if self.parent_window.current_image:
            angle = event.angleDelta().y()
            if angle > 0:
                self.scale_factor *= 1.05
            else:
                self.scale_factor /= 1.05
            self.scale_factor = max(0.5, min(self.scale_factor, 3.0))
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

    def get_text_at_position(self, pos):
        if not self.parent_window.current_image:
            return None
        pixmap = self.pixmap()
        if not pixmap:
            return None
        pixmap_size = pixmap.size()
        image_size = self.parent_window.current_image.size
        scale_x = pixmap_size.width() / image_size[0]
        scale_y = pixmap_size.height() / image_size[1]
        x = pos.x() / scale_x
        y = pos.y() / scale_y
        if self.header_bbox and self.is_point_in_bbox(x, y, self.header_bbox):
            return "header"
        if self.footer_bbox and self.is_point_in_bbox(x, y, self.footer_bbox):
            return "footer"
        return None

    def is_point_in_bbox(self, x, y, bbox):
        left, top, right, bottom = bbox
        return left <= x <= right and top <= y <= bottom

    def update_spin_boxes(self):
        if not self.parent_window.current_image or not self.dragging_text:
            return
        pixmap = self.pixmap()
        if not pixmap:
            return
        pixmap_size = pixmap.size()
        image_size = self.parent_window.current_image.size
        scale_x = image_size[0] / pixmap_size.width()
        scale_y = image_size[1] / pixmap_size.height()
        x = int(self.end_pos.x() * scale_x)
        y = int(self.end_pos.y() * scale_y)
        x = max(0, min(x, image_size[0]))
        y = max(0, min(y, image_size[1]))
        if self.dragging_text == "header":
            self.parent_window.ui.headerXSpinBox.setValue(x)
            self.parent_window.ui.headerYSpinBox.setValue(y)
            self.parent_window.ui.tabWidget.setCurrentWidget(self.parent_window.ui.headerTab)
        elif self.dragging_text == "footer":
            self.parent_window.ui.footerXSpinBox.setValue(x)
            self.parent_window.ui.footerYSpinBox.setValue(y)
            self.parent_window.ui.tabWidget.setCurrentWidget(self.parent_window.ui.footerTab)

    def apply_text_position(self):
        if not self.parent_window.current_image or not self.dragging_text:
            return
        pixmap = self.pixmap()
        if not pixmap:
            return
        pixmap_size = pixmap.size()
        image_size = self.parent_window.current_image.size
        scale_x = image_size[0] / pixmap_size.width()
        scale_y = image_size[1] / pixmap_size.height()
        x = int(self.end_pos.x() * scale_x)
        y = int(self.end_pos.y() * scale_y)
        x = max(0, min(x, image_size[0]))
        y = max(0, min(y, image_size[1]))
        if self.dragging_text == "header":
            self.parent_window.ui.headerXSpinBox.setValue(x)
            self.parent_window.ui.headerYSpinBox.setValue(y)
            self.parent_window.apply_header()
        elif self.dragging_text == "footer":
            self.parent_window.ui.footerXSpinBox.setValue(x)
            self.parent_window.ui.footerYSpinBox.setValue(y)
            self.parent_window.apply_footer()

    def apply_crop(self):
        if not self.parent_window.current_image:
            return
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
            self.parent_window.current_image = self.parent_window.current_image.crop((left, top, right, bottom))
            self.parent_window.display_image()
            # Cập nhật lại tọa độ văn bản sau khi crop
            self.parent_window.adjust_text_positions_after_crop(left, top, right - left, bottom - top)

class MainWindow(QtWidgets.QMainWindow):
    """Lớp chính xử lý logic và sự kiện của ứng dụng PyQt6."""
    def __init__(self, on_save_callback):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.on_save_callback = on_save_callback
        self.high_quality_mode = False

        # Thay labelPreview bằng CropLabel
        self.ui.labelPreview.deleteLater()
        self.labelPreview = CropLabel(self.ui.widgetPreview)
        self.labelPreview.setObjectName("labelPreview")
        self.labelPreview.setScaledContents(False)
        self.labelPreview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelPreview.setText("Template Preview")
        self.labelPreview.setGeometry(QtCore.QRect(10, 10, 796, 380))
        self.labelPreview.parent_window = self
        self.labelPreview.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        # Khởi tạo canvas trắng
        self.current_image = Image.new('RGBA', (800, 600), (0, 0, 0, 0))
        self.original_image = self.current_image.copy()
        self.image_path = None
        self.history = deque(maxlen=10)
        self.logo_image_path = None
        self.header_color = QtGui.QColor(0, 0, 0, 255)
        self.footer_color = QtGui.QColor(0, 0, 0, 255)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

        # Hiển thị canvas ban đầu
        self.display_image()

        # Kết nối sự kiện
        self.ui.btnUpload.clicked.connect(self.upload_image)
        self.ui.btnRotate.clicked.connect(self.rotate_image)
        self.ui.btnCrop.clicked.connect(self.start_crop)
        self.ui.btnSave.clicked.connect(self.save_image)
        self.ui.btnDelete.clicked.connect(self.delete_image)
        self.ui.btnUndo.clicked.connect(self.undo)
        self.ui.listWidget.itemClicked.connect(self.switch_page)
        self.ui.btnApplyHeader.clicked.connect(self.apply_header)
        self.ui.btnApplyFooter.clicked.connect(self.apply_footer)
        self.ui.btnUploadLogo.clicked.connect(self.upload_logo)
        self.ui.btnApplyLogo.clicked.connect(self.apply_logo)
        self.ui.headerColorButton.clicked.connect(self.choose_header_color)
        self.ui.footerColorButton.clicked.connect(self.choose_footer_color)
        self.ui.btnHighQuality.clicked.connect(self.toggle_high_quality)

        # Phím tắt
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, self.rotate_image)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"), self, self.start_crop)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, self.save_image)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+D"), self, self.delete_image)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self, self.undo)

        # Điều chỉnh kích thước cửa sổ
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.resize(int(min(screen.width() * 0.9, 1200)), int(min(screen.height() * 0.9, 700)))
        self.fix_missing_icons()
        QtCore.QTimer.singleShot(0, self.debug_buttons)  # Delay debug to ensure UI is rendered

    def debug_buttons(self):
        buttons = {
            "btnUpload": self.ui.btnUpload,
            "btnRotate": self.ui.btnRotate,
            "btnCrop": self.ui.btnCrop,
            "btnSave": self.ui.btnSave,
            "btnDelete": self.ui.btnDelete,
            "btnUndo": self.ui.btnUndo,
            "btnApplyHeader": self.ui.btnApplyHeader,
            "btnApplyFooter": self.ui.btnApplyFooter,
            "btnUploadLogo": self.ui.btnUploadLogo,
            "btnApplyLogo": self.ui.btnApplyLogo,
            "headerColorButton": self.ui.headerColorButton,
            "footerColorButton": self.ui.footerColorButton,
            "btnHighQuality": self.ui.btnHighQuality,
        }
        for name, button in buttons.items():
            try:
                print(f"{name}: Visible={button.isVisible()}, Enabled={button.isEnabled()}, Geometry={button.geometry()}")
            except AttributeError:
                print(f"Error: {name} not found in UI.")

    def fix_missing_icons(self):
        icon_paths = [
            ("listWidget", "C:/Users/Admin/Downloads/IPR img/Icons/template.png"),
            ("listWidget", "C:/Users/Admin/Downloads/IPR img/Icons/edit.png"),
        ]
        for widget_name, path in icon_paths:
            if not os.path.exists(path):
                print(f"Warning: Icon not found at {path}")
                if widget_name == "listWidget":
                    for i in range(self.ui.listWidget.count()):
                        self.ui.listWidget.item(i).setIcon(QtGui.QIcon())

    def switch_page(self, item):
        index = self.ui.listWidget.row(item)
        if index == 0:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page)
            print(f"Switched to page index: {self.ui.stackedWidget.currentIndex()}")
        else:  # index == 1 (Edit)
            temp_file_path = None
            if self.current_image:
                try:
                    temp_file_path = "temp_image.png"
                    self.current_image.save(temp_file_path, quality=95)
                    print(f"Temporary image saved at: {temp_file_path}")
                except Exception as e:
                    print(f"Failed to save temporary image: {str(e)}")
            self.on_save_callback(temp_file_path)

    def upload_image(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Background Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
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
            self.original_image = Image.open(file_path).convert('RGBA')
            self.current_image = self.original_image.copy()
            self.history.clear()
            self.labelPreview.header_bbox = None
            self.labelPreview.footer_bbox = None
            print(f"Loaded image size: {self.current_image.size}")
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
            bytes_per_line = 4 * width
            q_image = QtGui.QImage(image_array.data, width, height, bytes_per_line, QtGui.QImage.Format.Format_RGBA8888)
            
            # Hỗ trợ màn hình DPI cao
            device_pixel_ratio = self.ui.widgetPreview.devicePixelRatioF()
            q_image.setDevicePixelRatio(device_pixel_ratio)
            
            pixmap = QtGui.QPixmap.fromImage(q_image)
            
            # Tính toán kích thước hiển thị
            label_size = self.labelPreview.size()
            image_size = QtCore.QSize(width, height)
            scale_factor = self.labelPreview.scale_factor
            if self.high_quality_mode:
                scale_factor *= 2  # Tăng độ phân giải gấp đôi
            
            # Tỷ lệ hiển thị tối ưu
            scaled_size = image_size * scale_factor * device_pixel_ratio
            scaled_size = scaled_size.boundedTo(label_size * device_pixel_ratio)
            scaled_size = scaled_size.expandedTo(QtCore.QSize(1, 1))
            
            scaled_pixmap = pixmap.scaled(
                scaled_size,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            self.labelPreview.setPixmap(scaled_pixmap)
            print(f"Displayed image: Original={image_size}, Scaled={scaled_pixmap.size()}, ScaleFactor={scale_factor}, DPR={device_pixel_ratio}")
        else:
            self.labelPreview.clear()
            self.labelPreview.setText("Template Preview")

    def toggle_high_quality(self):
        self.high_quality_mode = not self.high_quality_mode
        self.ui.btnHighQuality.setText("High Quality" if not self.high_quality_mode else "Normal Quality")
        print(f"High quality mode: {self.high_quality_mode}")
        self.display_image()

    def rotate_image(self):
        if self.current_image:
            self.history.append(self.current_image.copy())
            self.current_image = self.current_image.rotate(-90, expand=True)
            self.labelPreview.header_bbox = None
            self.labelPreview.footer_bbox = None
            self.display_image()

    def start_crop(self):
        if self.current_image:
            self.labelPreview.enter_crop_mode()

    def upload_logo(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Logo Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.logo_image_path = file_path
            print(f"Logo image selected: {file_path}")

    def choose_header_color(self):
        color = QtWidgets.QColorDialog.getColor(self.header_color, self, "Choose Header Color")
        if color.isValid():
            self.header_color = color
            self.ui.headerColorButton.setStyleSheet(f"""
                QPushButton {{ 
                    background-color: {color.name()}; 
                    color: white; 
                    border-radius: 5px; 
                    padding: 8px; 
                }}
                QPushButton:hover {{ 
                    background-color: {color.lighter(110).name()}; 
                }}""")

    def choose_footer_color(self):
        color = QtWidgets.QColorDialog.getColor(self.footer_color, self, "Choose Footer Color")
        if color.isValid():
            self.footer_color = color
            self.ui.footerColorButton.setStyleSheet(f"""
                QPushButton {{ 
                    background-color: {color.name()}; 
                    color: white; 
                    border-radius: 5px; 
                    padding: 8px; 
                }}
                QPushButton:hover {{ 
                    background-color: {color.lighter(110).name()}; 
                }}""")

    def apply_header(self):
        if not self.ui.HeaderEdit.text():
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter header text.")
            return
        self.history.append(self.current_image.copy())
        draw_image = self.current_image.copy()
        width, height = draw_image.size
        draw = ImageDraw.Draw(draw_image)
        font_name = self.ui.headerFontCombo.currentText().lower().replace(" ", "")
        try:
            font = ImageFont.truetype(f"{font_name}.ttf", self.ui.headerSizeSpinBox.value())
        except:
            font = ImageFont.load_default().font_variant(size=self.ui.headerSizeSpinBox.value())
        text = self.ui.HeaderEdit.text()
        x = self.ui.headerXSpinBox.value()
        y = self.ui.headerYSpinBox.value()
        if x < 0 or x > width or y < 0 or y > height:
            QtWidgets.QMessageBox.warning(self, "Warning", "Position out of canvas bounds.")
            return
        color = (self.header_color.red(), self.header_color.green(), self.header_color.blue(), self.header_color.alpha())
        draw.text((x, y), text, fill=color, font=font)
        # Lưu vùng giới hạn của header
        text_bbox = draw.textbbox((x, y), text, font=font)
        self.labelPreview.header_bbox = text_bbox
        self.current_image = draw_image
        self.display_image()

    def apply_footer(self):
        if not self.ui.FooterEdit.text():
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter footer text.")
            return
        self.history.append(self.current_image.copy())
        draw_image = self.current_image.copy()
        width, height = draw_image.size
        draw = ImageDraw.Draw(draw_image)
        font_name = self.ui.footerFontCombo.currentText().lower().replace(" ", "")
        try:
            font = ImageFont.truetype(f"{font_name}.ttf", self.ui.footerSizeSpinBox.value())
        except:
            font = ImageFont.load_default().font_variant(size=self.ui.footerSizeSpinBox.value())
        text = self.ui.FooterEdit.text()
        x = self.ui.footerXSpinBox.value()
        y = self.ui.footerYSpinBox.value()
        if x < 0 or x > width or y < 0 or y > height:
            QtWidgets.QMessageBox.warning(self, "Warning", "Position out of canvas bounds.")
            return
        color = (self.footer_color.red(), self.footer_color.green(), self.footer_color.blue(), self.footer_color.alpha())
        draw.text((x, y), text, fill=color, font=font)
        # Lưu vùng giới hạn của footer
        text_bbox = draw.textbbox((x, y), text, font=font)
        self.labelPreview.footer_bbox = text_bbox
        self.current_image = draw_image
        self.display_image()

    def adjust_text_positions_after_crop(self, left, top, new_width, new_height):
        """Điều chỉnh tọa độ văn bản sau khi crop."""
        if self.labelPreview.header_bbox:
            x = self.ui.headerXSpinBox.value() - left
            y = self.ui.headerYSpinBox.value() - top
            x = max(0, min(x, new_width))
            y = max(0, min(y, new_height))
            self.ui.headerXSpinBox.setValue(x)
            self.ui.headerYSpinBox.setValue(y)
            self.apply_header()
        if self.labelPreview.footer_bbox:
            x = self.ui.footerXSpinBox.value() - left
            y = self.ui.footerYSpinBox.value() - top
            x = max(0, min(x, new_width))
            y = max(0, min(y, new_height))
            self.ui.footerXSpinBox.setValue(x)
            self.ui.footerYSpinBox.setValue(y)
            self.apply_footer()

    def apply_logo(self):
        if not self.logo_image_path:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please upload a logo image.")
            return
        self.history.append(self.current_image.copy())
        draw_image = self.current_image.copy()
        width, height = draw_image.size
        try:
            logo_img = Image.open(self.logo_image_path).convert('RGBA')
            logo_img = logo_img.resize((min(100, logo_img.width), min(100, logo_img.height)), Image.Resampling.LANCZOS)
            x = self.ui.logoXSpinBox.value()
            y = self.ui.logoYSpinBox.value()
            if x < 0 or x + logo_img.width > width or y < 0 or y + logo_img.height > height:
                QtWidgets.QMessageBox.warning(self, "Warning", "Logo position out of canvas bounds.")
                return
            draw_image.paste(logo_img, (x, y), logo_img)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to apply logo image: {str(e)}")
            return
        self.current_image = draw_image
        self.display_image()

    def save_image(self):
        if self.current_image:
            file_dialog = QtWidgets.QFileDialog(self)
            file_path, _ = file_dialog.getSaveFileName(
                self, "Save Template", self.ui.ImageName.text() or "template.png", "PNG Images (*.png);;JPEG Images (*.jpg *.jpeg)"
            )
            if file_path:
                try:
                    progress = QtWidgets.QProgressDialog("Saving template...", "Cancel", 0, 100, self)
                    progress.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
                    progress.setAutoClose(True)
                    progress.show()
                    QtCore.QCoreApplication.processEvents()
                    if file_path.lower().endswith('.png'):
                        self.current_image.save(file_path, format='PNG')
                    else:
                        self.current_image.convert('RGB').save(file_path, format='JPEG', quality=95)
                    progress.setValue(50)
                    footer_text = self.ui.FooterEdit.text()
                    if footer_text:
                        footer_file_path = os.path.splitext(file_path)[0] + "_footer.txt"
                        with open(footer_file_path, "w", encoding="utf-8") as f:
                            f.write(footer_text)
                        print(f"Footer saved at: {footer_file_path}")
                    progress.setValue(100)
                    QtWidgets.QMessageBox.information(self, "Success", "Template saved successfully!")
                except Exception as e:
                    progress.cancel()
                    QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")

    def delete_image(self):
        self.current_image = Image.new('RGBA', (800, 600), (0, 0, 0, 0))
        self.original_image = self.current_image.copy()
        self.image_path = None
        self.logo_image_path = None
        self.header_color = QtGui.QColor(0, 0, 0, 255)
        self.footer_color = QtGui.QColor(0, 0, 0, 255)
        self.history.clear()
        self.labelPreview.clear()
        self.labelPreview.setText("Template Preview")
        self.ui.ImageName.setText("TemplateName")
        self.ui.HeaderEdit.setText("")
        self.ui.FooterEdit.setText("")
        self.ui.headerXSpinBox.setValue(0)
        self.ui.headerYSpinBox.setValue(120)
        self.ui.footerXSpinBox.setValue(0)
        self.ui.footerYSpinBox.setValue(550)
        self.ui.logoXSpinBox.setValue(10)
        self.ui.logoYSpinBox.setValue(10)
        self.ui.headerFontCombo.setCurrentIndex(0)
        self.ui.footerFontCombo.setCurrentIndex(0)
        self.ui.headerSizeSpinBox.setValue(36)
        self.ui.footerSizeSpinBox.setValue(36)
        self.ui.headerColorButton.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.ui.footerColorButton.setStyleSheet("""
            QPushButton { 
                background-color: #4682B4; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: #5A9BD4; 
            }""")
        self.labelPreview.scale_factor = 1.0
        self.labelPreview.header_bbox = None
        self.labelPreview.footer_bbox = None
        self.labelPreview.exit_modes()
        self.display_image()

    def undo(self):
        if self.history:
            self.current_image = self.history.pop()
            self.labelPreview.header_bbox = None
            self.labelPreview.footer_bbox = None
            self.display_image()
            # Cập nhật lại vùng giới hạn nếu cần
            if self.ui.HeaderEdit.text():
                self.apply_header()
            if self.ui.FooterEdit.text():
                self.apply_footer()
        else:
            QtWidgets.QMessageBox.information(self, "Undo", "No actions to undo.")

    def resizeEvent(self, event):
        window_size = self.centralWidget().size()
        window_width = window_size.width()
        window_height = window_size.height()
        header_height = 80
        sidebar_width = 150
        content_width = window_width - sidebar_width
        self.ui.frame.setGeometry(QtCore.QRect(0, 0, sidebar_width, header_height))
        self.ui.frame_2.setGeometry(QtCore.QRect(sidebar_width, 0, content_width, header_height))
        self.ui.header_label.setGeometry(QtCore.QRect(0, 0, content_width, header_height))
        content_height = window_height - header_height
        self.ui.listWidget.setGeometry(QtCore.QRect(0, header_height, sidebar_width, content_height))
        self.ui.scrollArea.setGeometry(QtCore.QRect(sidebar_width, header_height, content_width, content_height))
        self.ui.stackedWidget.setMinimumSize(content_width, content_height)
        self.ui.New_template.setGeometry(QtCore.QRect(7, 0, content_width - 20, content_height - 10))
        self.ui.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, content_width - 40, 80))
        preview_width = content_width - 240
        preview_height = content_height - 200
        self.ui.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 110, preview_width, preview_height))
        self.ui.sidebarWidget.setGeometry(QtCore.QRect(content_width - 230, 110, 200, content_height - 200))
        self.ui.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, content_height - 100, content_width - 40, 50))
        self.labelPreview.setGeometry(QtCore.QRect(10, 10, preview_width - 20, preview_height - 20))
        if self.current_image:
            self.display_image()
        super().resizeEvent(event)

def run_tkinter(saved_image_path=None):
    """Khởi động giao diện Tkinter."""
    root = tk.Tk()
    logic = CanvasEditorLogic(None)
    ui = EditorApp(root, logic)
    logic.ui = ui
    if saved_image_path:
        try:
            logic.load_image(saved_image_path)
        except AttributeError:
            print(f"Warning: CanvasEditorLogic does not have load_image method. Saved image path: {saved_image_path}")
    root.mainloop()

def run_pyqt():
    """Khởi động ứng dụng PyQt6 và xử lý chuyển đổi sang Tkinter khi nhấn Edit."""
    os.environ["QT_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    def on_save_callback(file_path):
        window.close()
        app.quit()
        run_tkinter(file_path)
    
    window = MainWindow(on_save_callback)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_pyqt()

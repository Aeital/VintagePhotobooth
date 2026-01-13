from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog,
    QButtonGroup, QRadioButton
)
from PyQt6.QtGui import QFont, QPixmap, QImage, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer
import cv2
import sys
import os
import numpy as np

# ---------------------- DownloadSuccessWindow ----------------------

class DownloadSuccessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download Complete")
        self.setFixedSize(420, 420)
        self.setStyleSheet("background-color: #FFFDD0;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        success_label = QLabel("Downloaded successfully")
        success_label.setFont(QFont("Georgia", 18, QFont.Weight.DemiBold))
        success_label.setStyleSheet("color: #723A03;")
        success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(success_label)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #723A03;
                color: #FFFDD0;
                padding: 10px 24px;
                border: none;
                border-radius: 12px;
                font-family: 'Georgia';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8B5E3C;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

# ---------------------- FilterWindow ----------------------

class FilterWindow(QWidget):
    def __init__(self, images):
        super().__init__()
        self.setWindowTitle("Choose Filter")
        self.setFixedSize(420, 420)
        self.setStyleSheet("background-color: #FFFDD0;")
        self.images = images
        self.selected_filter = "sepia"
        self.strip_color = "#723A03"
        self.bg_color = "#FFFDD0"
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        heading = QLabel("Choose your filter")
        heading.setFont(QFont("Segoe Script", 16))
        heading.setStyleSheet("color: #723A03;")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(heading)

        # Filter choices
        filters = ["sepia", "bw", "warm", "yellow"]
        filter_layout = QHBoxLayout()
        self.filter_buttons = QButtonGroup()

        for f in filters:
            btn = QRadioButton(f.upper())
            btn.setFont(QFont("Georgia", 10))
            if f == "sepia":
                btn.setChecked(True)
            self.filter_buttons.addButton(btn)
            filter_layout.addWidget(btn)

        layout.addLayout(filter_layout)

        # Strip color
        strip_label = QLabel("Strip color")
        strip_label.setFont(QFont("Segoe Script", 14))
        strip_label.setStyleSheet("color: #723A03;")
        strip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(strip_label)

        strip_colors = ["#723A03", "#F5DEB3", "#A0522D", "#8B4513"]
        self.strip_color_buttons = QButtonGroup()
        strip_layout = QHBoxLayout()
        for i, color in enumerate(strip_colors):
            radio = QRadioButton()
            if i == 0:  # First one selected by default
                radio.setStyleSheet(f"""
                    QRadioButton::indicator {{
                        width: 20px;
                        height: 20px;
                        border-radius: 10px;
                        background-color: {color};
                        border: 3px solid #8B5E3C;
                    }}
                """)
                radio.setChecked(True)
            else:
                radio.setStyleSheet(f"""
                    QRadioButton::indicator {{
                        width: 20px;
                        height: 20px;
                        border-radius: 10px;
                        background-color: {color};
                    }}
                """)
            radio.toggled.connect(lambda checked, idx=i: self.update_strip_selection(idx, checked))
            self.strip_color_buttons.addButton(radio)
            strip_layout.addWidget(radio)
        layout.addLayout(strip_layout)

        # Background color
        bg_label = QLabel("Background color")
        bg_label.setFont(QFont("Segoe Script", 14))
        bg_label.setStyleSheet("color: #723A03;")
        bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(bg_label)

        bg_colors = ["#FFFDD0", "#F0E68C", "#FFDAB9", "#FFE4B5"]
        self.bg_color_buttons = QButtonGroup()
        bg_layout = QHBoxLayout()
        for i, color in enumerate(bg_colors):
            radio = QRadioButton()
            if i == 0:  # First one selected by default
                radio.setStyleSheet(f"""
                    QRadioButton::indicator {{
                        width: 20px;
                        height: 20px;
                        border-radius: 10px;
                        background-color: {color};
                        border: 3px solid #8B5E3C;
                    }}
                """)
                radio.setChecked(True)
            else:
                radio.setStyleSheet(f"""
                    QRadioButton::indicator {{
                        width: 20px;
                        height: 20px;
                        border-radius: 10px;
                        background-color: {color};
                    }}
                """)
            radio.toggled.connect(lambda checked, idx=i: self.update_bg_selection(idx, checked))
            self.bg_color_buttons.addButton(radio)
            bg_layout.addWidget(radio)
        layout.addLayout(bg_layout)

        # Next button
        next_button = QPushButton("Next")
        next_button.setStyleSheet("""
            QPushButton {
                background-color: #723A03;
                color: #FFFDD0;
                padding: 10px 24px;
                border: none;
                border-radius: 12px;
                font-family: 'Georgia';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8B5E3C;
            }
        """)
        next_button.clicked.connect(self.go_to_final)
        layout.addWidget(next_button)

        self.setLayout(layout)

    def update_strip_selection(self, idx, checked):
        if checked:
            strip_colors = ["#723A03", "#F5DEB3", "#A0522D", "#8B4513"]
            # Update all buttons
            for i, button in enumerate(self.strip_color_buttons.buttons()):
                color = strip_colors[i]
                if i == idx:
                    button.setStyleSheet(f"""
                        QRadioButton::indicator {{
                            width: 20px;
                            height: 20px;
                            border-radius: 10px;
                            background-color: {color};
                            border: 3px solid #8B5E3C;
                        }}
                    """)
                else:
                    button.setStyleSheet(f"""
                        QRadioButton::indicator {{
                            width: 20px;
                            height: 20px;
                            border-radius: 10px;
                            background-color: {color};
                        }}
                    """)

    def update_bg_selection(self, idx, checked):
        if checked:
            bg_colors = ["#FFFDD0", "#F0E68C", "#FFDAB9", "#FFE4B5"]
            # Update all buttons
            for i, button in enumerate(self.bg_color_buttons.buttons()):
                color = bg_colors[i]
                if i == idx:
                    button.setStyleSheet(f"""
                        QRadioButton::indicator {{
                            width: 20px;
                            height: 20px;
                            border-radius: 10px;
                            background-color: {color};
                            border: 3px solid #8B5E3C;
                        }}
                    """)
                else:
                    button.setStyleSheet(f"""
                        QRadioButton::indicator {{
                            width: 20px;
                            height: 20px;
                            border-radius: 10px;
                            background-color: {color};
                        }}
                    """)

    def go_to_final(self):
        self.selected_filter = self.filter_buttons.checkedButton().text().lower()
        strip_idx = self.strip_color_buttons.checkedId()
        bg_idx = self.bg_color_buttons.checkedId()
        self.strip_color = ["#723A03", "#F5DEB3", "#A0522D", "#8B4513"][strip_idx]
        self.bg_color = ["#FFFDD0", "#F0E68C", "#FFDAB9", "#FFE4B5"][bg_idx]
        self.final_window = FinalDisplayWindow(self.images, self.selected_filter, self.strip_color, self.bg_color)
        self.final_window.show()
        self.close()

# ---------------------- FinalDisplayWindow ----------------------

class FinalDisplayWindow(QWidget):
    def __init__(self, images, selected_filter, strip_color, bg_color):
        super().__init__()
        self.setWindowTitle("Final Strip")
        self.setFixedSize(420, 420)
        self.images = images
        self.strip_color = strip_color
        self.bg_color = bg_color
        self.selected_filter = selected_filter
        self.setStyleSheet(f"background-color: {self.bg_color};")
        self.initUI()

    def apply_sepia_filter(self, pixmap):
        """Apply sepia filter to pixmap"""
        image = pixmap.toImage()
        width, height = image.width(), image.height()
        
        for x in range(width):
            for y in range(height):
                pixel = image.pixel(x, y)
                r, g, b = (pixel >> 16) & 255, (pixel >> 8) & 255, pixel & 255
                
                # Sepia formula
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                
                # Clamp values
                tr = min(255, tr)
                tg = min(255, tg)
                tb = min(255, tb)
                
                new_pixel = (255 << 24) | (tr << 16) | (tg << 8) | tb
                image.setPixel(x, y, new_pixel)
        
        return QPixmap.fromImage(image)

    def apply_bw_filter(self, pixmap):
        """Apply black and white filter to pixmap"""
        image = pixmap.toImage()
        width, height = image.width(), image.height()
        
        for x in range(width):
            for y in range(height):
                pixel = image.pixel(x, y)
                r, g, b = (pixel >> 16) & 255, (pixel >> 8) & 255, pixel & 255
                
                # Grayscale formula
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                new_pixel = (255 << 24) | (gray << 16) | (gray << 8) | gray
                image.setPixel(x, y, new_pixel)
        
        return QPixmap.fromImage(image)

    def apply_warm_filter(self, pixmap):
        """Apply warm filter to pixmap"""
        image = pixmap.toImage()
        width, height = image.width(), image.height()
        
        for x in range(width):
            for y in range(height):
                pixel = image.pixel(x, y)
                r, g, b = (pixel >> 16) & 255, (pixel >> 8) & 255, pixel & 255
                
                # Warm filter - increase red and reduce blue
                r = min(255, int(r * 1.2))
                g = min(255, int(g * 1.1))
                b = int(b * 0.8)
                
                new_pixel = (255 << 24) | (r << 16) | (g << 8) | b
                image.setPixel(x, y, new_pixel)
        
        return QPixmap.fromImage(image)

    def apply_yellow_filter(self, pixmap):
        """Apply yellow filter to pixmap"""
        image = pixmap.toImage()
        width, height = image.width(), image.height()
        
        for x in range(width):
            for y in range(height):
                pixel = image.pixel(x, y)
                r, g, b = (pixel >> 16) & 255, (pixel >> 8) & 255, pixel & 255
                
                # Yellow filter - increase red and green, reduce blue
                r = min(255, int(r * 1.15))
                g = min(255, int(g * 1.15))
                b = int(b * 0.7)
                
                new_pixel = (255 << 24) | (r << 16) | (g << 8) | b
                image.setPixel(x, y, new_pixel)
        
        return QPixmap.fromImage(image)

    def apply_filter(self, pixmap):
        """Apply the selected filter to the pixmap"""
        if self.selected_filter == "sepia":
            return self.apply_sepia_filter(pixmap)
        elif self.selected_filter == "bw":
            return self.apply_bw_filter(pixmap)
        elif self.selected_filter == "warm":
            return self.apply_warm_filter(pixmap)
        elif self.selected_filter == "yellow":
            return self.apply_yellow_filter(pixmap)
        else:
            return pixmap

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for pixmap in self.images:
            img_label = QLabel()
            img_label.setFixedSize(200, 100)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_label.setStyleSheet(f"""
                background-color: {self.strip_color};
                border-radius: 20px;
                padding: 5px;
            """)
            # Apply filter before scaling
            filtered_pixmap = self.apply_filter(pixmap)
            img_label.setPixmap(filtered_pixmap.scaled(190, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            layout.addWidget(img_label)

        save_button = QPushButton("Download")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #723A03;
                color: #FFFDD0;
                padding: 10px 24px;
                border: none;
                border-radius: 12px;
                font-family: 'Georgia';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8B5E3C;
            }
        """)
        save_button.clicked.connect(self.save_image)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_image(self):
        strip_image = QImage(220, 330, QImage.Format.Format_RGB32)
        strip_image.fill(QColor(self.bg_color))
        painter = QPainter(strip_image)
        y = 10
        for pixmap in self.images:
            painter.setBrush(QColor(self.strip_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(10, y, 200, 100, 20, 20)
            # Apply filter before saving
            filtered_pixmap = self.apply_filter(pixmap)
            scaled = filtered_pixmap.scaled(190, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(15, y + 5, scaled)
            y += 110
        painter.end()

        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        path = os.path.join(downloads, "photostrip.png")
        strip_image.save(path)
        
        # Show success window
        self.success_window = DownloadSuccessWindow()
        self.success_window.show()

# ---------------------- UploadWindow ----------------------

class UploadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Upload Pictures")
        self.setFixedSize(420, 420)
        self.setStyleSheet("background-color: #FFFDD0;")
        self.initUI()

    def initUI(self):
        self.image_labels = []
        self.pixmaps = []
        images_layout = QHBoxLayout()
        images_layout.setSpacing(10)
        images_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for _ in range(3):
            label = QLabel()
            label.setFixedSize(100, 100)
            label.setStyleSheet("""
                background-color: #D3D3D3;
                border: 4px solid #723A03;
                border-radius: 20px;
            """)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.mousePressEvent = self.upload_image_event(label)
            self.image_labels.append(label)
            images_layout.addWidget(label)

        next_button = QPushButton("Next")
        next_button.setStyleSheet("""
            QPushButton {
                background-color: #723A03;
                color: #FFFDD0;
                padding: 10px 24px;
                border: none;
                border-radius: 12px;
                font-family: 'Georgia';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8B5E3C;
            }
        """)
        next_button.clicked.connect(self.open_filter_window)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(images_layout)
        layout.addSpacing(30)
        layout.addWidget(next_button)
        self.setLayout(layout)

    def upload_image_event(self, label):
        def handler(event):
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
            if file_path:
                pixmap = QPixmap(file_path).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(pixmap)
                self.pixmaps.append(QPixmap(file_path))
        return handler

    def open_filter_window(self):
        if len(self.pixmaps) >= 3:
            self.filter_window = FilterWindow(self.pixmaps[:3])
            self.filter_window.show()
            self.close()

# ---------------------- CameraWindow ----------------------

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera View")
        self.setFixedSize(420, 420)
        self.setStyleSheet("background-color: #FFFDD0;")
        self.image_count = 0
        self.captured_images = []
        self.countdown_active = False
        self.countdown_value = 3

        self.camera_frame = QLabel()
        self.camera_frame.setFixedSize(400, 400)
        self.camera_frame.setStyleSheet("""
            background-color: #D3D3D3;
            border: 6px solid #723A03;
            border-radius: 24px;
        """)
        self.camera_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Countdown label
        self.countdown_label = QLabel()
        self.countdown_label.setFixedSize(400, 400)
        self.countdown_label.setStyleSheet("""
            background-color: transparent;
            color: #723A03;
            font-size: 120px;
            font-weight: bold;
            font-family: 'Georgia';
        """)
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.hide()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.camera_frame)
        self.setLayout(layout)

        # Position countdown label on top of camera frame
        self.countdown_label.setParent(self.camera_frame)
        self.countdown_label.move(0, 0)

        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Countdown timer
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

        self.camera_frame.mousePressEvent = self.start_countdown

    def update_frame(self):
        if self.capture.isOpened() and not self.countdown_active:
            ret, frame = self.capture.read()
            if ret:
                self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = self.current_frame.shape
                bytes_per_line = ch * w
                image = QImage(self.current_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.camera_frame.setPixmap(QPixmap.fromImage(image))

    def start_countdown(self, event):
        if self.image_count < 3 and not self.countdown_active:
            self.countdown_active = True
            self.countdown_value = 3
            self.countdown_label.show()
            self.countdown_label.setText(str(self.countdown_value))
            self.countdown_timer.start(1000)  # 1 second intervals

    def update_countdown(self):
        self.countdown_value -= 1
        if self.countdown_value > 0:
            self.countdown_label.setText(str(self.countdown_value))
        else:
            self.countdown_timer.stop()
            self.countdown_label.hide()
            self.capture_image()
            self.countdown_active = False

    def capture_image(self):
        if hasattr(self, 'current_frame') and self.image_count < 3:
            image = QImage(self.current_frame.data, self.current_frame.shape[1], self.current_frame.shape[0], self.current_frame.shape[1]*3, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.captured_images.append(pixmap)
            self.image_count += 1
            
        if self.image_count == 3:
            self.filter_window = FilterWindow(self.captured_images)
            self.filter_window.show()
            self.close()

    def closeEvent(self, event):
        if self.capture:
            self.capture.release()
        event.accept()

# ---------------------- Main ----------------------

class VintagePhotobooth(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vintage Photobooth")
        self.setFixedSize(420, 420)
        self.setStyleSheet("background-color: #FFFDD0; border-radius: 20px;")
        self.initUI()

    def initUI(self):
        title = QLabel("Vintage Photobooth")
        title.setFont(QFont("Georgia", 20, QFont.Weight.DemiBold))
        title.setStyleSheet("color: #723A03;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Take your photo!")
        subtitle.setFont(QFont("Segoe Script", 16))
        subtitle.setStyleSheet("color: #723A03;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        camera_btn = QPushButton("Use Camera")
        upload_btn = QPushButton("Upload Picture")

        button_style = """
            QPushButton {
                background-color: #723A03;
                color: #FFFDD0;
                padding: 10px 24px;
                border: none;
                border-radius: 12px;
                font-family: 'Georgia';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8B5E3C;
            }
        """
        camera_btn.setStyleSheet(button_style)
        upload_btn.setStyleSheet(button_style)

        camera_btn.clicked.connect(self.open_camera_window)
        upload_btn.clicked.connect(self.open_upload_window)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(camera_btn)
        btn_layout.addWidget(upload_btn)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(btn_layout)
        layout.setContentsMargins(20, 10, 20, 20)
        layout.setSpacing(5)
        self.setLayout(layout)

    def open_camera_window(self):
        self.cam_window = CameraWindow()
        self.cam_window.show()

    def open_upload_window(self):
        self.upload_window = UploadWindow()
        self.upload_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VintagePhotobooth()
    window.show()
    sys.exit(app.exec())
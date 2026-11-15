import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QFont
from modules.monitor import get_system_stats

class AeroNotch(QWidget):
    def __init__(self):
        super().__init__()
        self.is_expanded = False
        self.collapsed_w, self.collapsed_h = 220, 36
        self.expanded_w, self.expanded_h = 380, 140
        
        self.init_ui()
        self.init_timers()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background-color: #0D0D0D;
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.18);
            }
            QLabel {
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 10px;
                padding: 4px 10px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
            }
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                height: 6px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #38BDF8;
                border-radius: 4px;
            }
        """)

        # Верхняя панель (видна всегда)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(14, 0, 14, 0)
        
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        
        self.status_label = QLabel("AeroNotch")
        self.status_label.setStyleSheet("color: #A1A1AA; font-size: 11px;")
        
        self.cpu_mini_label = QLabel("CPU 0%")
        self.cpu_mini_label.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: bold;")

        top_layout.addWidget(self.time_label)
        top_layout.addStretch()
        top_layout.addWidget(self.status_label)
        top_layout.addStretch()
        top_layout.addWidget(self.cpu_mini_label)

        # Нижняя панель (видна при раскрытии)
        self.expanded_widget = QWidget()
        exp_layout = QVBoxLayout(self.expanded_widget)
        exp_layout.setContentsMargins(14, 4, 14, 10)
        exp_layout.setSpacing(8)

        # Датчики
        stats_layout = QHBoxLayout()
        self.cpu_bar = QProgressBar()
        self.ram_bar = QProgressBar()
        stats_layout.addWidget(QLabel("CPU:"))
        stats_layout.addWidget(self.cpu_bar)
        stats_layout.addWidget(QLabel("RAM:"))
        stats_layout.addWidget(self.ram_bar)
        exp_layout.addLayout(stats_layout)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.close_btn = QPushButton("Закрыть ✕")
        self.close_btn.clicked.connect(QApplication.quit)
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)
        exp_layout.addLayout(btn_layout)

        self.expanded_widget.hide()

        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(0, 6, 0, 6)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.expanded_widget)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(280)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.update_position(self.collapsed_w, self.collapsed_h, animate=False)

    def init_timers(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
        self.update_data()

    def update_data(self):
        now = datetime.now().strftime("%H:%M")
        self.time_label.setText(now)
        cpu, ram = get_system_stats()
        self.cpu_mini_label.setText(f"CPU {cpu}%")
        self.cpu_bar.setValue(cpu)
        self.ram_bar.setValue(ram)

    def update_position(self, w, h, animate=True):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - w) // 2
        y = 8
        target_rect = QRect(x, y, w, h)
        self.container.setGeometry(0, 0, w, h)

        if animate:
            self.anim.stop()
            self.anim.setStartValue(self.geometry())
            self.anim.setEndValue(target_rect)
            self.anim.start()
        else:
            self.setGeometry(target_rect)

    def enterEvent(self, event):
        if not self.is_expanded:
            self.is_expanded = True
            self.expanded_widget.show()
            self.update_position(self.expanded_w, self.expanded_h)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.is_expanded:
            self.is_expanded = False
            self.expanded_widget.hide()
            self.update_position(self.collapsed_w, self.collapsed_h)
        super().leaveEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notch = AeroNotch()
    notch.show()
    sys.exit(app.exec())

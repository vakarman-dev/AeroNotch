cat << 'EOF' > test_termux.py
import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont
import psutil

class AeroNotch(QWidget):
    def __init__(self):
        super().__init__()
        self.is_expanded = False
        self.collapsed_w, self.collapsed_h = 220, 36
        self.expanded_w, self.expanded_h = 380, 140
        self.init_ui()
        self.init_timers()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background-color: #0D0D0D;
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
            QLabel { color: #FFFFFF; font-family: sans-serif; }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white; border-radius: 10px; padding: 4px 10px;
            }
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px; height: 6px;
            }
            QProgressBar::chunk { background-color: #38BDF8; border-radius: 4px; }
        """)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(14, 0, 14, 0)
        self.time_label = QLabel("00:00")
        self.status_label = QLabel("AeroNotch")
        self.cpu_mini_label = QLabel("CPU 0%")

        top_layout.addWidget(self.time_label)
        top_layout.addStretch()
        top_layout.addWidget(self.status_label)
        top_layout.addStretch()
        top_layout.addWidget(self.cpu_mini_label)

        self.expanded_widget = QWidget()
        exp_layout = QVBoxLayout(self.expanded_widget)
        stats_layout = QHBoxLayout()
        self.cpu_bar = QProgressBar()
        self.ram_bar = QProgressBar()
        stats_layout.addWidget(QLabel("CPU:"))
        stats_layout.addWidget(self.cpu_bar)
        stats_layout.addWidget(QLabel("RAM:"))
        stats_layout.addWidget(self.ram_bar)
        exp_layout.addLayout(stats_layout)

        self.close_btn = QPushButton("Закрыть")
        self.close_btn.clicked.connect(QApplication.quit)
        exp_layout.addWidget(self.close_btn, alignment=Qt.AlignRight)
        self.expanded_widget.hide()

        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(0, 6, 0, 6)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.expanded_widget)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.update_position(self.collapsed_w, self.collapsed_h, animate=False)

    def init_timers(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
        self.update_data()

    def update_data(self):
        self.time_label.setText(datetime.now().strftime("%H:%M"))
        cpu = int(psutil.cpu_percent())
        ram = int(psutil.virtual_memory().percent)
        self.cpu_mini_label.setText(f"CPU {cpu}%")
        self.cpu_bar.setValue(cpu)
        self.ram_bar.setValue(ram)

    def update_position(self, w, h, animate=True):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - w) // 2
        target_rect = QRect(x, 8, w, h)
        self.container.setGeometry(0, 0, w, h)
        if animate:
            self.anim.stop()
            self.anim.setStartValue(self.geometry())
            self.anim.setEndValue(target_rect)
            self.anim.start()
        else:
            self.setGeometry(target_rect)

    def mousePressEvent(self, event):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.expanded_widget.show()
            self.update_position(self.expanded_w, self.expanded_h)
        else:
            self.expanded_widget.hide()
            self.update_position(self.collapsed_w, self.collapsed_h)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notch = AeroNotch()
    notch.show()
    sys.exit(app.exec_())
EOF

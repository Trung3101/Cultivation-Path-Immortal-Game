# gm_launcher.py
import time
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QInputDialog, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt


class GMLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎮 GM Master – Quản lý vật phẩm")
        self.setMinimumSize(800, 600)

        # Placeholder ban đầu – có thể sửa thành dashboard GM nếu muốn
        self.placeholder = QLabel("🔧 Chào mừng Master! Hãy sử dụng công cụ bên dưới.")
        self.placeholder.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.placeholder)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.failed_attempts = 0
        self.locked_until = None

        # Khi khởi tạo là đã xác thực rồi (từ giftcode), nên ta vào luôn
        self.launch_gm_tools()

    def launch_gm_tools(self):
        from ui.item_table import ItemTable
        self.item_table = ItemTable(enable_shortcut=False)
        self.setCentralWidget(self.item_table)
        self.item_table.enable_admin_controls()

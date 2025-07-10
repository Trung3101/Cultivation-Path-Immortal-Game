# ui/entry_menu.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from ui.main_menu import MainMenu
from ui.load_character import LoadCharacterMenu

class EntryMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌌 Đạo Đồ – Khởi đầu")

        layout = QVBoxLayout()

        self.btn_new = QPushButton("🌱 Tạo nhân vật mới")
        self.btn_load = QPushButton("🔄 Chơi lại nhân vật cũ")

        self.btn_new.clicked.connect(self.create_new)
        self.btn_load.clicked.connect(self.load_existing)

        layout.addWidget(self.btn_new)
        layout.addWidget(self.btn_load)

        self.setLayout(layout)

    def create_new(self):
        self.menu = MainMenu()
        self.menu.show()
        self.close()

    def load_existing(self):
        self.load_menu = LoadCharacterMenu()
        self.load_menu.show()
        self.close()

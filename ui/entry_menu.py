# ui/entry_menu.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QPushButton
from ui.item_form import ItemForm
from ui.main_menu import MainMenu
from ui.load_character import LoadCharacterMenu
from ui.item_viewer import ItemViewer

class EntryMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌌 Đạo Đồ – Khởi đầu")

        layout = QVBoxLayout()

        self.btn_new = QPushButton("🌱 Tạo nhân vật mới")
        self.btn_load = QPushButton("🔄 Chơi lại nhân vật cũ")

        self.btn_new.clicked.connect(self.create_new)
        self.btn_load.clicked.connect(self.load_existing)

        self.item_button = QPushButton("🧾 Nhập vật phẩm")
        self.item_button.clicked.connect(self.open_item_form)
        layout.addWidget(self.item_button)

        self.viewer_button = QPushButton("📜 Xem vật phẩm đã nhập")
        self.viewer_button.clicked.connect(self.open_item_viewer)
        layout.addWidget(self.viewer_button)

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

    def open_item_form(self):
        self.item_window = ItemForm()
        self.item_window.show()

    def open_item_viewer(self):
        self.viewer_window = ItemViewer()
        self.viewer_window.show()

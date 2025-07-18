from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from ui.item_form import ItemForm
from ui.main_menu import MainMenu
from ui.load_character import LoadCharacterMenu
from ui.item_viewer import ItemViewer
from gm_launcher import GMLauncher  # Đăng nhập GM từ giftcode

class EntryMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌌 Đạo Đồ – Khởi đầu")

        layout = QVBoxLayout()

        # 🔐 Ngụy trang ô Giftcode thành cửa ngõ vào GM
        self.label_gift = QLabel("🎁 Nhập mã giftcode:")
        self.input_gift = QLineEdit()
        self.btn_gift = QPushButton("Nhận")
        self.btn_gift.clicked.connect(self.check_giftcode)

        layout.addWidget(self.label_gift)
        layout.addWidget(self.input_gift)
        layout.addWidget(self.btn_gift)

        # 🧾 Nhập vật phẩm
        self.item_button = QPushButton("🧾 Nhập vật phẩm")
        self.item_button.clicked.connect(self.open_item_form)
        layout.addWidget(self.item_button)

        # 📜 Xem vật phẩm đã nhập
        self.viewer_button = QPushButton("📜 Xem vật phẩm đã nhập")
        self.viewer_button.clicked.connect(self.open_item_viewer)
        layout.addWidget(self.viewer_button)

        # 🌱 Tạo nhân vật mới
        self.btn_new = QPushButton("🌱 Tạo nhân vật mới")
        self.btn_new.clicked.connect(self.create_new)
        layout.addWidget(self.btn_new)

        # 🔄 Chơi lại nhân vật cũ
        self.btn_load = QPushButton("🔄 Chơi lại nhân vật cũ")
        self.btn_load.clicked.connect(self.load_existing)
        layout.addWidget(self.btn_load)

        self.setLayout(layout)

    def check_giftcode(self):
        code = self.input_gift.text()
        if code == "Trieu@182005":
            self.goto_gm()
        else:
            QMessageBox.information(self, "Mã quà tặng", "🎁 Mã giftcode không hợp lệ!")

    def goto_gm(self):
        self.gm_window = GMLauncher()
        self.gm_window.show()
        self.close()

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

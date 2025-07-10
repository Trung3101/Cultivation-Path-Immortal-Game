# ui/main_menu.py
import os
import json

from ui.character_info import CharacterInfo
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QMessageBox
)

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XUYÊN KHÔNG - ĐẠO ĐỒ")

        # Tạo label và ô nhập tên
        self.name_label = QLabel("Tên của bạn:")
        self.name_input = QLineEdit()

        # Tạo combo box chọn cảnh giới
        self.realm_label = QLabel("Chọn cảnh giới khởi đầu:")
        self.realm_select = QComboBox()
        self.realm_select.addItems(["Phàm Nhân", "Luyện Khí", "Trúc Cơ"])

        # Tạo nút bắt đầu
        self.start_button = QPushButton("Bắt đầu hành trình")
        self.start_button.clicked.connect(self.start_game)

        # Xếp các thành phần vào layout dọc
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.realm_label)
        layout.addWidget(self.realm_select)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def start_game(self):
        print("==> Đã vào hàm start_game()")
        name = self.name_input.text().strip()
        realm = self.realm_select.currentText()

        if not name:
            print("==> Không có tên, hiển thị cảnh báo")
            QMessageBox.warning(self, "Lỗi", "Bạn chưa nhập tên!")
            return

        user_data = {
            "name": name,
            "realm": realm,
            "exp": 0,
            "level": 1,
            "skills": [],
            "inventory": [],
            "dao_tam": "Trung Lập"
        }

        data_path = os.path.join("data", "users.json")
        print(f"==> Ghi vào: {data_path}")

        try:
            if os.path.exists(data_path):
                with open(data_path, "r", encoding="utf-8") as f:
                    users = json.load(f)
            else:
                users = []
        except Exception as e:
            print(f"==> Lỗi đọc file: {e}")
            users = []

        users.append(user_data)

        try:
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            print("==> Ghi dữ liệu xong.")
        except Exception as e:
            print(f"==> Lỗi ghi file: {e}")

        # Tạo giao diện tiếp theo
        self.character_window = CharacterInfo(user_data)
        self.character_window.show()
        self.close()  # đóng cửa sổ hiện tại


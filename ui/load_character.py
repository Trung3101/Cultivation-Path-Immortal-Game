# ui/load_character.py
import os, json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox
from ui.character_info import CharacterInfo

class LoadCharacterMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔄 Chọn nhân vật cũ")

        self.data_path = os.path.join("data", "users.json")
        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.btn_continue = QPushButton("🎮 Chơi tiếp")
        self.btn_delete = QPushButton("❌ Xoá nhân vật")
        self.btn_continue.setEnabled(False)
        self.btn_delete.setEnabled(False)

        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.btn_continue)
        self.layout.addWidget(self.btn_delete)
        self.setLayout(self.layout)

        self.load_characters()
        self.list_widget.itemClicked.connect(self.on_select)
        self.btn_continue.clicked.connect(self.play_game)
        self.btn_delete.clicked.connect(self.delete_character)

    def load_characters(self):
        if not os.path.exists(self.data_path):
            QMessageBox.information(self, "Không có dữ liệu", "Chưa có nhân vật nào được lưu.")
            self.close()
            return

        with open(self.data_path, "r", encoding="utf-8") as f:
            try:
                self.users = json.load(f)
            except:
                self.users = []

        if not self.users:
            QMessageBox.information(self, "Không có dữ liệu", "Danh sách nhân vật trống.")
            self.close()
            return

        for user in self.users:
            self.list_widget.addItem(f"{user['name']} – {user['realm']}")

    def on_select(self):
        self.btn_continue.setEnabled(True)
        self.btn_delete.setEnabled(True)

    def play_game(self):
        index = self.list_widget.currentRow()
        user_data = self.users[index]
        self.info_window = CharacterInfo(user_data)
        self.info_window.show()
        self.close()

    def delete_character(self):
        index = self.list_widget.currentRow()
        user = self.users[index]

        confirm = QMessageBox.question(
            self,
            "Xác nhận xoá",
            f"Bạn có chắc chắn muốn xoá nhân vật '{user['name']}' không?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            del self.users[index]

            # Ghi lại vào file
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)

            QMessageBox.information(self, "Đã xoá", "Nhân vật đã bị xoá.")
            self.list_widget.clear()
            self.btn_continue.setEnabled(False)
            self.btn_delete.setEnabled(False)
            self.load_characters()

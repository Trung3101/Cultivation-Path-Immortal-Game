# ui/character_info.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit

class CharacterInfo(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("📜 Thông tin nhân vật")
        self.user_data = user_data

        layout = QVBoxLayout()

        # Thông tin cơ bản
        basic_info = (
            f"👤 Tên: {user_data['name']}\n"
            f"🌌 Cảnh giới: {user_data['realm']}\n"
            f"⭐ Kinh nghiệm: {user_data['exp']}\n"
            f"🎯 Cấp độ: {user_data['level']}\n"
            f"🧭 Đạo tâm: {user_data['dao_tam']}\n"
        )

        # Kỹ năng
        skills = user_data.get("skills", [])
        skills_text = "\n".join(f"• {s}" for s in skills) if skills else "Chưa có kỹ năng nào."

        # Vật phẩm
        items = user_data.get("inventory", [])
        items_text = "\n".join(f"• {i}" for i in items) if items else "Túi trống trơn."

        # Ghép tổng thể
        full_text = (
            basic_info + "\n"
            + "📚 Kỹ năng:\n" + skills_text + "\n\n"
            + "🎒 Vật phẩm:\n" + items_text
        )

        self.info_area = QTextEdit()
        self.info_area.setText(full_text)
        self.info_area.setReadOnly(True)

        self.btn_back = QPushButton("🔙 Quay lại Menu")
        self.btn_back.clicked.connect(self.back_to_menu)

        layout.addWidget(self.info_area)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

    def back_to_menu(self):
        from ui.main_menu_game import MainGameMenu  # 👈 Lazy import tại đây
        self.menu = MainGameMenu(user_data=self.user_data)
        self.menu.show()
        self.close()

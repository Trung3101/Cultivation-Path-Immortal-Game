# ui/improve_technique.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QCheckBox, QMessageBox
)
from datetime import datetime

class ImproveTechnique(QWidget):
    def __init__(self, user_data, technique_item, inventory_manager):
        super().__init__()
        self.setWindowTitle("💠 Cải tiến công pháp")
        self.user_data = user_data
        self.technique = technique_item
        self.manager = inventory_manager

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(f"📘 Công pháp: {self.technique['name']}"))
        self.layout.addWidget(QLabel(f"⚡ Cảnh giới: {user_data['realm']}"))
        self.layout.addWidget(QLabel(f"🎯 Thành thục: {self.technique.get('mastery', 0)}%"))
        self.layout.addWidget(QLabel("🧬 Bạn muốn cải tiến gì?"))

        # Các lựa chọn cải tiến
        self.check_effect = QCheckBox("✨ Cải tiến hiệu ứng")
        self.check_element = QCheckBox("🌪️ Thay đổi hệ (element)")
        self.check_level = QCheckBox("🔺 Nâng cấp độ")
        self.check_name = QCheckBox("📛 Đổi tên công pháp")

        self.layout.addWidget(self.check_effect)
        self.layout.addWidget(self.check_element)
        self.layout.addWidget(self.check_level)
        self.layout.addWidget(self.check_name)

        self.btn_upgrade = QPushButton("🔧 Tiến hành cải tiến")
        self.btn_upgrade.clicked.connect(self.attempt_upgrade)
        self.layout.addWidget(self.btn_upgrade)

        self.setLayout(self.layout)

    def attempt_upgrade(self):
        if self.technique.get("mastery", 0) < 100:
            QMessageBox.warning(self, "Chưa đủ điều kiện", "Công pháp chưa thành thục (100%).")
            return

        # Tạm kiểm tra cảnh giới bằng tên
        if "Nguyên Anh" not in self.user_data["realm"]:
            QMessageBox.warning(self, "Cảnh giới quá thấp", "Cần đạt tối thiểu Nguyên Anh hậu kỳ để cải tiến.")
            return

        # Giả lập kiểm tra nguyên liệu (sau này sẽ đọc từ inventory thật)
        has_material = False
        for item in self.manager.get_items():
            if item.get("id") == "huyet_long_than":
                has_material = True
                break

        if not has_material:
            QMessageBox.warning(self, "Thiếu nguyên liệu", "Cần có Huyết Long Thần để cải tiến công pháp này.")
            return

        # Giả lập xác suất: thành công 70%, thất bại 25%, đột biến 5%
        from random import randint
        roll = randint(1, 100)

        if roll <= 70:
            self.apply_improvements()
            QMessageBox.information(self, "Thành công", "Công pháp đã được cải tiến thành công!")
        elif roll <= 95:
            QMessageBox.information(self, "Thất bại", "Cải tiến thất bại. Công pháp giữ nguyên, nguyên liệu bị mất.")
        else:
            self.apply_mutation()
            QMessageBox.information(self, "Đột biến!", "Một biến dị hiếm đã xảy ra! Bạn nhận được công pháp đặc biệt.")

        # Ghi lịch sử cải tiến
        self.save_upgrade_log()
        self.close()

    def apply_improvements(self):
        if self.check_effect.isChecked():
            self.technique["effect"] = "Đột phá giới hạn long khí, hỗ trợ công kích đa hệ"

        if self.check_element.isChecked():
            self.technique["element"] = "hỗn độn"

        if self.check_level.isChecked():
            self.technique["level"] += 1

        if self.check_name.isChecked():
            self.technique["name"] = self.technique["name"] + " • Thần Biến"

        # Update túi đồ
        self.manager.save_inventory()

    def apply_mutation(self):
        self.technique["name"] = "Long Ma Hỗn Độn Đạo"
        self.technique["element"] = "ma-long"
        self.technique["effect"] = "Công pháp hỗn hợp ma đạo – long tộc, không thể tu luyện bởi chính đạo"
        self.technique["level"] = 9

        self.manager.save_inventory()

    def save_upgrade_log(self):
        log_path = f"data/player_analysis/{self.user_data['id']}/upgrade_log.txt"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] Đã cố gắng cải tiến: {self.technique['name']}\n")

import json
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap

class ItemDetail(QWidget):
    def __init__(self, item_data):
        super().__init__()
        self.setWindowTitle(f"Chi tiết: {item_data['name']}")
        self.setGeometry(400, 250, 500, 600)

        layout = QVBoxLayout()

        # Tên
        name_label = QLabel(f"<b>{item_data['name']}</b>")
        layout.addWidget(name_label)

        # Icon
        icon_path = item_data.get("icon", "")
        if not os.path.exists(icon_path):
            icon_path = "icons/default.png"

        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label = QLabel()
            icon_label.setPixmap(pixmap.scaled(100, 100))
            layout.addWidget(icon_label)

        # Mô tả
        desc_label = QLabel("📜 Mô tả:")
        layout.addWidget(desc_label)

        desc_text = QTextEdit(item_data.get("description", "Không có mô tả"))
        desc_text.setReadOnly(True)
        layout.addWidget(desc_text)

        # Effect
        effect_label = QLabel("⚙️ Hiệu ứng:")
        layout.addWidget(effect_label)

        effect_text = QTextEdit()
        effect_text.setReadOnly(True)

        parsed = self.parse_effect(item_data.get("effect"))
        effect_text.setPlainText(parsed)
        layout.addWidget(effect_text)

        self.setLayout(layout)

    def parse_effect(self, effect_json):
        if not effect_json:
            return "Không có hiệu ứng."

        try:
            effect = json.loads(effect_json)
            text = ""

            # stats
            stats = effect.get("stats", {})
            for key, val in stats.items():
                name = self.stat_translate(key)
                text += f"+{val} {name}\n"

            # element
            element = effect.get("element")
            if element:
                text += f"+{element.get('bonus', 0)} sát thương nguyên tố {element.get('type', '')}\n"

            # special
            specials = effect.get("special", [])
            for s in specials:
                text += f"* {s}\n"

            return text.strip()
        except Exception as e:
            return f"[LỖI PARSE EFFECT]: {e}"

    def stat_translate(self, key):
        return {
            "attack": "Tấn công",
            "defense": "Phòng thủ",
            "crit_rate": "Tỷ lệ chí mạng",
            "crit_damage": "Sát thương chí mạng",
            "hp": "Máu",
            "mana": "Linh lực",
            "speed": "Tốc độ",
            "armor_penetration": "Xuyên giáp",
        }.get(key, key)

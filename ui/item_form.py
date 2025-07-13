import sqlite3
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QComboBox, QCheckBox, QSpinBox
)

class ItemForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thêm vật phẩm vào Đạo Đồ")
        db_path = os.path.join(os.getcwd(), r"D:\Bài tập python nâng cao\Game Tu Tiên_Đạo Đồ\Xuyên Không\dao_do_items.db")
        self.conn = sqlite3.connect(db_path)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.inputs = {}

        fields = [
            ("id", QLineEdit), ("name", QLineEdit), ("type", QLineEdit),
            ("rank", QLineEdit), ("description", QTextEdit),
            ("effect", QTextEdit), ("origin", QLineEdit), ("icon", QLineEdit),
            ("stackable", QCheckBox), ("usable", QCheckBox),
            ("craftable", QCheckBox), ("rarity", QLineEdit),
            ("price", QSpinBox), ("require_level", QSpinBox),
            ("require_gender", QLineEdit), ("class_restriction", QLineEdit)
        ]

        for label_text, widget_class in fields:
            label = QLabel(label_text)
            if widget_class == QCheckBox:
                widget = widget_class()
            elif widget_class == QSpinBox:
                widget = widget_class()
                widget.setMaximum(999999)
            else:
                widget = widget_class()
            self.inputs[label_text] = widget
            layout.addWidget(label)
            layout.addWidget(widget)

        submit_btn = QPushButton("💾 Thêm vật phẩm")
        submit_btn.clicked.connect(self.add_item)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def add_item(self):
        try:
            data = {
                key: (
                    self.inputs[key].isChecked()
                    if isinstance(self.inputs[key], QCheckBox)
                    else self.inputs[key].value()
                    if isinstance(self.inputs[key], QSpinBox)
                    else self.inputs[key].text()
                    if isinstance(self.inputs[key], QLineEdit)
                    else self.inputs[key].toPlainText()
                )
                for key in self.inputs
            }

            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO items (
                    id, name, type, rank, description, effect,
                    origin, icon, stackable, usable, craftable,
                    rarity, price, require_level, require_gender,
                    class_restriction
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(data.values()))
            self.conn.commit()

            QMessageBox.information(self, "Thành công", "Đã thêm vật phẩm!")
            for w in self.inputs.values():
                if isinstance(w, (QLineEdit, QTextEdit)):
                    w.clear()
                elif isinstance(w, QCheckBox):
                    w.setChecked(False)
                elif isinstance(w, QSpinBox):
                    w.setValue(0)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

import os
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)

class ItemViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📜 Danh sách vật phẩm đã nhập")
        self.setGeometry(300, 200, 900, 500)
        db_path = os.path.join(os.getcwd(), r"D:\Bài tập python nâng cao\Game Tu Tiên_Đạo Đồ\Xuyên Không\dao_do_items.db")
        self.conn = sqlite3.connect(db_path)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("📦 Dưới đây là toàn bộ vật phẩm đã nhập:")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.load_items()

    def load_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, type, rank, rarity, price, require_level FROM items")
        items = cursor.fetchall()

        self.table.setRowCount(len(items))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên", "Loại", "Phẩm", "Độ hiếm", "Giá", "Yêu cầu cấp"
        ])

        for row_idx, row_data in enumerate(items):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

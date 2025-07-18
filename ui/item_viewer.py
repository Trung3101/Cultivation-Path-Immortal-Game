import os
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)
from PyQt5.QtCore import Qt
from ui.item_detail import ItemDetail

class ItemViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Danh sách vật phẩm đã nhập")
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

        self.table.cellDoubleClicked.connect(self.show_detail)

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

    def show_detail(self, row, column):
        item_data = {}
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col).text().lower()
            value = self.table.item(row, col).text()
            item_data[header] = value

        # Lấy dữ liệu chi tiết từ DB
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_data["id"],))
        row_data = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        full_item = dict(zip(columns, row_data))

        self.detail_window = ItemDetail(full_item)
        self.detail_window.show()

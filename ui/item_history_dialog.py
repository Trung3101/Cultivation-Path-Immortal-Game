from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QColor
from data.item_log import get_edit_log
from datetime import datetime

class ItemHistoryDialog(QDialog):
    def __init__(self, item_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🕓 Lịch sử sửa đổi vật phẩm")
        self.setMinimumSize(700, 450)

        self.item_id = item_id
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "🕒 Thời gian", "👤 Người sửa", "📌 Trường", "🧾 Giá trị cũ", "🆕 Giá trị mới"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"📜 Lịch sử sửa đổi - Vật phẩm ID: {self.item_id}"))
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_data()

    def format_timestamp(self, raw_time):
        try:
            dt = datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d-%m-%Y %H:%M:%S")
        except:
            return raw_time  # fallback nếu không parse được

    def load_data(self):
        logs = get_edit_log(self.item_id)
        self.table.setRowCount(len(logs))

        for row, log in enumerate(logs):
            time_item = QTableWidgetItem(self.format_timestamp(log["timestamp"]))
            editor_item = QTableWidgetItem(log["editor"])
            field_item = QTableWidgetItem(log["field_changed"])
            old_item = QTableWidgetItem(str(log["old_value"]))
            new_item = QTableWidgetItem(str(log["new_value"]))

            # Tooltip nếu mô tả dài
            for item in [old_item, new_item]:
                if len(item.text()) > 40:
                    item.setToolTip(item.text())

            # Nếu thay đổi "rank_id" hoặc "type_id" → đổi màu
            if log["field_changed"] in ("rank_id", "type_id"):
                for cell in [field_item, old_item, new_item]:
                    cell.setBackground(QColor(255, 255, 180))  # vàng nhạt

            self.table.setItem(row, 0, time_item)
            self.table.setItem(row, 1, editor_item)
            self.table.setItem(row, 2, field_item)
            self.table.setItem(row, 3, old_item)
            self.table.setItem(row, 4, new_item)

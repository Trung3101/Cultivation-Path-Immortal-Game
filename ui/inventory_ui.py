# ui/inventory_ui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox,
    QDialog, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt
from ui.inventory_manager import InventoryManager
from ui.analyze_ai import mock_ai_analyze
from ui.improve_technique import ImproveTechnique
from ui.soul_dialog import SoulDialog

class InventoryUI(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("🎒 Túi Trữ Vật")
        self.user_data = user_data
        self.manager = InventoryManager(user_data["name"])
        self.grid_size = 5  # 5x5 ô

        self.layout = QVBoxLayout()
        self.label = QLabel(f"🧍 Nhân vật: {user_data['name']} – Ô đã dùng: {len(self.manager.items)} / {self.manager.max_slots}")
        self.grid = QGridLayout()

        self.layout.addWidget(self.label)
        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)

        self.render_grid()

    def render_grid(self):
        self.clear_grid()

        items = self.manager.get_items()
        for index, item in enumerate(items):
            row = index // self.grid_size
            col = index % self.grid_size
            btn = QPushButton(self.get_item_icon(item))
            btn.setToolTip(item["name"])
            btn.clicked.connect(lambda checked, it=item: self.show_item_detail(it))

            color = self.get_border_color(item["rank"])
            btn.setStyleSheet(f"border: 2px solid {color}; padding: 10px;")

            self.grid.addWidget(btn, row, col)

    def clear_grid(self):
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def get_item_icon(self, item):
        type_map = {
            "Đan dược": "💊",
            "Pháp bảo": "🗡️",
            "Trang bị": "🛡️",
            "Linh thạch": "🔮",
            "Nguyên liệu": "🌿",
            "Phù chú": "📜",
            "Công pháp": "📘",
            "Tọa kỵ": "🐎",
            "Đạo cụ đặc biệt": "✨",
            "Nhiệm vụ": "🧩"
        }
        icon = type_map.get(item.get("type", ""), "❓")
        q = item.get("quantity", "")
        return f"{icon} {q}" if q else icon

    def get_border_color(self, rank):
        color_map = {
            "Phàm": "gray",
            "Nhân": "lightgreen",
            "Hoàng": "gold",
            "Huyền": "purple",
            "Địa": "darkorange",
            "Thiên": "red",
            "Tiên": "cyan",
            "Chí Tôn": "deeppink",
            "Vũ Trụ": "blue",
            "Hỗn Nguyên": "black"
        }
        return color_map.get(rank, "silver")

    def show_item_detail(self, item):
        dialog = QDialog(self)
        dialog.setWindowTitle(item["name"])
        layout = QVBoxLayout()

        desc = QTextEdit()
        desc.setReadOnly(True)

        # Format chi tiết vật phẩm
        text = f"""
    📝 Tên: {item['name']}
    🏷️ Loại: {item.get('type', '')}
    🧬 Phẩm: {item.get('rank', '')} – {item.get('tier', '')}
    📄 Mô tả: {item.get('description', '')}
    """
        if "effect" in item:
            text += f"⚡ Tác dụng: {item['effect']}\n"
        if "power" in item:
            text += f"🗡️ Sức mạnh: {item['power']}\n"
        if "defense" in item:
            text += f"🛡️ Phòng ngự: {item['defense']}\n"
        if "durability" in item:
            text += f"⏳ Độ bền: {item['durability']}\n"
        if "quantity" in item:
            text += f"📦 Số lượng: {item['quantity']}\n"

        desc.setText(text.strip())
        layout.addWidget(desc)

        # Nếu là loại có thể sử dụng
        if item.get("type") in ["Đan dược", "Linh thạch", "Phù chú"]:
            btn_use = QPushButton("🔘 Sử dụng")
            btn_use.clicked.connect(lambda: self.use_item(item, dialog))
            layout.addWidget(btn_use)

        # Nếu có mô tả thì cho phép phân tích
        if "description" in item:
            btn_analyze = QPushButton("🔍 Phân tích")
            btn_analyze.clicked.connect(lambda: self.analyze_item(item))
            layout.addWidget(btn_analyze)

        # Nếu là công pháp & có thể cải tiến thì cho nút cải tiến
        if item.get("type") == "Công pháp" and item.get("can_upgrade", False):
            btn_upgrade = QPushButton("💠 Cải tiến")
            btn_upgrade.clicked.connect(lambda: self.open_upgrade(item))
            layout.addWidget(btn_upgrade)

        # Nếu vật phẩm có hồn trí thì thêm nút giao tiếp
        if item.get("soulbound", False):
            btn_soul = QPushButton("💬 Giao tiếp Hồn Trí")
            btn_soul.clicked.connect(lambda: self.open_soul_dialog(item))
            layout.addWidget(btn_soul)

        dialog.setLayout(layout)
        dialog.exec_()

    def use_item(self, item, dialog):
        if item.get("quantity", 0) <= 0:
            QMessageBox.warning(self, "Lỗi", "Không còn đủ vật phẩm để sử dụng.")
            return

        # Thực hiện "sử dụng" đan dược
        item["quantity"] -= 1
        if item["quantity"] == 0:
            self.manager.items.remove(item)

        # Giả lập: nếu có "exp" trong effect → cộng exp
        if "exp" in item.get("effect", "").lower():
            self.user_data["exp"] += 100  # Có thể cải tiến đọc số từ effect sau

        QMessageBox.information(self, "Đã dùng", f"Đã sử dụng 1 {item['name']}")
        self.manager.save_inventory()
        dialog.close()
        self.label.setText(f"🧍 Nhân vật: {self.user_data['name']} – Ô đã dùng: {len(self.manager.items)} / {self.manager.max_slots}")
        self.render_grid()

    def analyze_item(self, item):
        analysis = mock_ai_analyze(item.get("description", "Không có mô tả."))

        text = (
            f"🔎 Tính chất: {analysis['tính_chất']}\n\n"
            f"⚠️ Nguy cơ: {analysis['nguy_cơ']}\n\n"
            f"📌 Khuyến nghị: {analysis['khuyến_nghị']}"
        )

        QMessageBox.information(self, f"Phân tích {item['name']}", text)

    def open_upgrade(self, item):
        self.upgrade_ui = ImproveTechnique(self.user_data, item, self.manager)
        self.upgrade_ui.show()

    def open_soul_dialog(self, item):
        self.soul_dialog = SoulDialog(self.user_data, item)
        self.soul_dialog.exec_()

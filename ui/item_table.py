from PyQt5.QtWidgets import QWidget, QShortcut, QMessageBox, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from data.constants import ADMIN_PASSWORD
from ui.login_admin_dialog import LoginAdminDialog
from data.item_manager import get_all_items
import traceback

class ItemTable(QWidget):
    def __init__(self, enable_shortcut=True):
        super().__init__()
        self.admin_mode = False
        self.setup_ui()
        self.load_items()

        if enable_shortcut:
            self.setup_shortcuts()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.btn_edit = QPushButton("✏️ Sửa vật phẩm")
        self.btn_edit.clicked.connect(self.edit_selected_item)
        self.btn_delete = QPushButton("🗑️ Xoá vật phẩm")
        self.btn_recover_items = QPushButton("♻️ Khôi phục vật phẩm")

        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_recover_items)

        self.btn_edit.hide()
        self.btn_delete.hide()
        self.btn_recover_items.hide()

    def setup_shortcuts(self):
        self.shortcut_gm = QShortcut(QKeySequence("Ctrl+Shift+G"), self)
        self.shortcut_gm.activated.connect(self.show_gm_login)

    def show_gm_login(self):
        if self.admin_mode:
            return
        dialog = LoginAdminDialog(self)
        if dialog.exec_():
            self.enable_admin_controls()

    def enable_admin_controls(self):
        self.admin_mode = True
        self.btn_edit.show()
        self.btn_delete.show()
        self.btn_recover_items.show()
        QMessageBox.information(self, "GM Mode", "🎮 Quyền quản trị đã được kích hoạt!")

    def edit_selected_item(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "⚠️ Chưa chọn vật phẩm", "Vui lòng chọn một vật phẩm để sửa.")
            return

        item_id = self.table.item(selected_row, 0).text()

        try:
            from ui.edit_item_dialog import EditItemDialog
            from data.item_manager import get_item_by_id

            item = get_item_by_id(item_id)
            if item is None:
                QMessageBox.critical(self, "Lỗi", f"Không tìm thấy vật phẩm ID: {item_id}")
                return

            dialog = EditItemDialog(item_id, editor_name="Master GM", parent=self)
            if dialog.exec_():
                self.load_items()
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            QMessageBox.critical(self, "Lỗi khi mở hộp thoại", f"Chi tiết lỗi:\n{e}\n\n{tb}")

    def load_items(self):
        items = get_all_items()
        if not items:
            self.table.setRowCount(0)
            return

        columns = list(items[0].keys())
        self.table.setRowCount(len(items))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for row, item in enumerate(items):
            for col, key in enumerate(columns):
                self.table.setItem(row, col, QTableWidgetItem(str(item[key])))

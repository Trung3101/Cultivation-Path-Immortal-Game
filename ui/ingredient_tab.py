from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QLineEdit, QFormLayout, QTableWidgetItem, QMessageBox
from data.ingredient_manager import get_ingredients_for_item, add_ingredient, update_ingredient, delete_ingredient

class IngredientTab(QWidget):
    def __init__(self, item_id, parent=None):
        super().__init__(parent)
        self.item_id = item_id
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.btn_add = QPushButton("➕ Thêm nguyên liệu")
        self.btn_add.clicked.connect(self.add_row)
        self.layout.addWidget(self.btn_add)

        self.load_ingredients()

    def load_ingredients(self):
        data = get_ingredients_for_item(self.item_id)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Tên nguyên liệu", "Số lượng", "Ghi chú"])
        self.table.setRowCount(len(data))
        for row, (ing_id, name, qty, note) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(ing_id)))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(str(qty)))
            self.table.setItem(row, 3, QTableWidgetItem(note))

    def add_row(self):
        name, qty, note = "Nguyên liệu mới", 1, ""
        add_ingredient(self.item_id, name, qty, note)
        self.load_ingredients()

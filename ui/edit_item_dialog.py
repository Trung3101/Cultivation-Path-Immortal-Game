from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QComboBox, QTabWidget, QWidget, QFormLayout, QMessageBox, QHBoxLayout
)
from data.item_manager import get_item_by_id, update_item
from data.item_log import log_edit
from ui.item_history_dialog import ItemHistoryDialog
from ui.ingredient_tab import IngredientTab

class EditItemDialog(QDialog):
    def __init__(self, item_id, editor_name="admin", parent=None):
        super().__init__(parent)
        self.setWindowTitle("🛠️ Sửa vật phẩm")
        self.setMinimumSize(600, 500)

        self.item_id = item_id
        self.editor_name = editor_name
        self.original_item = get_item_by_id(item_id)

        self.fields = {}  # lưu các widget sửa

        self.tabs = QTabWidget()
        self.tab_basic = QWidget()
        self.tab_advanced = QWidget()
        self.tab_attributes = QWidget()

        self.build_tabs()

        self.tab_ingredients = IngredientTab(item_id=self.item_id)
        self.tabs.addTab(self.tab_ingredients, "🧪 Nguyên liệu")

        self.btn_save = QPushButton("💾 Lưu thay đổi")
        self.btn_save.clicked.connect(self.save_changes)

        self.btn_history = QPushButton("🕓 Lịch sử sửa đổi")
        self.btn_history.clicked.connect(self.open_history)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_history)
        self.setLayout(layout)

    def build_tabs(self):
        # TAB CƠ BẢN
        basic_layout = QFormLayout()
        self.id_field = QLineEdit(self.item_id)
        self.id_field.setReadOnly(True)
        self.fields["id"] = self.id_field

        self.name_edit = QLineEdit(self.original_item["name"])
        self.fields["name"] = self.name_edit

        self.type_edit = QLineEdit(self.original_item["type"])
        self.fields["type"] = self.type_edit

        self.rank_edit = QLineEdit(self.original_item["rank"])
        self.fields["rank"] = self.rank_edit

        self.description_edit = QTextEdit(self.original_item["description"])
        self.fields["description"] = self.description_edit

        basic_layout.addRow("🆔 ID (không sửa):", self.id_field)
        basic_layout.addRow("📛 Tên vật phẩm:", self.name_edit)
        basic_layout.addRow("🏷️ Loại:", self.type_edit)
        basic_layout.addRow("👑 Phẩm cấp:", self.rank_edit)
        basic_layout.addRow("📜 Mô tả:", self.description_edit)
        self.tab_basic.setLayout(basic_layout)

        # TAB NÂNG CAO
        adv_layout = QFormLayout()
        self.effect_edit = QTextEdit(self.original_item.get("effect", ""))
        self.fields["effect"] = self.effect_edit

        self.origin_edit = QLineEdit(self.original_item.get("origin", ""))
        self.fields["origin"] = self.origin_edit

        self.icon_edit = QLineEdit(self.original_item.get("icon", ""))
        self.fields["icon"] = self.icon_edit

        self.ingredients_edit = QTextEdit(self.original_item.get("ingredients", ""))
        self.fields["ingredients"] = self.ingredients_edit

        self.rarity_edit = QLineEdit(self.original_item.get("rarity", ""))
        self.fields["rarity"] = self.rarity_edit

        adv_layout.addRow("✨ Hiệu ứng:", self.effect_edit)
        adv_layout.addRow("🌍 Nguồn gốc:", self.origin_edit)
        adv_layout.addRow("🖼️ Icon:", self.icon_edit)
        adv_layout.addRow("🧪 Nguyên liệu:", self.ingredients_edit)
        adv_layout.addRow("💎 Độ hiếm:", self.rarity_edit)
        self.tab_advanced.setLayout(adv_layout)

        # TAB THUỘC TÍNH
        attr_layout = QFormLayout()

        self.stackable = QComboBox()
        self.stackable.addItems(["0", "1"])
        self.stackable.setCurrentText(str(self.original_item.get("stackable", 0)))
        self.fields["stackable"] = self.stackable

        self.usable = QComboBox()
        self.usable.addItems(["0", "1"])
        self.usable.setCurrentText(str(self.original_item.get("usable", 0)))
        self.fields["usable"] = self.usable

        self.craftable = QComboBox()
        self.craftable.addItems(["0", "1"])
        self.craftable.setCurrentText(str(self.original_item.get("craftable", 0)))
        self.fields["craftable"] = self.craftable

        self.price_edit = QLineEdit(str(self.original_item.get("price", 0)))
        self.fields["price"] = self.price_edit

        self.require_level = QLineEdit(str(self.original_item.get("require_level", 0)))
        self.fields["require_level"] = self.require_level

        self.require_gender = QLineEdit(self.original_item.get("require_gender", ""))
        self.fields["require_gender"] = self.require_gender

        self.class_restriction = QLineEdit(self.original_item.get("class_restriction", ""))
        self.fields["class_restriction"] = self.class_restriction

        attr_layout.addRow("📦 Xếp chồng:", self.stackable)
        attr_layout.addRow("🥤 Có thể dùng:", self.usable)
        attr_layout.addRow("🔧 Có thể chế:", self.craftable)
        attr_layout.addRow("💰 Giá:", self.price_edit)
        attr_layout.addRow("🎓 Yêu cầu cấp:", self.require_level)
        attr_layout.addRow("🚻 Yêu cầu giới tính:", self.require_gender)
        attr_layout.addRow("⚔️ Hạn chế lớp:", self.class_restriction)

        self.tab_attributes.setLayout(attr_layout)

        # Thêm tabs
        self.tabs.addTab(self.tab_basic, "🔹 Cơ bản")
        self.tabs.addTab(self.tab_advanced, "🔸 Nâng cao")
        self.tabs.addTab(self.tab_attributes, "🧬 Thuộc tính")

    def save_changes(self):
        updates = {}

        for field, widget in self.fields.items():
            if field in ("id", "ingredients"):  # ❌ Không cập nhật những cột không tồn tại
                continue
            if isinstance(widget, QLineEdit):
                new_val = widget.text()
            elif isinstance(widget, QTextEdit):
                new_val = widget.toPlainText()
            elif isinstance(widget, QComboBox):
                new_val = int(widget.currentText())
            else:
                continue

            old_val = self.original_item.get(field)
            if str(old_val) != str(new_val):
                updates[field] = new_val
                log_edit(
                    item_id=self.item_id,
                    editor=self.editor_name,
                    field_changed=field,
                    old_value=old_val,
                    new_value=new_val
                )

        if updates:
            update_item(self.item_id, updates)
            QMessageBox.information(self, "✅ Thành công", "Đã lưu thay đổi.")
            self.accept()
        else:
            QMessageBox.information(self, "ℹ️ Không thay đổi", "Bạn chưa chỉnh sửa gì.")

    def open_history(self):
        dialog = ItemHistoryDialog(self.item_id)
        dialog.exec_()

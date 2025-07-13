# ui/main_menu_game.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from ui.train import TrainWindow
from ui.vision import VisionWindow
from ui.explore import ExploreWindow
from ui.battle import BattleWindow
from ui.character_info import CharacterInfo
from ui.inventory_ui import InventoryUI

class MainGameMenu(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("Menu Chính – Đạo Đồ")

        self.user_data = user_data

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"👋 Chào {user_data['name']} – Cảnh giới: {user_data['realm']}"))

        # Các nút chức năng
        self.train_button = QPushButton("🧘 Tu luyện")
        self.explore_button = QPushButton("🗺️ Ra ngoài")
        self.fight_button = QPushButton("⚔️ Chiến đấu")
        self.vision_button = QPushButton("👁️ Nhìn xuyên căn nguyên")
        self.info_button = QPushButton("📜 Xem nhân vật")
        self.quit_button = QPushButton("🔙 Thoát game")
        self.train_button.clicked.connect(self.open_training)
        self.vision_button.clicked.connect(self.open_vision)
        self.explore_button.clicked.connect(self.open_explore)
        self.fight_button.clicked.connect(self.open_battle)
        self.info_button.clicked.connect(self.open_info)
        self.inventory_button = QPushButton("🎒 Túi đồ")
        self.inventory_button.clicked.connect(self.open_inventory)
        layout.addWidget(self.inventory_button)

        # Thêm nút vào layout
        layout.addWidget(self.train_button)
        layout.addWidget(self.explore_button)
        layout.addWidget(self.fight_button)
        layout.addWidget(self.vision_button)
        layout.addWidget(self.info_button)
        layout.addWidget(self.quit_button)

        # Thoát game
        self.quit_button.clicked.connect(self.close)

        self.setLayout(layout)

    def open_training(self):
        self.train_window = TrainWindow(self.user_data)
        self.train_window.show()

    def open_vision(self):
        self.vision_window = VisionWindow(self.user_data)
        self.vision_window.show()

    def open_explore(self):
        self.explore_window = ExploreWindow(self.user_data)
        self.explore_window.show()

    def open_battle(self):
        self.battle_window = BattleWindow(self.user_data)
        self.battle_window.show()

    def open_info(self):
        import importlib
        CharacterInfo = importlib.import_module("ui.character_info").CharacterInfo
        self.info_window = CharacterInfo(self.user_data)
        self.info_window.show()
        self.close()

    def open_inventory(self):
        self.inventory_window = InventoryUI(self.user_data)
        self.inventory_window.show()

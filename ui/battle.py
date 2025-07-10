# ui/battle.py
import random
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QMessageBox

class BattleWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("⚔️ Chiến đấu")
        self.user_data = user_data

        # Tạo kẻ địch ngẫu nhiên
        self.enemy = self.generate_enemy()

        # Chỉ số cơ bản
        self.player_hp = 100
        self.player_atk = random.randint(10, 20)
        self.enemy_hp = self.enemy["hp"]
        self.enemy_atk = self.enemy["atk"]

        # Giao diện
        layout = QVBoxLayout()

        self.label_player = QLabel(f"👤 Bạn: {user_data['name']} | HP: {self.player_hp}")
        self.label_enemy = QLabel(f"👹 Địch: {self.enemy['name']} | HP: {self.enemy_hp}")
        self.battle_log = QTextEdit()
        self.battle_log.setReadOnly(True)
        self.btn_attack = QPushButton("Tấn công!")
        self.btn_attack.clicked.connect(self.fight_turn)

        layout.addWidget(self.label_player)
        layout.addWidget(self.label_enemy)
        layout.addWidget(self.battle_log)
        layout.addWidget(self.btn_attack)

        self.setLayout(layout)

    def generate_enemy(self):
        enemies = [
            {"name": "Yêu Lang", "hp": 80, "atk": 12},
            {"name": "Quỷ Mị", "hp": 100, "atk": 15},
            {"name": "Xác sống Tu sĩ", "hp": 120, "atk": 10},
            {"name": "Thần Thú Lạc Lôi", "hp": 150, "atk": 18}
        ]
        return random.choice(enemies)

    def fight_turn(self):
        if self.player_hp <= 0 or self.enemy_hp <= 0:
            return

        # Người chơi tấn công trước
        damage = self.player_atk + random.randint(-3, 3)
        self.enemy_hp -= damage
        self.battle_log.append(f"🗡️ Bạn tấn công gây {damage} sát thương!")

        if self.enemy_hp <= 0:
            self.enemy_hp = 0
            self.end_battle(winner="player")
            return

        # Địch phản công
        damage_enemy = self.enemy_atk + random.randint(-2, 4)
        self.player_hp -= damage_enemy
        self.battle_log.append(f"👹 {self.enemy['name']} phản công gây {damage_enemy} sát thương!")

        if self.player_hp <= 0:
            self.player_hp = 0
            self.end_battle(winner="enemy")
            return

        # Cập nhật chỉ số
        self.label_player.setText(f"👤 Bạn: {self.user_data['name']} | HP: {self.player_hp}")
        self.label_enemy.setText(f"👹 Địch: {self.enemy['name']} | HP: {self.enemy_hp}")

    def end_battle(self, winner):
        self.label_player.setText(f"👤 Bạn: {self.user_data['name']} | HP: {self.player_hp}")
        self.label_enemy.setText(f"👹 Địch: {self.enemy['name']} | HP: {self.enemy_hp}")
        self.btn_attack.setEnabled(False)

        if winner == "player":
            self.battle_log.append("🎉 Bạn đã chiến thắng!")
            self.user_data["exp"] += 10
            self.save_progress()
            QMessageBox.information(self, "Thắng lợi!", "Bạn đã chiến thắng và nhận 10 EXP!")
        else:
            self.battle_log.append("💀 Bạn đã thất bại...")
            QMessageBox.information(self, "Thất bại", "Bạn đã bị đánh bại. Hãy thử lại sau.")

    def save_progress(self):
        import json, os

        path = os.path.join("data", "users.json")
        if not os.path.exists(path):
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                users = json.load(f)
        except:
            users = []

        for user in users:
            if user["name"] == self.user_data["name"]:
                user.update(self.user_data)
                break

        with open(path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

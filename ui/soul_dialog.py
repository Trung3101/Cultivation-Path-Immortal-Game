# ui/soul_dialog.py

import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
)

SOUL_RESPONSES = {
    1: {
        "greeting": "…Ai đó? Linh thức ta mờ nhạt… ngươi là… chủ nhân mới?",
        "responses": [
            "Ta từng là khí linh của một luyện khí sư vô danh.",
            "Ngươi… còn quá yếu. Ta chưa thể toàn tâm trợ lực.",
            "Ta chỉ muốn… được chiến đấu một lần nữa..."
        ]
    },
    2: {
        "greeting": "Ngươi cảm nhận được ta sao? Không tệ…",
        "responses": [
            "Ta là tàn niệm của Huyết Nguyệt Kiếm Chủ, phong ấn nơi hư không.",
            "Niềm tin là thứ dễ vỡ, nhưng hãy thử một lần.",
            "Thả ta ra khỏi lớp bụi quên lãng… và ta sẽ chiến đấu bên ngươi."
        ]
    },
    3: {
        "greeting": "Cuối cùng, ngươi đã nghe tiếng ta gọi trong mộng tưởng…",
        "responses": [
            "Ta là Kiếm Hồn Long Thần – từng chém thiên yêu tại Vạn Long Cốc.",
            "Linh hồn ngươi dao động… nhưng có một đạo tâm đủ sâu.",
            "Hãy rèn luyện thêm, rồi ta sẽ trao ngươi huyết ấn của Chân Long."
        ]
    },
    4: {
        "greeting": "Ta đã đợi… hàng vạn năm trong giấc ngủ vô tận.",
        "responses": [
            "Khi ta còn tỉnh thức, cả giới tu chân quỳ dưới Kiếm Vực ta tạo.",
            "Không ai có thể điều khiển ta – ngoại trừ người mà ta công nhận.",
            "Ngươi… có thể là kẻ đó chăng?"
        ]
    },
    5: {
        "greeting": "Đã lâu… kể từ khi ta gọi tên ai đó là 'Chủ Nhân'.",
        "responses": [
            "Ta là hồn khí vĩnh hằng – kết nối với Đạo Luân chính khí.",
            "Linh giới này sắp tan. Ngươi… là hi vọng cuối cùng.",
            "Ta nguyện hiến toàn bộ sức mạnh nếu ngươi bước qua Hư Đạo Kiếp."
        ]
    }
}

class SoulDialog(QDialog):
    def __init__(self, user_data, item_data):
        super().__init__()
        self.user_data = user_data
        self.item_data = item_data
        self.soul_tier = item_data.get("soul_tier", 1)
        self.bond_level = 0

        self.setWindowTitle(f"💬 Giao tiếp với {item_data['name']}")
        self.layout = QVBoxLayout()

        # Câu chào đầu
        greeting = SOUL_RESPONSES.get(self.soul_tier, SOUL_RESPONSES[1])["greeting"]
        self.label = QLabel(f"🧿 {greeting}")
        self.layout.addWidget(self.label)

        # Nút tương tác
        for i, option in enumerate([
            "Ngươi là ai?",
            "Ta có thể tin ngươi không?",
            "Ngươi muốn gì từ ta?"
        ]):
            btn = QPushButton(option)
            btn.clicked.connect(lambda _, idx=i: self.respond(idx))
            self.layout.addWidget(btn)

        self.setLayout(self.layout)

    def respond(self, index):
        response_set = SOUL_RESPONSES.get(self.soul_tier, SOUL_RESPONSES[1])
        if index < len(response_set["responses"]):
            response = response_set["responses"][index]
            QMessageBox.information(self, "⚡ Phản hồi từ khí linh", response)
            self.bond_level += 1
            self.save_log(response)

    def save_log(self, last_response):
        folder = f"data/soul_logs/{self.user_data['id']}"
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{self.item_data['id']}.json")

        data = {
            "item_name": self.item_data["name"],
            "soul_tier": self.soul_tier,
            "bond_level": self.bond_level,
            "last_contact": datetime.now().isoformat(),
            "last_response": last_response
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

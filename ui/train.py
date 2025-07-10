# ui/train.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer

class TrainWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("🧘 Tu luyện")
        self.user_data = user_data
        self.training_time = 0
        self.elapsed = 0

        layout = QVBoxLayout()

        self.label_status = QLabel("Chọn thời gian tu luyện:")
        self.combo_time = QComboBox()
        self.combo_time.addItems(["30", "60", "120"])  # giây
        self.btn_start = QPushButton("Bắt đầu tu luyện")
        self.label_timer = QLabel("⏳ Chưa bắt đầu")
        self.btn_start.clicked.connect(self.start_training)

        layout.addWidget(self.label_status)
        layout.addWidget(self.combo_time)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.label_timer)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_training(self):
        self.training_time = int(self.combo_time.currentText())
        self.elapsed = 0
        self.label_timer.setText(f"Đang tu luyện: 0 / {self.training_time} giây")
        self.timer.start(1000)  # gọi mỗi 1 giây
        self.btn_start.setEnabled(False)

    def update_timer(self):
        self.elapsed += 1
        self.label_timer.setText(f"Đang tu luyện: {self.elapsed} / {self.training_time} giây")

        if self.elapsed >= self.training_time:
            self.timer.stop()
            self.btn_start.setEnabled(True)
            gained_exp = self.training_time  # 1 exp mỗi giây
            self.user_data["exp"] += gained_exp

            # Cập nhật cảnh giới mới nếu có
            new_realm = self.get_realm_by_exp(self.user_data["exp"])
            old_realm = self.user_data["realm"]
            if new_realm != old_realm:
                self.user_data["realm"] = new_realm
                QMessageBox.information(self, "Đột phá!", f"🎉 Bạn đã đột phá cảnh giới!\nTừ: {old_realm}\nĐến: {new_realm}")

            # Lưu lại file JSON
            self.update_user_json()

            self.label_timer.setText("⏳ Chọn thời gian để tiếp tục.")
            QMessageBox.information(self, "Hoàn tất", f"Tu luyện xong!\nBạn nhận được {gained_exp} EXP.")
            self.label_timer.setText("⏳ Chọn thời gian để tiếp tục.")

    def get_realm_by_exp(self, exp):
        if exp < 100:
            return "Trúc Cơ sơ kỳ"
        elif exp < 200:
            return "Trúc Cơ trung kỳ"
        elif exp < 300:
            return "Trúc Cơ hậu kỳ"
        else:
            return "Kim Đan sơ kỳ"

    def update_user_json(self):
        import json, os

        path = os.path.join("data", "users.json")
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except:
                users = []

        # Ghi đè user hiện tại
        for user in users:
            if user["name"] == self.user_data["name"]:
                user.update(self.user_data)
                break

        with open(path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

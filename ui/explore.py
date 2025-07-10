# ui/explore.py
import random
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QTextEdit

class ExploreWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("🗺️ Ra Ngoài Khám Phá")
        self.user_data = user_data

        layout = QVBoxLayout()

        self.label_area = QLabel("🏞️ Chọn khu vực muốn khám phá:")
        self.combo_area = QComboBox()
        self.combo_area.addItems([
            "Thôn Lạc Nhật",
            "Rừng Huyết Vụ",
            "Tàng Thư Các",
            "Hồ Bích Ngọc"
        ])

        self.btn_explore = QPushButton("Khám Phá")
        self.btn_explore.clicked.connect(self.do_explore)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        layout.addWidget(self.label_area)
        layout.addWidget(self.combo_area)
        layout.addWidget(self.btn_explore)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def do_explore(self):
        area = self.combo_area.currentText()
        result = self.generate_event(area)
        self.result_area.setText(result)

    def generate_event(self, area):
        events = [
            "Bạn gặp một lão giả bí ẩn, ông ấy tặng bạn một viên đan dược.",
            "Bạn bị tấn công bởi một yêu thú cấp thấp, nhưng nhanh chóng đánh bại nó.",
            "Bạn nhặt được một pháp bảo rỉ sét dưới bụi cỏ.",
            "Không có chuyện gì xảy ra... nhưng bạn cảm thấy tâm linh được rèn luyện.",
            "Bạn thấy một trận pháp cổ bị phong ấn, nhưng chưa đủ tu vi để giải mã."
        ]
        return f"📍 Khu vực: {area}\n\n🌀 Sự kiện: {random.choice(events)}"

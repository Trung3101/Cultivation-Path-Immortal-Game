# ui/vision.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QTextEdit

class VisionWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle("👁️ Nhìn Xuyên Căn Nguyên")
        self.user_data = user_data

        layout = QVBoxLayout()

        self.label_title = QLabel("🔍 Chọn đối tượng để phân tích:")
        self.combo_target = QComboBox()
        self.combo_target.addItems(["NPC: Linh Nhi", "Pháp bảo: Vô Tự Kiếm", "Công pháp: Băng Tâm Quyết", "Đan dược: Cửu Chuyển Kim Đan", "Trận pháp: Cửu Tinh Liên Tỏa Trận"])
        self.btn_analyze = QPushButton("Phân tích bản chất")
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        layout.addWidget(self.label_title)
        layout.addWidget(self.combo_target)
        layout.addWidget(self.btn_analyze)
        layout.addWidget(self.result_area)

        self.btn_analyze.clicked.connect(self.analyze_target)
        self.setLayout(layout)

    def analyze_target(self):
        target = self.combo_target.currentText()

        if "Linh Nhi" in target:
            result = (
                "🌸 NPC: Linh Nhi\n"
                "- Ngoài thiện, trong ác\n"
                "- Đang tu luyện Huyết Linh Ma Công ngụy trang thành 'Tịnh Tâm Kinh'\n"
                "- Chỉ số: Ngộ tính cao, khí vận mạnh, tâm ma nặng\n"
                "- Gợi ý: Giám sát kỹ, có thể phản đồ nếu trở thành đệ tử"
            )
        elif "Vô Tự Kiếm" in target:
            result = (
                "🗡️ Pháp bảo: Vô Tự Kiếm\n"
                "- Bên ngoài trông tầm thường, bên trong ẩn chứa kiếm ý cổ xưa\n"
                "- Cấp độ: Địa cấp đỉnh phong (có thể tiến hóa)\n"
                "- Phù hợp với người có tâm niệm kiếm đạo vững chắc\n"
                "- Gợi ý: Dùng tâm pháp 'Vô Niệm Kiếm Kinh' để cộng hưởng kiếm ý"
            )
        elif "Băng Tâm Quyết" in target:
            result = (
                "📖 Công pháp: Băng Tâm Quyết\n"
                "- Hệ: Thủy - Âm\n"
                "- Bề ngoài tu tâm tĩnh lặng, nhưng dễ hình thành tuyệt tình tâm cảnh\n"
                "- Người tu lâu dễ trở nên vô cảm với thế giới\n"
                "- Gợi ý: Nên phối hợp 'Dục Hỏa Tâm Kinh' để cân bằng"
            )
        elif "Cửu Chuyển Kim Đan" in target:
            result = (
                "💊 Đan dược: Cửu Chuyển Kim Đan\n"
                "- Tăng tu vi mạnh nhưng có độc ẩn trong đan khí\n"
                "- Nếu dùng quá sớm sẽ gây phản phệ\n"
                "- Gợi ý: Luyện hóa bằng Hỏa Linh Tâm Pháp trước khi dùng"
            )
        elif "Cửu Tinh Liên Tỏa Trận" in target:
            result = (
                "🔺 Trận pháp: Cửu Tinh Liên Tỏa Trận\n"
                "- Trận lực liên kết theo thiên tượng, mạnh mẽ nhưng khó kiểm soát\n"
                "- Nếu trận tâm bất ổn, dễ phản chấn toàn bộ đội hình\n"
                "- Gợi ý: Dùng cùng 'Tĩnh Tâm Huyền Đồ' để ổn định trận lực"
            )
        else:
            result = "Không thể phân tích đối tượng này."

        self.result_area.setText(result)

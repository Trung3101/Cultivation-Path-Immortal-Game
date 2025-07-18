from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from data.constants import ADMIN_PASSWORD

class LoginAdminDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xác thực quản trị")
        self.setFixedSize(300, 120)

        self.label = QLabel("Nhập mật khẩu quản trị:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Xác nhận")
        self.btn_login.clicked.connect(self.check_password)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)

    def check_password(self):
        if self.password_input.text() == ADMIN_PASSWORD:
            self.accept()  # cho phép đóng dialog và báo 'thành công'
        else:
            QMessageBox.warning(self, "Sai mật khẩu", "Bạn không có quyền truy cập.")

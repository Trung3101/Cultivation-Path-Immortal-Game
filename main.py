# main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui.entry_menu import EntryMenu

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = EntryMenu()
    window.show()

    sys.exit(app.exec_())

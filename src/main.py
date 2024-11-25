import sys
from PyQt5.QtWidgets import QApplication
from frontend.gui import ErrorAnalyzerGUI
# import qdarkstyle
# import os
# def load_stylesheet(file_path):
#     """Load and return the content of a QSS file."""
#     with open(file_path, "r") as file:
#         return file.read()
# [print(i) for i in list(sys.modules.keys())]
def main():
    app = QApplication(sys.argv)
    # stylesheet = load_stylesheet("style.qss")
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    gui = ErrorAnalyzerGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
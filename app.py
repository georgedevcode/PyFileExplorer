#https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QMainWindow.html#qmainwindow
import sys
from QComponents.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec()
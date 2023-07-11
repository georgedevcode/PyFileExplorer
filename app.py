#https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QMainWindow.html#qmainwindow
import sys
from PySide6.QtWidgets import QApplication
from QComponents.MainWindow import MainWindow


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec()
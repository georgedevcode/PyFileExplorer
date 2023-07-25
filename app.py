import os
import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic

class PyFileExplorer(QtWidgets.QMainWindow):
        def __init__(self):
            super(PyFileExplorer, self).__init__()
            self.ui_path = os.path.dirname(os.path.abspath(__file__))
            uic.load_ui.loadUi(os.path.join(self.ui_path,"PyFileExplorer.ui"), self)


app = QtWidgets.QApplication(sys.argv)
PyFileExplorer = PyFileExplorer()
PyFileExplorer.show()
sys.exit(app.exec_())
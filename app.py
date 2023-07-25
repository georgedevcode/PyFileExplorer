import os
import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtGui import QFileSystemModel
from pathlib import Path

class PyFileExplorer(QtWidgets.QMainWindow):

        HOME_PATH = Path.home().as_posix()

        def __init__(self):
            super(PyFileExplorer, self).__init__()
            self.ui_path = os.path.dirname(os.path.abspath(__file__))
            uic.load_ui.loadUi(os.path.join(self.ui_path,"PyFileExplorer.ui"), self)
            self.FilesTreeView = self.findChild(QtWidgets.QTreeView, "FilesTreeView")
            self.SearchButton = self.findChild(QtWidgets.QPushButton, "SearchButton")
            self.FileViewWidget = self.findChild(QtWidgets.QListView, "FileViewWidget")
            self.SearchFileWidget = self.findChild(QtWidgets.QLineEdit, "SearchFileWidget")

            # Setting up the File View Tree
            self.model = QFileSystemModel()
            self.model.setRootPath(self.HOME_PATH)
            self.FilesTreeView.setModel(self.model)
            self.FilesTreeView.setRootIndex(self.model.index(self.HOME_PATH))
            self.FilesTreeView.setColumnWidth(0, 250)
            self.FilesTreeView.setAlternatingRowColors(True)
            

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PyFileExplorer = PyFileExplorer()
    PyFileExplorer.show()
    app.exec()
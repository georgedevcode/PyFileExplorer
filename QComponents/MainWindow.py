from PySide6.QtWidgets import (QMainWindow, QMenu, QlineEdit)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyExplorer")
        self.setFixedSize(1024, 800)

        #Menu
        menuBar = self.menuBar()
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help") 

        self.searchBar = QlineEdit()
        

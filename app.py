import os
import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QFileSystemModel, QMouseEvent, QDesktopServices, QPointingDevice
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QListView, QMessageBox
from PyQt6.QtCore import QDir, QModelIndex
from PyQt6.QtGui import QDesktopServices

class PyFileExplorer(QtWidgets.QMainWindow):

        HOME_PATH = Path.home().as_posix()
        # Field to keep track on the previous index
        PREV_INDEX_FILE_VIEW = HOME_PATH
        

        def __init__(self):
            super(PyFileExplorer, self).__init__()
            self.ui_path = os.path.dirname(os.path.abspath(__file__))
            uic.load_ui.loadUi(os.path.join(self.ui_path,"PyFileExplorer.ui"), self)
            self.FilesTreeView = self.findChild(QtWidgets.QTreeView, "FilesTreeView")
            self.SearchButton = self.findChild(QtWidgets.QPushButton, "SearchButton")
            self.FileViewWidget = self.findChild(QtWidgets.QListView, "FileViewWidget")
            self.SearchFileWidget = self.findChild(QtWidgets.QLineEdit, "SearchFileWidget")
            self.HomeButton = self.findChild(QtWidgets.QPushButton, "HomeButton")
            self.ReturnButton = self.findChild(QtWidgets.QPushButton, "ReturnButton")
            self.MenuBar = self.findChild(QtWidgets.QMenuBar, "menubar")
            self.MenuFile = self.MenuBar.findChild(QtWidgets.QMenu, "menuFile")

            # Setting up the File View Tree
            self.model = QFileSystemModel()
            self.model.setRootPath(self.HOME_PATH)
            self.FilesTreeView.setModel(self.model)
            self.FilesTreeView.setRootIndex(self.model.index(self.HOME_PATH))
            self.FilesTreeView.setColumnWidth(0, 250)
            self.FilesTreeView.setAlternatingRowColors(True)
            self.FilesTreeView.doubleClicked.connect(self.MouseDoubleClickOpenFileFolders)

            # Setting up the File View tree
            self.FileViewWidget.setModel(self.model)
            self.FileViewWidget.setRootIndex(self.model.index(self.HOME_PATH))
            self.FileViewWidget.setViewMode(self.FileViewWidget.ViewMode.IconMode)
            self.FileViewWidget.setResizeMode(self.FileViewWidget.ResizeMode.Adjust)
            self.FileViewWidget.setMovement(self.FileViewWidget.Movement.Free)

            # Setting up the File menu options
            self.CreateFolderMenuAction = self.MenuFile.addAction("Crear Carpeta")
            self.PlainFileMenuAction = self.MenuFile.addAction("Crear Archivo Plano")
            self.ModifyPlainFileMenuAction = self.MenuFile.addAction("Modificar Archivo Plano")
            self.DeletePlainFileMenuAction = self.MenuFile.addAction("Eliminar Archivo Plano")
            self.EncryptionPlainFileMenuAction = self.MenuFile.addAction("Encriptar Archivo Plano")
            self.DecryptionPlainFileMenuAction = self.MenuFile.addAction("Desencriptar Archivo Plano")
            self.SeeFilesInvetoryMenuAction = self.MenuFile.addAction("Ver inventario de archivos")
           
            #slots
            self.HomeButton.clicked.connect(self.HomeButtonClickEvent)
            self.FileViewWidget.doubleClicked.connect(self.MouseDoubleClickOpenFileFolders)
            self.PlainFileMenuAction.triggered.connect(self.CreatePlainTextFile)
            self.CreateFolderMenuAction.triggered.connect(self.CreateFolder)
            self.ModifyPlainFileMenuAction.triggered.connect(self.ModifyPlainTextFile)
            self.DeletePlainFileMenuAction.triggered.connect(self.DeleteFile)
            self.EncryptionPlainFileMenuAction.triggered.connect(self.EncryptPlainTextFile)
            self.DecryptionPlainFileMenuAction.triggered.connect(self.DecryptPlainTextFile)
            self.SeeFilesInvetoryMenuAction.triggered.connect(self.SeeFilesInvetory)

            
        def MouseDoubleClickOpenFileFolders(self, index):
                file_info = self.model.fileInfo(index)
                if file_info.isDir():
                    # If it's a folder, open it
                    folder_path = file_info.absoluteFilePath()
                    self.model.setRootPath(folder_path)
                    self.FileViewWidget.setRootIndex(self.model.index(folder_path))
                else:
                    # If it's a file, open it with the default application
                    file_path = file_info.filePath()
                    QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        
        def HomeButtonClickEvent(self):
             self.model.setRootPath(self.HOME_PATH)
             self.FileViewWidget.setRootIndex(self.model.index(self.HOME_PATH))
        
        def CreatePlainTextFile(self):
             print("File created")

        def CreateFolder(self):
             print("Folder created")
        
        def ModifyPlainTextFile(self):
             print("File Modified")

        def DeleteFile(self):
             print("File Deleted")
        
        def EncryptPlainTextFile(self):
             print("File Encrypted")
        
        def DecryptPlainTextFile(self):
             print("File Decrypted")
        
        def SeeFilesInvetory(self):
             print("Showing Files Invetory")
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PyFileExplorer = PyFileExplorer()
    PyFileExplorer.show()
    app.exec()
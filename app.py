import os
import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QEvent
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFileSystemModel, QMouseEvent, QDesktopServices, QPointingDevice
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QListView, QMessageBox, QMenu, QInputDialog
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
            self.SearchButton.clicked.connect(self.SearchButtonClickEvent)
                        
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

        def mousePressEvent(self, event):
            if event.button() == Qt.RightButton:
                # Mostrar el menú en la posición del cursor
                self.menu.exec_(event.globalPos())
            
        def create_file(self, filename):
            current_path = self.model.rootPath()
            file_path = os.path.join(current_path, filename)
    
            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    pass  
            
                self.model.refresh(self.model.index(current_path))
        
        def file_exists(self, filename):
            current_path = self.model.rootPath()
            file_path = os.path.join(current_path, filename)
            return os.path.exists(file_path)

        def modify_file(self, filename):
            if not self.file_exists(filename):
                QMessageBox.warning(self, 'Archivo no encontrado', f'El archivo "{filename}" no existe en este directorio.')
            return
    
            current_path = self.model.rootPath()
            file_path = os.path.join(current_path, filename)

            self.model.refresh(self.model.index(current_path))

        def delete_file(self, filename):
            current_path = self.model.rootPath()
            file_path = os.path.join(current_path, filename)
    
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    # Refresca la vista para reflejar los cambios
                    self.model.refresh(self.model.index(current_path))
                except OSError as e:
                    QMessageBox.critical(self, 'Error al Eliminar', f"No se pudo eliminar el archivo '{filename}': {e}")
            else:
                    QMessageBox.warning(self, 'Archivo no Encontrado', f"El archivo '{filename}' no existe.")

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
            filename, ok = QInputDialog.getText(self, 'Crear Archivo', 'Ingrese el nombre del archivo:')
            if ok and filename:
                self.create_file(filename)

        def CreateFolder(self):
             print("Folder created")
        
        def ModifyPlainTextFile(self):
            print("File Modified")
            filename, ok = QInputDialog.getText(self, 'Modificar Archivo', 'Ingrese el nombre del archivo a modificar:')
            if ok and filename:
                self.modify_file(filename)

        def DeleteFile(self):
            print("File Deleted")
            filename, ok = QInputDialog.getText(self, 'Eliminar Archivo', 'Ingrese el nombre del archivo a eliminar:')
            if ok and filename:
                self.delete_file(filename)
        
        def EncryptPlainTextFile(self):
             print("File Encrypted")
        
        def DecryptPlainTextFile(self):
             print("File Decrypted")
        
        def SeeFilesInvetory(self):
             print("Showing Files Invetory")
        

        def SearchButtonClickEvent(self):
            search_text = self.SearchFileWidget.text()
            if search_text:
               current_path = self.model.rootPath()
               self.model.setNameFilters([f"*{search_text}*"])
               self.model.setRootPath(current_path)
               self.FileViewWidget.setRootIndex(self.model.index(current_path))

               # Hide non-matching files
               for row in range(self.model.rowCount(self.FileViewWidget.rootIndex())):
                   index = self.model.index(row, 0, self.FileViewWidget.rootIndex())
                   file_info = self.model.fileInfo(index)
                   if not file_info.fileName().lower().startswith(search_text.lower()):
                      self.FileViewWidget.setRowHidden(row, True)
                   else:
                      self.FileViewWidget.setRowHidden(row, False)
            else:
                 current_path = self.model.rootPath()
                 self.model.setNameFilters([])
                 self.model.setRootPath(current_path)
                 self.FileViewWidget.setRootIndex(self.model.index(current_path))
                 for row in range(self.model.rowCount(self.FileViewWidget.rootIndex())):
                     self.FileViewWidget.setRowHidden(row, self.FileViewWidget.rootIndex(), False)      

                     #Falta corregir la búsqueda de documentos dentro de carpetas   

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PyFileExplorer = PyFileExplorer()
    PyFileExplorer.show()
    app.exec()
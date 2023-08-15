import os
import sys
import shutil
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QUrl, QFileInfo
from PyQt6.QtCore import QEvent
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFileSystemModel, QMouseEvent, QDesktopServices, QPointingDevice
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QListView, QMessageBox, QMenu, QInputDialog
from PyQt6.QtCore import QDir, QModelIndex
from PyQt6.QtGui import QDesktopServices
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from QComponents.ModifyPlainText import ModifyPlainTextWindow

class PyFileExplorer(QtWidgets.QMainWindow):
        # User home directory on the system
        HOME_PATH = Path.home().as_posix()
        # Field to keep track on the previous index
        PREV_INDEX_FILE_VIEW = HOME_PATH
        #Fernet Object containing the Fernet key
        FERNET = None

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
            self.DeleteFolderMenuAction = self.MenuFile.addAction("Eliminar Carpeta")
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
            self.DeleteFolderMenuAction.triggered.connect(self.DeleteFolder)
            self.ModifyPlainFileMenuAction.triggered.connect(self.ModifyPlainTextFile)
            self.DeletePlainFileMenuAction.triggered.connect(self.DeleteFile)
            self.EncryptionPlainFileMenuAction.triggered.connect(self.EncryptPlainTextFile)
            self.DecryptionPlainFileMenuAction.triggered.connect(self.DecryptPlainTextFile)
            self.SeeFilesInvetoryMenuAction.triggered.connect(self.SeeFilesInvetory)
            
        def create_file(self, filename):
            current_path = self.model.rootPath()
            file_path = os.path.join(current_path, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    self.SaveFileOnInventory(file_path)
                    pass  
                self.model.layoutChanged.emit()

        def create_folder(self, foldername):
            current_path = self.model.rootPath()
            folder_path = os.path.join(current_path, foldername)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            else:
                QMessageBox.warning(self, "Advertencia", "El folder ya existe")
            self.model.layoutChanged.emit()
        
        def delete_folder(self, foldername):
            current_path = self.model.rootPath()
            folder_path = os.path.join(current_path, foldername)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            else:
                QMessageBox.warning(self, f"El folder no existe")
            self.model.layoutChanged.emit()

        def file_exists(self, filename):
            current_path = self.model.rootPath()
            file_path = os.path.join(current_path, filename)
            return os.path.exists(file_path)

        def modify_file(self, filename):
            current_path = self.model.rootPath()
            if not self.file_exists(filename):
                QMessageBox.warning(self, "Advertencia", 'Archivo no encontrado', 'El archivo no existe en este directorio.')
            else:
                modify_window  = ModifyPlainTextWindow(current_path, filename)
                modify_window.exec()


        def delete_file(self, filename):
            current_path = self.model.rootPath()
            file_path = os.path.join(current_path, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    # Refresca la vista para reflejar los cambios
                    self.model.layoutChanged.emit()
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
            filename, ok = QInputDialog.getText(self, 'Crear Archivo', 'Ingrese el nombre del archivo:')
            if ok and filename:
                self.create_file(filename)

        def CreateFolder(self):
            foldername, ok = QInputDialog.getText(self, 'Crear Folder', 'Ingrese el nombre del folder:')
            if ok and foldername:
                self.create_folder(foldername)

        def DeleteFolder(self):
            foldername, ok = QInputDialog.getText(self, 'Borrar Folder', 'Ingrese el nombre del folder:')
            if ok and foldername:
                self.delete_folder(foldername)
        
        def ModifyPlainTextFile(self):
            filename, ok = QInputDialog.getText(self, 'Modificar Archivo', 'Ingrese el nombre del archivo a modificar:')
            if ok and filename:
                self.modify_file(filename)

        def DeleteFile(self):
            filename, ok = QInputDialog.getText(self, 'Eliminar Archivo', 'Ingrese el nombre del archivo a eliminar:')
            if ok and filename:
                self.delete_file(filename)

        # Initialzing the Fernet key
        # This is needed in order to encrypt and decrypt the data
        def InitializeFernet(self):
            path = os.getcwd()
            file_key = "FernetKey.txt"
            key_path = os.path.join(path,file_key)

            b_file_exists = os.path.exists(key_path)
            
            #File exists on directory
            if b_file_exists:
                #File is not empty
                b_file_empty = os.stat(key_path).st_size != 0
                if b_file_empty:
                    #Let's read the file and retrive the fernet key
                    with open(key_path, "r") as file:
                        key = file.read()
                        key = key.encode()
            else:
                #If there is not a file holding the key, then let's create the file and generate the fernet key
                with open(key_path, "w") as file:
                    key = Fernet.generate_key()
                    file.write(key.decode("utf-8"))
            self.FERNET = Fernet(key)
            return self.FERNET
        
        def EncryptPlainTextFile(self):
            filename, ok = QInputDialog.getText(self, 'Eliminar Archivo', 'Ingrese el nombre del archivo a eliminar:')
            if ok and filename:
                path = self.model.rootPath()
                full_file_path = os.path.join(path, filename)

                with open(full_file_path, 'rb') as file:
                    original_file = file.read()
                
                encrypted = self.FERNET.encrypt(original_file)

                with open(full_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted)
                    file.close()

        def DecryptPlainTextFile(self):
            filename, ok = QInputDialog.getText(self, 'Eliminar Archivo', 'Ingrese el nombre del archivo a eliminar:')
            if ok and filename:
                path = self.model.rootPath()
                full_file_path = os.path.join(path, filename)

                with open(full_file_path, 'rb') as file:
                    original_file = file.read()
                
                decrypted = self.FERNET.decrypt(original_file)

                with open(full_file_path, 'wb') as dec_file:
                    dec_file.write(decrypted )
                    file.close()
        
        def SeeFilesInvetory(self):
             print("Showing Files Invetory")
        
        def SaveFileOnInventory(self, filepath):
            print("Saving File On Inventory")
            file_info = QFileInfo(filepath)
            file_name = file_info.fileName()
            file_dir = file_info.filePath()
            file_create_day = file_info.birthTime().toString(format=Qt.DateFormat.TextDate)
            last_day_modified = file_info.lastModified().toString(format=Qt.DateFormat.TextDate)

            with open("registro_documentos.txt", "a") as file:
                        file.write(f"Nombre Archivo: {file_name}\n")
                        file.write(f"Directorio: {file_dir}\n")
                        file.write(f"Creado en: {file_create_day}\n")
                        file.write(f"Ultima modificaion: {last_day_modified}")
                        file.write("\n================================\n")
                        file.close()

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
    PyFileExplorer.InitializeFernet()
    PyFileExplorer.show()
    app.exec()
import os
import sys
import traceback
import asyncio
from PyQt6 import QtCore, QtGui, QtWidgets, uic

class ModifyPlainTextWindow(QtWidgets.QDialog):
    def __init__(self, path, filename):                
        super(ModifyPlainTextWindow,self).__init__()                        
        self.path = path
        self.filename = filename
        self.ui_path = os.path.dirname(os.path.abspath(__file__))               
        uic.load_ui.loadUi(os.path.join(self.ui_path, "form.ui"),self)        
        self.textEscribir = self.findChild(QtWidgets.QPlainTextEdit,"TxtEscribir")
        self.btnEscribir = self.findChild(QtWidgets.QPushButton,"BtnCrear")
        self.textLeer = self.findChild(QtWidgets.QPlainTextEdit,"TxtLeer")
        self.btnLeer = self.findChild(QtWidgets.QPushButton,"BtnLeer")
        self.btnEscribir.clicked.connect(self.mensajeEmergente)
        self.btnLeer.clicked.connect(self.LecturaArchivo)  
        self.VentanaEmergente = None      

        
    def mensajeEmergente(self):        
        msg = QtWidgets.QMessageBox(self)  
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
        msg.setText("Desea escrbir en el archivo?")        
        msg.setWindowTitle("Validacion de escritura")        
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)        
        a = msg.exec()  
        if (a == QtWidgets.QMessageBox.StandardButton.Yes):
            self.EscribirFile()            
        else:
            pass 
        
    def EscribirFile(self):
        try:
            
            archivo = open(os.path.join(self.path, self.filename),'a') #append       
            archivo.write(self.textEscribir.toPlainText()+"\r")
            archivo.close()
            self.textEscribir.clear()
            
        except OSError as oE:
            archivo.close()
            print(oE.strerror)
        except BaseException:
            print(traceback.format_exc())
            archivo.close()
    
    def LecturaArchivo(self):
        try:
            archivo = open(os.path.join(self.path, self.filename),'r')        
            texto = archivo.read()                        
            self.textLeer.setPlainText(texto)
            archivo.close()
            #print(archivo.read()) 
        except OSError as oE:
            archivo.close()
            print(oE.strerror)
        except BaseException:
            archivo.close()   
        


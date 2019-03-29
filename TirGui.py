# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 14:32:54 2018
Control tir laview 
@author: loa
"""
from PyQt5 import QtCore,uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QMessageBox,QShortcut
import time
import sys
import tirSalleJaune as tirSJ
import moteurRSAI as RSAI  # Moteur RSAI
PY = sys.version_info[0]
if PY<3:
    print('wrong version of python : Python 3.X must be used')
#%%
class TIRGUI(QWidget) :
    """
    User interface for shooting class : 
    
    """
    
    def __init__(self,parent=None):
        
        super(TIRGUI, self).__init__(parent=None)
#        print('motor name:',self.motor)
#        print('motor type:',motorTypeName)
        self.isWinOpen=False
        guiName='Tir.ui'
        self.win=uic.loadUi(guiName,self)
        self.win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.configPath="C:/Users/loa/Desktop/MoteursV7/fichiersConfig/"
        self.confRSAI=QtCore.QSettings(self.configPath+'configMoteurRSAI.ini', QtCore.QSettings.IniFormat)
        self.setup()
        
        self.threadCibleVert=PositionThread(mot='Cible_Trans_Vert',motorType='RSAI') # thread pour afficher position Spectro
        self.threadCibleVert.POS.connect(self.POSITIONVert)
        time.sleep(0.1)
        self.threadCibleVert.start()
        self.PositionCibleLat=0
        self.PositionCibleVert=0
        self.PositionCibleFoc=0
        self.PositionSampleLat=0
        self.PositionSampleVert=0
        self.threadCibleLat=PositionThread(mot='Cible_Trans_Lat',motorType='RSAI') # thread pour afficher position Spectro
        self.threadCibleLat.POS.connect(self.POSITIONLat)
        time.sleep(0.1)
        self.threadCibleLat.start()

        self.threadSampleVert=PositionThread(mot='sample_Vert',motorType='RSAI') # thread pour afficher position Spectro
        self.threadSampleVert.POS.connect(self.POSITIONSampleVert)
        time.sleep(0.1)
        self.threadSampleVert.start()
        
        self.threadSampleLat=PositionThread(mot='sample_Lat',motorType='RSAI') # thread pour afficher position Spectro
        self.threadSampleLat.POS.connect(self.POSITIONSampleLat)
        time.sleep(0.1)
        self.threadSampleLat.start()



    def startThread2(self):
        self.win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.threadCibleLat.ThreadINIT()
        self.threadCibleLat.start()
        time.sleep(0.1)
        self.threadCibleVert.ThreadINIT()
        self.threadCibleVert.start()
        
        self.threadSampleVert.ThreadINIT()
        self.threadSampleVert.start()
        time.sleep(0.1)
        self.threadSampleLat.ThreadINIT()
        self.threadSampleLat.start()
        
        
    def POSITIONLat(self,Posi):
        self.PositionCibleLat=Posi
               
    def POSITIONVert(self,Posi):
        self.PositionCibleVert=Posi
    
    def POSITIONSampleLat(self,Posi):
        self.PositionSampleLat=Posi
               
    def POSITIONSampleVert(self,Posi):
        self.PositionSampleVert=Posi
    
    def setup(self):
        self.setWindowTitle('Tir Salle Jaune')# affichage nom du moteur sur la barre de la fenetre
        self.connectButton.clicked.connect(self.Connect)
        self.disconnectButton.clicked.connect(self.Disconnect)
        self.tirButton.clicked.connect(self.TirAct)
        self.shortcut = QShortcut(QKeySequence("Ctrl+t"), self)
        self.shortcut.activated.connect(self.TirAct)
        
    def closeEvent(self, event):
        """ when closing the window
        """
        self.fini()
        time.sleep(0.1)
        event.accept()   
        
    def fini(self): # a la fermeture de la fenetre on arrete le thread secondaire
        self.isWinOpen=False
        time.sleep(0.1)     
        self.threadCibleLat.stopThread()
        self.threadCibleVert.stopThread()
        self.threadSampleLat.stopThread()
        self.threadSampleVert.stopThread()
        
    def Connect(self):
        a=tirSJ.tirConnect()
        print (a)
        if a==1:
            self.connectButton.setStyleSheet("background-color: rgb(0, 170, 0)")
            self.connectButton.setText("Connected")
            self.TirConnected=1
            
        else :
            self.connectButton.setStyleSheet("background-color: rgb(180,180,180)")
            self.connectButton.setText("Connection")
            self.TirConnected=0

    def Disconnect(self):
    	tirSJ.disconnect()
    	self.connectButton.setStyleSheet("background-color: rgb(180,180,180)")
    	self.connectButton.setText("Connection")
    	self.TirConnected=0
    
    def TirAct(self):
        conf=self.confRSAI
        ref5LAT=float(conf.value('Cible_Trans_Lat'+"/ref5Pos"))
        ref5VERT=float(conf.value('Cible_Trans_Lat'+"/ref5Pos"))
        refPixelLat=float(conf.value('sample_Lat'+"/ref2Pos"))
        refPixelVert=float(conf.value('sample_Vert'+"/ref2Pos"))
        print (refPixelLat,refPixelVert,self.PositionSampleLat,self.PositionSampleVert)
        
        if (refPixelLat-10<self.PositionSampleLat<refPixelLat+10) or  refPixelVert-10<self.PositionSampleVert<refPixelVert+10:
            
            print('PixelLink en place!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Shooting not allowed !")
            msg.setInformativeText("PixelLink IN POSITION !")
            msg.setWindowTitle("Warning ...")
            msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msg.exec_()
        
        if (ref5LAT-200<self.PositionCibleLat<ref5LAT+200) or  ref5VERT-200<self.PositionCibleVert<ref5VERT+200:
            print('Microscope en place!')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Shooting not allowed !")
            msg.setInformativeText("MICROSCOPE IN POSITION !")
            msg.setWindowTitle("Warning ...")
            msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msg.exec_()
        else:
            
                
            a=tirSJ.Tir()
            self.win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            print( "tir :",a)
            if a==0 or a=="":
                self.TirConnected=0
                print( "Probleme tir")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Not connected !")
                msg.setInformativeText("Please connect !!")
                msg.setWindowTitle("Warning ...")
                msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                msg.exec_()


#%%#################################################################################       
class PositionThread(QtCore.QThread):
    '''
    thread secondaire pour afficher la position
    '''
    import time #?
    POS=QtCore.pyqtSignal(float) # signal transmit par le second thread au thread principal pour aff la position
    def __init__(self,parent=None,mot='',motorType=''):
        super(PositionThread,self).__init__(parent)
        self.MOT=mot
        self.motorType=motorType
        if self.motorType=='SmartAct':
            self.MOT=SMART.MOTORSMART(mot)
        if self.motorType=='RSAI':
            self.MOT=RSAI.MOTORRSAI(mot)
        if self.motorType=='A2V':
            self.MOT=A2V.MOTORA2V(mot)
        self.stop=False
        
    def run(self):
        while True:
            if self.stop==True:
                break
            else:
                
                Posi=(self.MOT.position())
                time.sleep(1)
                try :
                    self.POS.emit(Posi)
                    
                    time.sleep(0.5)
                except:
                    print('error emit')
                    
    def ThreadINIT(self):
        self.stop=False     
                       
    def stopThread(self):
        self.stop=True
        time.sleep(0.1)
        self.terminate()
        
#%%#####################################################################



   
if __name__ =='__main__':
    appli=QApplication(sys.argv)
    tt=TIRGUI()
    tt.startThread2()
    tt.show()
    appli.exec_()
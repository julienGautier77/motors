#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:49:41 2019

@author: juliengautier
"""


#%%Import
from PyQt5 import QtCore,uic
from PyQt5.QtWidgets import QApplication,QStyle
from PyQt5.QtWidgets import QWidget,QMessageBox,QSpinBox,QLineEdit,QFrame
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QWidget,QPushButton,QGridLayout,QTextEdit,QDoubleSpinBox
from PyQt5.QtWidgets import QInputDialog,QComboBox,QSlider,QCheckBox,QLabel,QSizePolicy,QLineEdit,QPlainTextEdit,QMessageBox,QMenu
from pyqtgraph.Qt import QtCore,QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut,QStyleOption
import sys,time,os
import qdarkstyle


class ONEMOTOR(QWidget) :

    def __init__(self, mot0='',motorTypeName0='',nomWin=''):
                 
        super(ONEMOTOR, self).__init__()
        
        self.motor=str(mot0)
        self.isWinOpen=False
        self.motorTypeName=motorTypeName0

        self.configPath="./fichiersConfig/"
        self.isWinOpen=False
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setup()
        self.setWindowTitle(nomWin)
        
        if self.motorTypeName=='RSAI':
            configMotName='configMoteurRSAI.ini'
            import moteurRSAI as RSAI
            self.motorType=RSAI
            self.MOT=self.motorType.MOTORRSAI(self.motor)
            
        elif self.motorTypeName=='SmartAct':
             configMotName='configMoteurSmartAct.ini'
             import smartactmot as SmartAct
             self.motorType=SmartAct
             self.MOT=self.motorType.MOTORSMART(self.motor)
             
        elif self.motorTypeName=='A2V':
             configMotName='configMoteurA2V.ini'
             import moteurA2V  as A2V
             self.motorType=A2V
             self.MOT=self.motorType.MOTORA2V(self.motor)
             
        elif self.motorTypeName=='NewFocus':
             configMotName='configMoteurNewFocus.ini'
             import moteurNewFocus as NewFoc
             self.motorType=NewFoc
             self.MOT=self.motorType.MOTORNEWFOCUS(self.motor)
             
        elif self.motorTypeName=='newport':
             configMotName='confNewport.ini'
             import newportMotors as Newport
             self.motorType=Newport
             self.MOT=self.motorType.MOTORNEWPORT(self.motor)
             
        elif self.motorTypeName=='Servo':
             configMotName='configMoteurServo.ini'
             import servo as servo
             self.motorType=servo
             self.MOT=self.motorType.MOTORSERVO(self.motor)
             
        elif self.motorTypeName=='Arduino':
             configMotName='configMoteurArduino.ini'
             import moteurArduino as arduino
             self.motorType=arduino
             self.MOT=self.motorType.MOTORARDUINO(self.motor)
             
        else:
            print('Error config motor Type name')
            
        configMotName=self.configPath+ configMotName  
        print('conf:',configMotName)
        self.conf=QtCore.QSettings(configMotName, QtCore.QSettings.IniFormat) # fichier config motor fichier .ini
        
        
        
        self.stepmotor=float(self.conf.value(self.motor+"/stepmotor"))
        self.butePos=float(self.conf.value(self.motor+"/buteePos"))
        self.buteNeg=float(self.conf.value(self.motor+"/buteeneg"))
        print(self.stepmotor)
        self.thread2=PositionThread(mot=self.MOT,motorType=self.motorType) # thread pour afficher position
        self.thread2.POS.connect(self.Position)
        self.actionButton()
        self.unitF()
        
    def startThread2(self):
        self.thread2.ThreadINIT()
        self.thread2.start()
        
    def setup(self):
        print('setup')
        vbox1=QVBoxLayout()
        hbox1=QHBoxLayout()
        pos=QLabel('Pos:')
        pos.setMaximumHeight(20)
        
        self.position=QLabel('1234567')
        self.position.setMaximumHeight(20)
        self.unitButton=QComboBox()
        self.unitButton.addItem('Step')
        self.unitButton.addItem('um')
        self.unitButton.addItem('mm')
        self.unitButton.addItem('ps')
        self.unitButton.setMinimumWidth(80)
        
        self.zeroButton=QPushButton('Zero')
        
        hbox1.addWidget(pos)
        hbox1.addWidget(self.position)
        hbox1.addWidget(self.unitButton)
        hbox1.addWidget(self.zeroButton)
        vbox1.addLayout(hbox1)
        
        
        hbox2=QHBoxLayout()
        self.moins=QPushButton(' - ')
        self.moins.setMinimumWidth(60)
        self.moins.setMinimumHeight(60)
        hbox2.addWidget(self.moins)
        self.jogStep=QDoubleSpinBox()
        self.jogStep.setMaximum(10000)
        hbox2.addWidget(self.jogStep)
         
        
        self.plus=QPushButton(' + ')
        self.plus.setMinimumWidth(60)
        self.plus.setMinimumHeight(60)
    
        hbox2.addWidget(self.plus)
        vbox1.addLayout(hbox2)
        
        self.setLayout(vbox1)
        
        
    def actionButton(self):
        self.plus.clicked.connect(self.pMove) # jog +
        self.plus.setAutoRepeat(True)
        self.moins.clicked.connect(self.mMove)# jog -
        self.moins.setAutoRepeat(True) 
        self.zeroButton.clicked.connect(self.Zero)
        #self.stopButton.clicked.connect(self.StopMot)
        self.unitButton.currentIndexChanged.connect(self.unitF)
         
    def pMove(self):# action jog +
        print('jog+')
        a=float(self.jogStep.value())
        print(a)
        a=float(a*self.unitChange)
        b=self.MOT.position()
        if b+a<self.buteNeg :
            print( "STOP : Butée Positive")
            self.MOT.stopMotor()
        elif b+a>self.butePos :
            print( "STOP : Butée Négative")
            self.MOT.stopMotor()
        else :
            self.MOT.rmove(a)



    def mMove(self): # action jog -
        a=float(self.jogStep.value())
        a=float(a*self.unitChange)
        b=self.MOT.position()
        if b-a<self.buteNeg :
            print( "STOP : Butée Positive")
            self.MOT.stopMotor()
        elif b-a>self.butePos :
            print( "STOP : Butée Négative")
            self.MOT.stopMotor()
        else :
            self.MOT.rmove(-a)
     
    def Zero(self): # remet le compteur a zero 
        self.MOT.setzero()    
        
    def unitF(self): # chg d'unité
        ii=self.unitButton.currentIndex()
        if ii==0: #  step
            self.unitChange=1
        if ii==1: # micron
            self.unitChange=float((1*self.stepmotor))  
        if ii==2: #  mm 
            self.unitChange=float((1000*self.stepmotor))
        if ii==3: #  ps  double passage : 1 microns=6fs
            self.unitChange=float(1*self.stepmotor/0.0066666666)    
        if self.unitChange==0:
            self.unitChange=1 #avoid 0 
    
    def StopMot(self): # stop le moteur
       self.MOT.stopMotor();

    def Position(self,Posi): # affichage de la position a l aide du second thread
        
        a=float(Posi)
        b=a # valeur en pas moteur pour sauvegarder en pas 
        a=round(a/self.unitChange,3) # valeur tenant compte du changement d'unite
        self.position.setText(str(a)) 
    
    def closeEvent(self, event):
        """ 
        When closing the window
        """
        self.fini()
        time.sleep(0.1)
        event.accept() 
        
    def fini(self): # a la fermeture de la fenetre on arrete le thread secondaire
        self.thread2.stopThread()
        self.isWinOpen=False
        time.sleep(0.1)      
        

#%%#################################################################################       
class PositionThread(QtCore.QThread):
    ### thread secondaire pour afficher la position
    import time #?
    POS=QtCore.pyqtSignal(float) # signal transmit par le second thread au thread principal pour aff la position
    def __init__(self,parent=None,mot='',motorType=''):
        super(PositionThread,self).__init__(parent)
        self.MOT=mot
        self.motorType=motorType
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
                    
                    time.sleep(0.1)
                except:
                    print('error emit')
                    
    def ThreadINIT(self):
        self.stop=False    
                         
    def stopThread(self):
        self.stop=True
        time.sleep(0.1)
        self.terminate()


        
if __name__ =='__main__':
    motor0="topview"
    motorType="Arduino"
    appli=QApplication(sys.argv)
    mot5=ONEMOTOR(mot0=motor0,motorTypeName0=motorType,nomWin='motorTopview')
    mot5.show()
    mot5.startThread2()
    appli.exec_()        
        

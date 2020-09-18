#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 13:41:34 2020
Pololu servo controlller 
use servo.py 
serial port defined in servo.py

@author: juliengautier
"""

import servo
from PyQt5 import QtCore

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout,QVBoxLayout
from PyQt5.QtGui import QIcon

import pathlib,os
import qdarkstyle
import time

class SERVOWIN(QWidget):
    
    
    def __init__(self,title='Density Control',configFile='configMoteurServo.ini'):
        
            super(SERVOWIN, self).__init__() 
            
            p = pathlib.Path(__file__)
            sepa=os.sep
            self.icon=str(p.parent) + sepa + 'icons' +sepa
            self.setWindowTitle(title)
            self.setWindowIcon(QIcon(self.icon+'LOA.png'))
            
            self.configPath=str(p.parent / "fichiersConfig")+sepa
            self.configMotName=self.configPath+configFile
            self.conf=QtCore.QSettings(self.configMotName, QtCore.QSettings.IniFormat)   
            self.groups=self.conf.childGroups() # lecture de tous les moteurs
            print('servo in ini   file : ',self.configMotName)
            print(self.groups)
            
            self.motorListButton=list()
            self.motorListGui=list()
            
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            grid = QGridLayout()
            vbox1=QVBoxLayout() 
            print('Please wait ...')
        
            for vi in self.groups:
                #print(vi)
                # creation des boutons avec le nom
                self.motorListButton.append(QPushButton(self.conf.value(vi+"/Name"),self))  
                # creation de widget oneMotorGui pour chaque moteurs
                self.motorListGui.append(servo.MOTORSERVO(mot=str(vi),motorTypeName='RSAI'))
                
            #creation des d'une matrice de point pour creer une grille    
            z=0
            self.nbOfMotor=len(self.motorListButton)
            for i in range(0,int(self.nbOfMotor/2)):
                for j in range(0,int(self.nbOfMotor/2)):
                    if z<self.nbOfMotor:
                        grid.addWidget(self.motorListButton[z], j, i)
                    z+=1
                
            j = 0
            for mm in self.motorListButton:
                # #ajout de chaque boutton dans la grille
                # grid.addWidget(self.motorListButton[j], gridPos[j][0], gridPos[j][1])
                
                #action de chaque bouton : open a new widget for onemotor control
                mm.clicked.connect(lambda checked, j=j:self.open_widget(self.motorListGui[j]))
                j+=1
            
            # ajout de la grille de bouton au widget proncipal
            vbox1.addLayout(grid)
            if self.shoot==True: # to add shoot button in salle Jaune
                self.tirWidget=TIRGUI()
                vbox1.addWidget(self.tirWidget)
                
            self.setLayout(vbox1)   
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    
    def open_widget(self,fene):
        """ ouverture widget suplementaire 
        """

        if fene.isWinOpen==False:
            fene.setup
            fene.isWinOpen=True
            
            fene.show()
        else:
            fene.activateWindow()
            fene.raise_()
            fene.showNormal()

    def closeEvent(self,event):
        print('close...')
        event.accept() 
            

    def iniPolulu(self):
            """
            initialisation des polulu
            """
            self.Centreur=[]      
            self.Polulu=[]
            print("polulu intialisation..." )
            for i in range(0,12) :
                self.Polulu.append(servo.MOTORSERVO('Servo'+str(i)))
                self.Polulu[i].goPositionIN()
                self.Polulu[i].setPosition(self.Polulu[i].posIN)
                time.sleep(0.2)
                self.Centreur.append(self.win.findChildren(QPushButton, "centreur" +str(i)))
                
            for i in  [0,1,2,3,4,5,6,8,9]: #♥ il manque le centreur 7
                self.Centreur[i][0].setStyleSheet("background-color: red")
                self.Centreur[i][0].setText('IN')
                self.Centreur[i][0].clicked.connect(self.poluluAction)
          
    def poluluAction(self):
        """
        definition des actions des boutons des polulu
        """
        nCentreur=int(self.win.sender().objectName()[8])
        
        if  self.Polulu[nCentreur].posOFF-100<self.Polulu[nCentreur].position()<self.Polulu[nCentreur].posOFF+100:
            print('on va en IN')
            self.Polulu[nCentreur].goPositionIN()
            self.Polulu[nCentreur].setPosition(self.Polulu[nCentreur].posIN)
            self.Centreur[nCentreur][0].setStyleSheet("background-color: red")
            self.Centreur[nCentreur][0].setText('IN')   
        else:
            print('on va en off')
            self.Polulu[nCentreur].goPositionOFF()
            self.Polulu[nCentreur].setPosition(self.Polulu[nCentreur].posOFF)
            self.Centreur[nCentreur][0].setStyleSheet("background-color:green")
            self.Centreur[nCentreur][0].setText('OUT')
            
        time.sleep(1)
        self.Polulu[nCentreur].stopMotor()
        
   
if __name__ == "__main__":
    appli = QApplication(sys.argv) 
    
    e = SERVOWIN()
    e.show()
    appli.exec_()
            
        
        

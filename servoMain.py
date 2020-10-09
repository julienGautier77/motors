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
            # print('servo in ini   file : ',self.configMotName)
            # print(self.groups)
            
            self.motorListButton=list()
            self.motorListGui=list()
            self.nameMotor=list()
            self.setup()
            self.iniPolulu()
            # self.poluluAction()
            
            
    def setup(self):
        
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            grid = QGridLayout()
            vbox1=QVBoxLayout() 
            print('Please wait ...')
        
            for vi in self.groups:
                #print(vi)
                # creation des boutons avec le nom
                self.motorListButton.append(QPushButton(self.conf.value(vi+"/Name"),self))  
                # creation de widget oneMotorGui pour chaque moteurs
                self.motorListGui.append(servo.MOTORSERVO(mot1=str(vi)))
                self.nameMotor.append(self.conf.value(vi+"/Name"))
             
            #creation des d'une matrice de point pour creer une grille    
            z=0
            self.nbOfMotor=len(self.motorListButton)
            # print(self.nbOfMotor)
            # print(self.motorListButton)
            for i in range(0,int(self.nbOfMotor/2)):
                for j in range(0,int(self.nbOfMotor/2)):
                    if z<self.nbOfMotor:
                        grid.addWidget(self.motorListButton[z], j, i)
                        # print(z,i,j)
                    z+=1
                
            
            # # ajout de la grille de bouton au widget proncipal
            vbox1.addLayout(grid)
            self.setLayout(vbox1)   
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            
            j = 0
            for mm in self.motorListButton:
              
                #action de chaque bouton : open a new widget for onemotor control
                mm.clicked.connect(lambda checked, j=j:self.actionPush(self.motorListGui[j],j))
                j+=1
        
    def actionPush(self,nbServo,nbButton):
        j=nbButton
        # print(nbServo.posOFF,j)
        button=self.motorListButton[j]
        
        
        if  nbServo.posOFF-100<int(nbServo.position())<nbServo.posOFF+100:
            # print('on va en IN')
            nbServo.goPositionIN()
            nbServo.setPosition(nbServo.posIN)
            button.setStyleSheet("background-color: green")
            button.setText(self.nameMotor[j]+' :   (IN)')   
        else:
            # print('on va en off')
            nbServo.goPositionOFF()
            nbServo.setPosition(nbServo.posOFF)
            button.setStyleSheet("background-color:red")
            button.setText(self.nameMotor[j]+' (OUT)')
            
        time.sleep(1)
        nbServo.stopMotor()
        
    def closeEvent(self,event):
        print('close...')
        servo.stopConnexion()
        event.accept() 
            

    def iniPolulu(self):
            """
            initialisation des polulu
            """
            print('initialisation ...')
            print('servo motor go to position in : ')
            for mot in self.motorListGui:
                
                mot.goPositionIN()
                time.sleep(0.3)
                mot.setPosition(mot.posIN)
                j=0
                print('...',end='')
            for but in self.motorListButton:
                but.setStyleSheet("background-color: green")
                but.setText(self.nameMotor[j]+'  (IN)')
                j+=1
            print()
            print('done') 
           
   
if __name__ == "__main__":
    appli = QApplication(sys.argv) 
    
    e = SERVOWIN()
    e.show()
    appli.exec_()
            
        
        

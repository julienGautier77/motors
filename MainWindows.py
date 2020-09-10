#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 09:42:51 2019

@author: juliengautier


create button and control all the motors in the .ini file


"""


from PyQt5 import QtCore

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout,QVBoxLayout
from PyQt5.QtGui import QIcon
import oneMotorGuiNew
import pathlib,os
import qdarkstyle
from TirGui import TIRGUI


class MainWin(QWidget) :
    def __init__(self,shoot=True,title='Motors Control',configFile='configMoteurRSAI.ini'):
        super(MainWin, self).__init__() 
        p = pathlib.Path(__file__)
        sepa=os.sep
        
       
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        
        self.shoot=shoot
        self.configPath=str(p.parent / "fichiersConfig")+sepa
        self.configMotName=self.configPath+configFile
        self.conf=QtCore.QSettings(self.configMotName, QtCore.QSettings.IniFormat)   
        self.groups=self.conf.childGroups() # lecture de tous les moteurs
        print('motor in file : ',self.configMotName)
        print(self.groups)
        self.motorListButton=list()
        self.motorListGui=list()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        grid = QGridLayout()
        vbox1=QVBoxLayout() 
        
        print('Please wait ...')
        
        for vi in self.groups:
            #print(vi)
            # creation des boutons avec le nom
            self.motorListButton.append(QPushButton(self.conf.value(vi+"/Name"),self))  
            # creation de widget oneMotorGui pour chaque moteurs
            self.motorListGui.append(oneMotorGuiNew.ONEMOTORGUI(mot=str(vi),motorTypeName='RSAI'))
            
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
            
        
    
if __name__ == "__main__":
    appli = QApplication(sys.argv) 
    
    e = MainWin(shoot=False)
    e.show()
    appli.exec_()
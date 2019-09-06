#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 09:42:51 2019

@author: juliengautier
"""

#%%
from PyQt5 import QtCore

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout
from PyQt5.QtGui import QIcon
import oneMotorGui

   
class MainWin(QWidget) :
    def __init__(self):
        super(MainWin, self).__init__()   
        self.confA2V=QtCore.QSettings('fichiersConfig/configMoteurA2V.ini', QtCore.QSettings.IniFormat) # motor configuration  files
        self.groups=self.confA2V.childGroups() # lecture de tous les moteurs
        self.motorListButton=list()
        self.motorListGui=list()
        self.setWindowTitle('Titre')
        self.setWindowIcon(QIcon("./LOA.png"))
        grid = QGridLayout()
        for vi in self.groups:
            # creation des boutons avec le nom
            self.motorListButton.append(QPushButton(self.confA2V.value(vi+"/Name"),self))  
            # creation de widget oneMotorGui pour chaque moteurs
            self.motorListGui.append(oneMotorGui.MOTORGUI(mot1=str(vi),motorTypeName='A2V'))
            
        #creation des d'une matrice de point pour creer une grille    
        gridPos = [(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3),(2,0),(2,1),(2,2),(2,3)]
            
        j = 0
        for mm in self.motorListButton:
            #ajout de chaque boutton dans la grille
            grid.addWidget(self.motorListButton[j], gridPos[j][0], gridPos[j][1])
            
            #action de chaque bouton 
            mm.clicked.connect(lambda checked, j=j:self.open_widget(self.motorListGui[j]))
            j+=1
        
        # ajout de la grille de bouton au widget proncipal
        self.setLayout(grid)   
       
    
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
        exit  
            
        
    
if __name__ == "__main__":
    appli = QApplication(sys.argv) 
    
    e = MainWin()
    e.show()
    appli.exec_()
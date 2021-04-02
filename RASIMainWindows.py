#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 09:42:51 2019

@author: juliengautier


create button and control all the motors in the .ini file
ROSA

"""


from PyQt5 import QtCore

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout,QVBoxLayout
from PyQt5.QtGui import QIcon
import oneMotorGuiNew
import pathlib,os
import qdarkstyle
from TirGui import TIRGUI
import moteurRSAI as RSAI
from TiltGuiNew import TILTMOTORGUI
from threeMotorGuiNew import THREEMOTORGUI
from twoMotorGuiNew import TWOMOTORGUI
from twoMotorGuiNewFoc import TWOMOTORGUIFOC

### fichier configuration moteur dans C:\Users\ROSA\Desktop\motors\fichiersConfig


class MainWin(QWidget) :
    
    def __init__(self,shoot=True,title='Motors Control RSAI ROSA',configFile='configMoteurRSAI.ini'):
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
        self.setGeometry(50, 50, 600, 700)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        vbox1=QVBoxLayout() 
        
        self.jetWidget=THREEMOTORGUI( motLat='Jet_LWFA_LAT',motorTypeName0='RSAI', motVert='Jet_LWFA_VERT',motorTypeName1='RSAI',motFoc='Jet_LWFA_FOC',motorTypeName2='RSAI',nomWin='JET Control',nomTilt='JET',nomFoc='',showRef=False,unit=1,unitFoc=2,jogValue=100,jogValueFoc=1,background="green")
        self.jetButton=QPushButton(" JET ")
        self.jetButton.setMinimumHeight(40)
        self.jetButton.setStyleSheet("background-color:green")
        
        self.jetButton.clicked.connect(lambda:self.open_widget(self.jetWidget))
        vbox1.addWidget(self.jetButton)
        
        
        self.miroirP1Widget=TILTMOTORGUI( motLat='Mirror_P1_LAT',motorTypeName0='RSAI',motVert='Mirror_P1_VERT',motorTypeName1='RSAI',nomWin='Tilts Mirror P1',nomTilt=' P1 Mirror',unit=0,jogValue=100)
        self.miroirP1Button=QPushButton(" P1 Mirror ")
        self.miroirP1Button.setMinimumHeight(40)
        self.miroirP1Button.clicked.connect(lambda:self.open_widget(self.miroirP1Widget))
        vbox1.addWidget(self.miroirP1Button)
        
        
        self.axiWidget=TWOMOTORGUI( motLat='Axipara_LAT',motorTypeName0='RSAI', motVert='Axipara_VERT',motorTypeName1='RSAI',nomWin='AXIPARABOLA Control',nomTilt='AXIPARA',unit=1,jogValue=100)
        self.axiButton=QPushButton(" AXIPARABOLE ")
        self.axiButton.setMinimumHeight(40)
        self.axiButton.clicked.connect(lambda:self.open_widget(self.axiWidget))
        vbox1.addWidget(self.axiButton)
        
        self.axiTiltWidget=TILTMOTORGUI( motLat='Axiparab_TILT_LAT',motorTypeName0='RSAI',motVert='Axiparab_TILT_VERT',motorTypeName1='RSAI',nomWin='Tilts AXIPARABOLA',nomTilt=' Tilt AXIPARA',unit=0,jogValue=100)
        self.axiTiltButton=QPushButton(" TILT AXIPARABOLA ")
        self.axiTiltButton.setMinimumHeight(40)
        self.axiTiltButton.clicked.connect(lambda:self.open_widget(self.axiTiltWidget))
        vbox1.addWidget(self.axiTiltButton)
        
        self.miroirAxiWidget=TILTMOTORGUI( motLat='Miroir_axi_LAT',motorTypeName0='RSAI',motVert='Miroir_axi_VERT',motorTypeName1='RSAI',nomWin='Tilts Mirror AXIPARABOLA',nomTilt=' TIlt Mirror AXI',unit=0,jogValue=100)
        self.miroirAxiButton=QPushButton(" Tilts Mirror AXIPARABOLA ")
        self.miroirAxiButton.setMinimumHeight(40)
        self.miroirAxiButton.clicked.connect(lambda:self.open_widget(self.miroirAxiWidget))
        vbox1.addWidget(self.miroirAxiButton)
        
        self.LameWidget=TWOMOTORGUIFOC( motLat='Lame_Foc',motorTypeName0='RSAI', motVert='Lame_Vert',motorTypeName1='RSAI',nomWin='Lame Control',nomTilt='Lame',unit=2,jogValue=1)
        self.LameButton=QPushButton('Lame')
        self.LameButton.setMinimumHeight(40)
        self.LameButton.clicked.connect(lambda:self.open_widget(self.LameWidget))
        vbox1.addWidget(self.LameButton)
        
        self.TBP1Widget=TILTMOTORGUI( motLat="TB_P1_LAT",motorTypeName0='RSAI',motVert='TB_P1_VERT',motorTypeName1='RSAI',nomWin='Tilts TurningBOX P1',nomTilt=' TIlt TB P1',unit=0,jogValue=10,background="purple")
        self.TBP1Button=QPushButton(" Tilts TB P1 ")
        self.TBP1Button.setMinimumHeight(40)
        self.TBP1Button.setStyleSheet("background-color:purple")
        self.TBP1Button.clicked.connect(lambda:self.open_widget(self.TBP1Widget))
        vbox1.addWidget(self.TBP1Button)
        
        self.TBP2Widget=TILTMOTORGUI( motLat="TB_P2_LAT",motorTypeName0='RSAI',motVert='TB_P2_VERT',motorTypeName1='RSAI',nomWin='Tilts TurningBOX P2',nomTilt=' TIlt TB P2',unit=0,jogValue=10,background="purple")
        self.TBP2Button=QPushButton(" Tilts TB P2 ")
        self.TBP2Button.setMinimumHeight(40)
        self.TBP2Button.setStyleSheet("background-color:purple")
        self.TBP2Button.clicked.connect(lambda:self.open_widget(self.TBP2Widget))
        vbox1.addWidget(self.TBP2Button)
        
        self.TBP3Widget=TILTMOTORGUI( motLat="TB_P3_LAT",motorTypeName0='RSAI',motVert='TB_P3_VERT',motorTypeName1='RSAI',nomWin='Tilts TurningBOX P3',nomTilt=' TIlt TB P3',unit=0,jogValue=10,background="purple")
        self.TBP3Button=QPushButton(" Tilts TB P3 ")
        self.TBP3Button.setMinimumHeight(40)
        self.TBP3Button.setStyleSheet("background-color:purple")
        self.TBP3Button.clicked.connect(lambda:self.open_widget(self.TBP3Widget))
        vbox1.addWidget(self.TBP3Button)
        
        
        
        self.camWidget=THREEMOTORGUI( motLat='CAM_Lat',motorTypeName0='RSAI', motVert='CAM_Vert',motorTypeName1='RSAI',motFoc='CAM_Foc',motorTypeName2='RSAI',nomWin='CAMERA Focal Spot Control',nomTilt='Camera',nomFoc='',showRef=False,unit=1,unitFoc=2,jogValue=100,jogValueFoc=1)
        self.camButton=QPushButton(" CAMERA ")
        self.camButton.setMinimumHeight(40)
        # self.camButton.setStyleSheet("background-color:green")
        
        self.camButton.clicked.connect(lambda:self.open_widget(self.camWidget))
        vbox1.addWidget(self.camButton)
        
        
        
        grid = QGridLayout()
        
        self.colorButton=list()
        print('Please wait ...')
        
        for vi in self.groups:
            #print(vi)
            # creation des boutons avec le nom
            self.motorListButton.append(QPushButton(self.conf.value(vi+"/Name"),self))  
            # creation de widget oneMotorGui pour chaque moteurs
            self.motorListGui.append(oneMotorGuiNew.ONEMOTORGUI(mot=str(vi),motorTypeName='RSAI',unit=1,jogValue=100))
            self.colorButton.append(str(self.conf.value(vi+"/Color")))
            
        #creation des d'une matrice de point pour creer une grille    
        z=0
        self.nbOfMotor=len(self.motorListButton)
        for i in range(0,int(self.nbOfMotor/2)):
            for j in range(0,int(self.nbOfMotor/3)):
                if z<self.nbOfMotor:
                    grid.addWidget(self.motorListButton[z], j, i)
                z+=1
            
        j = 0
        for mm in self.motorListButton:
            # #ajout de chaque boutton dans la grille
            # grid.addWidget(self.motorListButton[j], gridPos[j][0], gridPos[j][1])
            
            #action de chaque bouton : open a new widget for onemotor control
            mm.clicked.connect(lambda checked, j=j:self.open_widget(self.motorListGui[j]))
            mm.setMinimumHeight(30)
           
            if self.colorButton[j] != 'None' :
                mm.setStyleSheet("background-color:"+self.colorButton[j])
            else :
                
                mm.setStyleSheet("background-color:gray")
            
                
            j+=1
        
        # ajout de la grille de bouton au widget principal
        vbox1.addLayout(grid)
        if self.shoot==True: # to add shoot button in salle Jaune
            self.tirWidget=TIRGUI()
            vbox1.addWidget(self.tirWidget)
            
        self.setLayout(vbox1)   
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        print('ok')
        
        
    def open_widget(self,fene):
        """ ouverture widget suplementaire 
        """

        if fene.isWinOpen==False:
            fene.setup
            fene.isWinOpen=True
            fene.startThread2()
            self.setWindowState(QtCore.Qt.WindowActive)
            
            fene.setGeometry(700, 200, 200, 200)
            fene.show()
        else:
            fene.activateWindow()
            fene.raise_()
            self.setWindowState(QtCore.Qt.WindowActive)
            fene.showNormal()

    def closeEvent(self,event):
        print('close...')
        RSAI.stopConnexion()
        event.accept() 
            
        
    
if __name__ == "__main__":
    appli = QApplication(sys.argv) 
    
    e = MainWin(shoot=True)
    e.show()
    appli.exec_()
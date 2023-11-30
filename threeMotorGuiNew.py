# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:16:50 2019

@author: sallejaune
"""
#%%Import
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget,QMessageBox,QLineEdit
from PyQt6.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QPushButton,QGridLayout,QDoubleSpinBox,QCheckBox
from PyQt6.QtWidgets import QComboBox,QLabel
from PyQt6.QtGui import QIcon
import sys,time,os
import qdarkstyle
import pathlib
import __init__
import TirGui
__version__=__init__.__version__

from oneMotorGuiNew import ONEMOTORGUI

class THREEMOTORGUI(QWidget) :
    """
    User interface Motor class : 
    MOTOGUI(str(mot1), str(motorTypeName),str(mot2), str(motorTypeName), nomWin,nomTilt,nomFoc,showRef,unit,unitFoc )
    mot0= lat  'name of the motor ' (child group of the ini file)
    mot1 =vert
    mot 2 =foc
    nonWin= windows name
    nonTilt =windows tilt name
    nomFoc= windows Focus name
    showRef True or False to show refWidget 
    unit= initial Unit of the two fisrt motors :
        0=sterp
        1=Micros
        2=mm
        3=ps
        4=degres
        unitFoc= unit of the third motors
        
    motorTypeName= Controler name  : 'RSAI' or 'A2V' or 'NewFocus' or 'SmartAct' or 'Newport' , Servo, Arduino
    
    fichier de config des moteurs : 'configMoteurRSAI.ini' 'configMoteurA2V.ini' 'configMoteurNewFocus.ini' 'configMoteurSmartAct.ini'
    
    
    """




    def __init__(self, motLat='',motorTypeName0='', motVert='',motorTypeName1='',motFoc='',motorTypeName2='',nomWin='',nomTilt='',nomFoc='',showRef=False,unit=1,unitFoc=2,jogValue=1,jogValueFoc=1,parent=None):
        
        super(THREEMOTORGUI, self).__init__()
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        self.motor=[str(motLat),str(motVert),str(motFoc)]
        self.motorTypeName=[motorTypeName0,motorTypeName1,motorTypeName2]
        self.motorType=[0,0,0]
        self.MOT=[0,0,0]
        self.configMotName=[0,0,0]
        self.conf=[0,0,0]
        self.nomTilt=nomTilt
        self.etatLat='ok'
        self.etatVert='ok'
        self.etatFoc='ok'
        self.configPath="./fichiersConfig/"#"/.fichiersConfig/"
        self.isWinOpen=False
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
        self.refShowId=showRef
        self.indexUnit=unit
        self.indexUnitFoc=unitFoc
        self.jogValue=jogValue
        self.jogValueFoc=jogValueFoc
        self.LatWidget=ONEMOTORGUI(mot=self.motor[0],motorTypeName=self.motorTypeName[0],nomWin='Control One Motor : ',showRef=False,unit=2)
        self.VertWidget=ONEMOTORGUI(mot=self.motor[1],motorTypeName=self.motorTypeName[1],nomWin='Control One Motor : ',showRef=False,unit=2)
        self.FocWidget=ONEMOTORGUI(mot=self.motor[2],motorTypeName=self.motorTypeName[2],nomWin='Control One Motor : ',showRef=False,unit=2)
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        self.version=__version__
        self.tir=TirGui.TIRGUI()
        self.setWindowOpacity(0.96)
        
        for zi in range (0,3): #  list configuration and motor types 
            if self.motorTypeName[zi]=='RSAI':
                self.configMotName[zi]=self.configPath+'configMoteurRSAI.ini'
                import moteurRSAI as RSAI
                self.motorType[zi]=RSAI
                self.MOT[zi]=self.motorType[zi].MOTORRSAI(self.motor[zi])
                
            elif self.motorTypeName[zi]=='SmartAct':
                 self.configMotName[zi]=self.configPath+'configMoteurSmartAct.ini'
                 import smartactmot as SmartAct
                 self.motorType[zi]=SmartAct
                 self.MOT[zi]=self.motorType[zi].MOTORSMART(self.motor[zi])
                 
            elif self.motorTypeName[zi]=='A2V':
                 self.configMotName[zi]=self.configPath+'configMoteurA2V.ini'
                 import moteurA2V  as A2V
                 self.motorType[zi]=A2V
                 self.MOT[zi]=self.motorType[zi].MOTORA2V(self.motor[zi])
                 
            elif self.motorTypeName[zi]=='NewFocus':
                 self.configMotName[zi]=self.configPath+'configMoteurNewFocus.ini'
                 import moteurNewFocus as NewFoc
                 self.motorType=NewFoc
                 self.MOT=self.motorType[zi].MOTORNEWFOCUS(self.motor[zi])
                 
            elif self.motorTypeName[zi]=='newport':
                 self.configMotName[zi]=self.configPath+'confNewport.ini'
                 import newportMotors as Newport
                 self.motorType=Newport
                 self.MOT=self.motorType[zi].MOTORNEWPORT(self.motor[zi])
                 
            elif self.motorTypeName[zi]=='Servo':
                 self.configMotName[zi]=self.configPath+'configMoteurServo.ini'
                 import servo as servo
                 self.motorType=servo
                 self.MOT=self.motorType[zi].MOTORSERVO(self.motor[zi])
                 
            elif self.motorTypeName[zi]=='Arduino':
                print('zi',zi)
                self.configMotName[zi]=self.configPath+'configMoteurArduino.ini'
                print(self.configMotName[zi])
                import moteurArduino as arduino
                self.motorType[zi]=arduino
                self.MOT[zi]=self.motorType[zi].MOTORARDUINO(self.motor[zi])
                
            else:
                print('Error config motor Type name')
                self.configMotName[zi]=self.configPath+'configMoteurTest.ini'
                import moteurtest as test
                self.motorType[zi]=test
                self.MOT[zi]=self.motorType[zi].MOTORTEST(self.motor[zi])
                
            self.conf[zi]=QtCore.QSettings(self.configMotName[zi], QtCore.QSettings.Format.IniFormat) # fichier config motor fichier .ini
        
        self.stepmotor=[0,0,0]
        self.butePos=[0,0,0]
        self.buteNeg=[0,0,0]
        self.name=[0,0,0]
        for zzi in range(0,3):
            
            self.stepmotor[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/stepmotor")) #list of stepmotor values for unit conversion
            self.butePos[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteePos")) # list 
            self.buteNeg[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteeneg"))
            self.name[zzi]=str(self.conf[zzi].value(self.motor[zzi]+"/Name"))
        
        self.setWindowTitle(nomWin+'                     V.'+str(self.version))#+' : '+ self.name[0])
        
        self.threadLat=PositionThread(mot=self.MOT[0],motorType=self.motorType[0]) # thread for displaying position Lat
        self.threadLat.POS.connect(self.PositionLat)
        self.threadLat.ETAT.connect(self.EtatLat)
        
        self.threadVert=PositionThread(mot=self.MOT[1],motorType=self.motorType[1]) # thread for displaying  position Vert
        self.threadVert.POS.connect(self.PositionVert)
        self.threadVert.ETAT.connect(self.EtatVert)
        
        self.threadFoc=PositionThread(mot=self.MOT[2],motorType=self.motorType[2]) # thread for displaying  position Foc
        self.threadFoc.POS.connect(self.PositionFoc)
        self.threadFoc.ETAT.connect(self.EtatFoc)
        
        ## initialisation of the jog value 
        if self.indexUnitFoc==0: #  step
            self.unitChangeFoc=1
            self.unitNameFoc='step'
            
        if self.indexUnitFoc==1: # micron
            self.unitChangeFoc=float((1*self.stepmotor[2])) 
            self.unitNameFoc='um'
        if self.indexUnitFoc==2: #  mm 
            self.unitChangeFoc=float((1000*self.stepmotor[2]))
            self.unitNameFoc='mm'
        if self.indexUnitFoc==3: #  ps  double passage : 1 microns=6fs
            self.unitChangeFoc=float(1*self.stepmotor[2]/0.0066666666) 
            self.unitNameFoc='ps'
        if self.indexUnitFoc==4: #  en degres
            self.unitChangeFoc=1 *self.stepmotor[2]
            self.unitNameFoc='°'    
        
        if self.indexUnit==0: # step
            self.unitChangeLat=1
            self.unitChangeVert=1
            self.unitNameTrans='step'
        if self.indexUnit==1: # micron
            self.unitChangeLat=float((1*self.stepmotor[0]))  
            self.unitChangeVert=float((1*self.stepmotor[1]))  
            self.unitNameTrans='um'
        if self.indexUnit==2: 
            self.unitChangeLat=float((1000*self.stepmotor[0]))
            self.unitChangeVert=float((1000*self.stepmotor[1]))
            self.unitNameTrans='mm'
        if self.indexUnit==3: #  ps  en compte le double passage : 1 microns=6fs
            self.unitChangeLat=float(1*self.stepmotor[0]/0.0066666666)  
            self.unitChangeVert=float(1*self.stepmotor[1]/0.0066666666)  
            self.unitNameTrans='ps'
        if self.unitChangeLat==0:
            self.unitChangeLat=1 # if / par 0
        if self.unitChangeVert==0:
            self.unitChangeVert=1 #if / 0
        
        self.setup()
        self.unitFoc()
        self.unitTrans()
        self.jogStep.setValue(self.jogValue)
        self.jogStep_2.setValue(self.jogValueFoc)
        
        
        
    def startThread2(self):
        self.threadVert.ThreadINIT()
        self.threadVert.start()
        time.sleep(0.1)
        self.threadFoc.ThreadINIT()
        self.threadFoc.start()
        time.sleep(0.1)
        self.threadLat.ThreadINIT()
        self.threadLat.start()
        
        
    def setup(self):
        

        vbox1=QVBoxLayout() 
        hboxTitre=QHBoxLayout()
        self.nomTilt=QLabel(self.nomTilt)
        self.nomTilt.setStyleSheet("font: bold 20pt;color:yellow")
        hboxTitre.addWidget(self.nomTilt)
        
        self.unitTransBouton=QComboBox()
        self.unitTransBouton.setMaximumWidth(100)
        self.unitTransBouton.setMinimumWidth(100)
        self.unitTransBouton.setStyleSheet("font: bold 12pt")
        self.unitTransBouton.addItem('Step')
        self.unitTransBouton.addItem('um')
        self.unitTransBouton.addItem('mm')
        self.unitTransBouton.addItem('ps')
        self.unitTransBouton.setCurrentIndex(self.indexUnit)
        
        
        hboxTitre.addWidget(self.unitTransBouton)
        hboxTitre.addStretch(1)
        self.butNegButt=QCheckBox('But Neg',self)
        hboxTitre.addWidget(self.butNegButt)
       
        self.butPosButt=QCheckBox('But Pos',self)
        hboxTitre.addWidget(self.butPosButt)
        vbox1.addLayout(hboxTitre)
        
        hShoot=QHBoxLayout()
        self.shootCibleButton=QPushButton('Shot')
        self.shootCibleButton.setStyleSheet("font: 12pt;background-color: red")
        self.shootCibleButton.setMaximumWidth(100)
        self.shootCibleButton.setMinimumWidth(100)
        hShoot.addWidget(self.shootCibleButton)
        vbox1.addLayout(hShoot)
        
        hLatBox=QHBoxLayout()
        hbox1=QHBoxLayout()
        
        self.posLat=QPushButton('Lateral:')
        self.posLat.setStyleSheet("font: 12pt")
        self.posLat.setMaximumHeight(30)
        self.position_Lat=QLabel('12345667')
        self.position_Lat.setStyleSheet("font: bold 25pt" )
        self.position_Lat.setMaximumHeight(30)
        self.enPosition_Lat=QLineEdit('?')
        self.enPosition_Lat.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.enPosition_Lat.setMaximumWidth(70)
        self.enPosition_Lat.setStyleSheet("font: bold 12pt")
        self.zeroButtonLat=QPushButton('Zero')
        self.zeroButtonLat.setMaximumWidth(30)
        self.zeroButtonLat.setMinimumWidth(30)
        hLatBox.addWidget(self.posLat)
        hLatBox.addWidget(self.position_Lat)
        hLatBox.addWidget(self.enPosition_Lat)
        hLatBox.addWidget(self.zeroButtonLat)
        hLatBox.addSpacing(25)
        
        hVertBox=QHBoxLayout()
        self.posVert=QPushButton('Vertical:')
        self.posVert.setStyleSheet("font: 12pt")
        self.posVert.setMaximumHeight(30)
        self.position_Vert=QLabel('1234556')
        self.position_Vert.setStyleSheet("font: bold 25pt" )
        self.position_Vert.setMaximumHeight(30)
        self.enPosition_Vert=QLineEdit('?')
        self.enPosition_Vert.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.enPosition_Vert.setMaximumWidth(70)
        self.enPosition_Vert.setStyleSheet("font: bold 12pt")
        self.zeroButtonVert=QPushButton('Zero')
        self.zeroButtonVert.setMaximumWidth(30)
        self.zeroButtonVert.setMinimumWidth(30)
        
        
        hVertBox.addWidget(self.posVert)
        hVertBox.addWidget(self.position_Vert)
        hVertBox.addWidget(self.enPosition_Vert)
        hVertBox.addWidget(self.zeroButtonVert)
        hVertBox.addSpacing(25)
        
        vboxLatVert=QVBoxLayout() 
        vboxLatVert.addLayout(hLatBox)
        vboxLatVert.addLayout(hVertBox)
        
        hbox1.addLayout(vboxLatVert)
        
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(0)
        grid_layout.setHorizontalSpacing(10)
        self.haut=QPushButton()
        self.haut.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/flechehaut.png);background-color: transparent;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/flechehaut.png) ;background-color: transparent ;border-color: blue}")
        
        self.haut.setMaximumHeight(70)
        self.haut.setMinimumWidth(70)
        self.haut.setMaximumWidth(70)
        self.haut.setMinimumHeight(70)
        
        self.bas=QPushButton()
        self.bas.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/flechebas.png);background-color: transparent ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/flechebas.png);background-color: transparent ;border-color: blue}")
        self.bas.setMaximumHeight(70)
        self.bas.setMinimumWidth(70)
        self.bas.setMaximumWidth(70)
        self.bas.setMinimumHeight(70)
        
        self.gauche=QPushButton('Left')
        self.gauche.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/flechegauche.png);background-color: transparent ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/flechegauche.png);background-color: transparent ;border-color: blue}")
        
        self.gauche.setMaximumHeight(70)
        self.gauche.setMinimumWidth(70)
        self.gauche.setMaximumWidth(70)
        self.gauche.setMinimumHeight(70)
        self.droite=QPushButton('right')
        self.droite.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/flechedroite.png) ;background-color: transparent ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/flechedroite.png) ;background-color: transparent ;border-color: blue}")
        self.droite.setMaximumHeight(70)
        self.droite.setMinimumWidth(70)
        self.droite.setMaximumWidth(70)
        self.droite.setMinimumHeight(70)
        
        
        self.jogStep=QDoubleSpinBox()
        self.jogStep.setMaximum(1000)
        self.jogStep.setStyleSheet("font: bold 12pt")
        self.jogStep.setValue(100)
        self.jogStep.setMaximumWidth(120)
        
        self.jogStep.setValue(55)
        self.unitChangeLat=1
    
        center=QHBoxLayout()
        center.addWidget(self.jogStep)
        self.hautLayout=QHBoxLayout()
        self.hautLayout.addWidget(self.haut)
        self.basLayout=QHBoxLayout()
        self.basLayout.addWidget(self.bas)
        grid_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        grid_layout.addLayout(self.hautLayout, 0, 1)
        grid_layout.addLayout(self.basLayout,2,1)
        grid_layout.addWidget(self.gauche, 1, 0)
        grid_layout.addWidget(self.droite, 1, 2)
        grid_layout.addLayout(center,1,1)

        hbox1.addLayout(grid_layout)
        vbox1.addLayout(hbox1)     
        vbox1.addSpacing(10)
        
        hboxFoc=QHBoxLayout()
        self.posFoc=QPushButton('Foc:')
        self.posFoc.setMaximumHeight(30)
        self.posFoc.setStyleSheet("font: bold 12pt")
        self.position_Foc=QLabel('1234567')
        self.position_Foc.setStyleSheet("font: bold 25pt" )
        self.position_Foc.setMaximumHeight(30)
        self.unitFocBouton=QComboBox()
        self.unitFocBouton.addItem('Step')
        self.unitFocBouton.addItem('um')
        self.unitFocBouton.addItem('mm')
        self.unitFocBouton.addItem('ps')
        self.unitFocBouton.setMinimumWidth(80)
        self.unitFocBouton.setStyleSheet("font: bold 12pt")
        self.unitFocBouton.setCurrentIndex(self.indexUnitFoc)
        
        
        self.enPosition_Foc=QLineEdit()
        self.enPosition_Foc.setMaximumWidth(60)
        self.enPosition_Foc.setStyleSheet("font: bold 12pt")
        self.enPosition_Foc.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.zeroButtonFoc=QPushButton('Zero')
        self.zeroButtonFoc.setMaximumWidth(30)
        self.zeroButtonFoc.setMinimumWidth(30)
        
        hboxFoc.addWidget(self.posFoc)
        
        hboxFoc.addWidget(self.position_Foc)
        hboxFoc.addWidget(self.unitFocBouton)
        hboxFoc.addWidget(self.enPosition_Foc)
        hboxFoc.addWidget(self.zeroButtonFoc)
        hboxFoc.addSpacing(25)
        
        self.moins=QPushButton()
        self.moins.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/moinsBleu.png);background-color: transparent ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/moinsBleu.png);background-color: transparent;border-color: blue}")
        self.moins.setMaximumWidth(70)
        self.moins.setMinimumHeight(70)
        hboxFoc.addWidget(self.moins)
        
        self.jogStep_2=QDoubleSpinBox()
        self.jogStep_2.setMaximum(10000)
        self.jogStep_2.setStyleSheet("font: bold 12pt")
        self.jogStep_2.setValue(self.jogValueFoc)
        
        hboxFoc.addWidget(self.jogStep_2)
         
        
        self.plus=QPushButton()
        self.plus.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/plusBleu.png) ;background-color: transparent;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/plusBleu.png) ;background-color: transparent;border-color: blue}")
        self.plus.setMaximumWidth(70)
        self.plus.setMinimumHeight(70)
    
        hboxFoc.addWidget(self.plus)
        
        vbox1.addLayout(hboxFoc)
        vbox1.addSpacing(20)
        
        self.stopButton=QPushButton('STOP')
        self.stopButton.setStyleSheet("background-color: red")
        hbox3=QHBoxLayout()
        hbox3.addWidget(self.stopButton)
        self.showRef=QPushButton('Show Ref')
        self.showRef.setMaximumWidth(70)
        hbox3.addWidget(self.showRef)
        vbox1.addLayout(hbox3)
        
        self.REF1 = REF3M(num=1)
        self.REF2 = REF3M(num=2)
        self.REF3 = REF3M(num=3)
        self.REF4 = REF3M(num=4)
        self.REF5 = REF3M(num=5)
        self.REF6 = REF3M(num=6)
        
        grid_layoutRef = QGridLayout()
        grid_layoutRef.setVerticalSpacing(4)
        grid_layoutRef.setHorizontalSpacing(4)
        grid_layoutRef.addWidget(self.REF1,0,0)
        grid_layoutRef.addWidget(self.REF2,0,1)
        grid_layoutRef.addWidget(self.REF3,0,2)
        grid_layoutRef.addWidget(self.REF4,1,0)
        grid_layoutRef.addWidget(self.REF5,1,1)
        grid_layoutRef.addWidget(self.REF6,1,2)
       
        self.widget6REF=QWidget()
        self.widget6REF.setLayout(grid_layoutRef)
        vbox1.addWidget(self.widget6REF)
        
        
    
        self.setLayout(vbox1)
        
        self.absLatRef=[self.REF1.ABSLatref,self.REF2.ABSLatref,self.REF3.ABSLatref,self.REF4.ABSLatref,self.REF5.ABSLatref,self.REF6.ABSLatref] 
        self.absVertRef=[self.REF1.ABSVertref,self.REF2.ABSVertref,self.REF3.ABSVertref,self.REF4.ABSVertref,self.REF5.ABSVertref,self.REF6.ABSVertref]
        self.absFocRef=[self.REF1.ABSFocref,self.REF2.ABSFocref,self.REF3.ABSFocref,self.REF4.ABSFocref,self.REF5.ABSFocref,self.REF6.ABSFocref] # pour memoriser les positions
        self.posText=[self.REF1.posText,self.REF2.posText,self.REF3.posText,self.REF4.posText,self.REF5.posText,self.REF6.posText]
        self.POS=[self.REF1.Pos,self.REF2.Pos,self.REF3.Pos,self.REF4.Pos,self.REF5.Pos,self.REF6.Pos]
        self.Take=[self.REF1.take,self.REF2.take,self.REF3.take,self.REF4.take,self.REF5.take,self.REF6.take]
        
        
        self.jogStep_2.setFocus()
        self.refShow()
        self.actionButton()
#        self.setWindowIcon(QIcon('./icons/LOA.png'))
        
        
    def actionButton(self):
        '''
           buttons action setup 
        '''
        
        self.unitFocBouton.currentIndexChanged.connect(self.unitFoc) # Foc unit change
        self.unitTransBouton.currentIndexChanged.connect(self.unitTrans) # Trans unit change
        
        self.haut.clicked.connect(self.hMove) # jog up
        self.haut.setAutoRepeat(False)
        self.bas.clicked.connect(self.bMove) # jog down
        self.bas.setAutoRepeat(False)
        self.gauche.clicked.connect(self.gMove)
        self.gauche.setAutoRepeat(False)
        self.droite.clicked.connect(self.dMove)
        self.droite.setAutoRepeat(False)
        
        self.plus.clicked.connect(self.pMove) # jog + foc
        self.plus.setAutoRepeat(False)
        self.moins.clicked.connect(self.mMove)# jog - fo
        self.moins.setAutoRepeat(False) 
                
        self.zeroButtonFoc.clicked.connect(self.ZeroFoc) # reset display to 0
        self.zeroButtonLat.clicked.connect(self.ZeroLat)
        self.zeroButtonVert.clicked.connect(self.ZeroVert)
        
        #self.refZeroButton.clicked.connect(self.RefMark) # todo
        
        self.stopButton.clicked.connect(self.StopMot)
        self.showRef.clicked.connect(self.refShow)
        
        self.posVert.clicked.connect(lambda:self.open_widget(self.VertWidget))
        self.posLat.clicked.connect(lambda:self.open_widget(self.LatWidget))
        self.posFoc.clicked.connect(lambda:self.open_widget(self.FocWidget))
        self.shootCibleButton.clicked.connect(self.ShootAct)
        
        iii=1
        for saveNameButton in self.posText: # refference name
            nbRef=str(iii)
            saveNameButton.textChanged.connect(self.savName)
            saveNameButton.setText(str(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Name"))) # print  ref name
            iii+=1        
        for posButton in self.POS: # button GO
            posButton.clicked.connect(self.ref)    # go to reference value
        eee=1   
        for absButton in self.absLatRef: 
            nbRef=str(eee)
            absButton.setValue(float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))/self.unitChangeLat) # save reference lat  value
            #print('absButtonvalue',int(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos")))
            absButton.editingFinished.connect(self.savRefLat) # sauv value
            eee+=1
        eee=1     
        for absButton in self.absVertRef: 
            nbRef=str(eee)
            absButton.setValue(float(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Pos"))/self.unitChangeVert) #save reference vert value 
            absButton.editingFinished.connect(self.savRefVert) # save  value
            eee+=1
        eee=1     
        for absButton in self.absFocRef: 
            nbRef=str(eee)
            absButton.setValue(float(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Pos"))/self.unitChangeFoc) # save reference foc value
            absButton.editingFinished.connect(self.savRefFoc) #
            eee+=1
            
        for takeButton in self.Take:
            takeButton.clicked.connect(self.take)
             # take the value 
        
    def open_widget(self,fene):
        
        """ open new widget 
        """
        
        if fene.isWinOpen==False:
            #New widget"
            fene.show()
            fene.startThread2()
            fene.isWinOpen=True
    
        else:
            #fene.activateWindow()
            fene.raise_()
            fene.showNormal()  
            
            
            
    def refShow(self):
        
        if self.refShowId==True:
            #print(self.geometry())
            #self.resize(368, 345)
            self.widget6REF.show()
            self.refShowId=False
            self.showRef.setText('Hide Ref')
            self.setFixedSize(750,800)
            
            
        else:
            #print(self.geometry())
            self.widget6REF.hide()
            self.refShowId=True

            self.showRef.setText('Show Ref')
#            
            self.setFixedSize(750,450)
           
            #self.updateGeometry()      
    

       
    def pMove(self):
        '''
        action jog + foc 
        '''
        a=float(self.jogStep_2.value())
        a=float(a*self.unitChangeFoc)
        b=self.MOT[2].position()
        a=float(self.jogStep_2.value())
        a=float(a*self.unitChangeFoc)
        b=self.MOT[2].position()
        
        if b+a>self.butePos[2] :
            print( "STOP : Positive switch")
            self.MOT[2].stopMotor()
            self.butPosButt.setChecked(True)
        else :
            self.MOT[2].rmove(a)
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False)

    def mMove(self): 
        '''
        action jog - foc
        '''
        a=float(self.jogStep_2.value())
        a=float(a*self.unitChangeFoc)
        b=self.MOT[2].position()
        if b-a<self.buteNeg[2] :
            print( "STOP : Negative switch")
            self.MOT[2].stopMotor()
            self.butNegButt.setChecked(True)
        else :
            self.MOT[2].rmove(-a)
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False)


    def gMove(self):
        '''
        action button left + 
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeLat)
        b=self.MOT[0].position()
       
        if b+a>self.butePos[0] :
            print( "STOP : Positive switch")
            self.MOT[0].stopMotor()
            self.butPosButt.setChecked(True)
        else :
            self.MOT[0].rmove(a)
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False)
            
    def dMove(self):
        '''
        action bouton right -
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeLat)
        b=self.MOT[0].position()
        if b-a<self.buteNeg[0] :
            print( "STOP : Negative switch")
            self.MOT[0].stopMotor()
            self.butNegButt.setChecked(True)
        else :
            self.MOT[0].rmove(-a)
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False)
        
    def hMove(self): 
        '''
        action button up +
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeVert)
        b=self.MOT[1].position()
        if b+a>self.butePos[1] :
            print( "STOP : Positive switch")
            self.MOT[1].stopMotor()
            self.butPosButt.setChecked(True)
            
        else :
            self.MOT[1].rmove(a)           
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False) 
        
        
    def bMove(self):
        '''
        action button up -
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeVert)
        b=self.MOT[1].position()
        if b-a<self.buteNeg[1] :
            self.MOT[1].stopMotor()
            print( "STOP : Negative switch")
            self.butNegButt.setChecked(True)
        else :
            self.MOT[1].rmove(-a)   
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False)   
        
    def ZeroLat(self): #  zero 
        self.MOT[0].setzero()
    def ZeroVert(self): #  zero 
        self.MOT[1].setzero()
    def ZeroFoc(self): #  zero 
        self.MOT[2].setzero()

    def RefMark(self): # 
        """
            todo ....
        """
        #self.motorType.refMark(self.motor)
   
    def unitFoc(self):
        '''
        unit change mot foc
        '''
        self.indexUnitFoc=self.unitFocBouton.currentIndex()
        valueJog_2=self.jogStep_2.value()*self.unitChangeFoc
        if self.indexUnitFoc==0: #  step
            self.unitChangeFoc=1
            self.unitNameFoc='step'
        if self.indexUnitFoc==1: # micron
            self.unitChangeFoc=float((1*self.stepmotor[2]))  
            self.unitNameFoc='um'
        if self.indexUnitFoc==2: #  mm 
            self.unitChangeFoc=float((1000*self.stepmotor[2]))
            self.unitNameFoc='mm'
        if self.indexUnitFoc==3: #  ps  double passage : 1 microns=6fs
            self.unitChangeFoc=float(1*self.stepmotor[2]/0.0066666666)    
            self.unitNameFoc='ps'
        if self.unitChangeFoc==0:
            self.unitChangeFoc=1 #avoid 0 
        
        self.jogStep_2.setValue(valueJog_2/self.unitChangeFoc)
        self.jogStep_2.setSuffix(" %s" % self.unitNameFoc)
        eee=1     
        for absButton in self.absFocRef: 
            nbRef=str(eee)
            absButton.setValue(float(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Pos"))/self.unitChangeFoc) # save reference foc value
            absButton.setSuffix(" %s" % self.unitNameFoc)
            eee+=1
        
    def unitTrans(self):
        '''
         unit change mot foc
        '''
        valueJog=self.jogStep.value()*self.unitChangeLat
        
        
        self.indexUnit=self.unitTransBouton.currentIndex()
        if self.indexUnit==0: # step
            self.unitChangeLat=1
            self.unitChangeVert=1
            self.unitNameTrans='step'
        if self.indexUnit==1: # micron
            self.unitChangeLat=float((1*self.stepmotor[0]))  
            self.unitChangeVert=float((1*self.stepmotor[1]))  
            self.unitNameTrans='um'
        if self.indexUnit==2: 
            self.unitChangeLat=float((1000*self.stepmotor[0]))
            self.unitChangeVert=float((1000*self.stepmotor[1]))
            self.unitNameTrans='mm'
        if self.indexUnit==3: #  ps  en compte le double passage : 1 microns=6fs
            self.unitChangeLat=float(1*self.stepmotor[0]/0.0066666666)  
            self.unitChangeVert=float(1*self.stepmotor[1]/0.0066666666)  
            self.unitNameTrans='ps'
        if self.unitChangeLat==0:
            self.unitChangeLat=1 # if / par 0
        if self.unitChangeVert==0:
            self.unitChangeVert=1 #if / 0
        
        
        
        self.jogStep.setValue(valueJog/self.unitChangeLat)
        self.jogStep.setSuffix(" %s" % self.unitNameTrans)
        
        eee=1   
        for absButton in self.absLatRef: 
            nbRef=str(eee)
            absButton.setValue(float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))/self.unitChangeLat) # save reference lat  value
            absButton.setSuffix(" %s" % self.unitNameTrans)
            eee+=1
        eee=1     
        for absButton in self.absVertRef: 
            nbRef=str(eee)
            absButton.setValue(float(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Pos"))/self.unitChangeVert) #save reference vert value 
            absButton.setSuffix(" %s" % self.unitNameTrans)
            eee+=1
        
        
        
        
    def StopMot(self):
        '''
        stop all motors
        '''
        for zzi in range(0,3):
            self.MOT[zzi].stopMotor();
            
    def EtatLat(self,etat):
#        print(etat)
        self.etatLat=etat
    def EtatVert(self,etat):
#        print(etat)
        self.etatVert=etat
    def EtatFoc(self,etat):
#        print(etat)
        self.etatFoc=etat    
        
    def PositionLat(self,Posi):
        ''' 
        Position Lat  display with the second thread
        '''
        a=float(Posi)
        b=a # value in step
        a=a/self.unitChangeLat # value with unit changed
        if self.etatLat=='FDC-':
            self.position_Lat.setText('FDC -')
            self.position_Lat.setStyleSheet('font: bold 25pt;color:red')
            
        elif self.etatLat=='FDC+':
            self.position_Lat.setText('FDC +')
            self.position_Lat.setStyleSheet('font: bold 25pt;color:red')
        elif self.etatLat=='Power off' :
            self.position_Lat.setText('Power Off')
            self.position_Lat.setStyleSheet('font: bold 20pt;color:red')
        else:   
            self.position_Lat.setText(str(round(a,2))) 
            self.position_Lat.setStyleSheet('font: bold 25pt;color:white')
            
        positionConnue_Lat=0 # 
        precis=5
        if self.motorTypeName[0]=='SmartAct':
            precis=10000
        for nbRefInt in range(1,7):
            nbRef=str(nbRefInt)
            if float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))-precis<b< float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))+precis:
                self.enPosition_Lat.setText(str(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Name")))
                positionConnue_Lat=1
        if positionConnue_Lat==0:
            self.enPosition_Lat.setText('?' ) 
            
    def PositionVert(self,Posi): 
        ''' 
        Position Vert  displayed with the second thread
        '''
        a=float(Posi)
        b=a # value in step 
        a=a/self.unitChangeVert # value  with unit changed
        if self.etatVert=='FDC-':
            self.position_Vert.setText('FDC -')
            self.position_Vert.setStyleSheet('font: bold 25pt;color:red')
            
        elif self.etatVert=='FDC+':
            self.position_Vert.setText('FDC +')
            self.position_Vert.setStyleSheet('font: bold 25pt;color:red')
        elif self.etatVert=='Power off' :
            self.position_Vert.setText('Power Off')
            self.position_Vert.setStyleSheet('font: bold 20pt;color:red')
        else:   
            self.position_Vert.setText(str(round(a,2))) 
            self.position_Vert.setStyleSheet('font: bold 25pt;color:white')
            
        positionConnue_Vert=0 # 
        precis=5
        if self.motorTypeName[1]=='SmartAct':
            precis=10000
        for nbRefInt in range(1,7):
            nbRef=str(nbRefInt)
            if float(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Pos"))-precis<b< float(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Pos"))+precis:
                self.enPosition_Vert.setText(str(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Name")))
                positionConnue_Vert=1     
        if positionConnue_Vert==0:
            self.enPosition_Vert.setText('?' )   
            
    def PositionFoc(self,Posi): 
        ''' 
        Position Foc  displayed with the second thread
        '''
        a=float(Posi)
        b=a # value in step 
        a=a/self.unitChangeFoc # 
        if self.etatFoc=='FDC-':
            self.position_Foc.setText('FDC -')
            self.position_Foc.setStyleSheet('font: bold 25pt;color:red')
            
        elif self.etatFoc=='FDC+':
            self.position_Foc.setText('FDC +')
            self.position_Foc.setStyleSheet('font: bold 25pt;color:red')
        elif self.etatFoc=='Power off' :
            self.position_Foc.setText('Power Off')
            self.position_Foc.setStyleSheet('font: bold 20pt;color:red')
        else:   
            self.position_Foc.setText(str(round(a,2))) 
            self.position_Foc.setStyleSheet('font: bold 25pt;color:white')
        
        
        
        
        positionConnue_Foc=0
        precis=5
        if self.motorTypeName[2]=='SmartAct':
            precis=10000
        for nbRefInt in range(1,7):
            nbRef=str(nbRefInt)
            if float(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Pos"))-precis<b< float(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Pos"))+precis:
                self.enPosition_Foc.setText(str(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Name")))
                positionConnue_Foc=1   
        if positionConnue_Foc==0:
            self.enPosition_Foc.setText('?' )
        

#    

    def take (self) : 
        ''' 
        take and save the reference
        '''
        sender=QtCore.QObject.sender(self) # take the name of  the button 
        # print ('sender name',sender)
        reply=QMessageBox.question(None,'Save Position ?',"Do you want to save this position ?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
               tposLat=self.MOT[0].position()
               nbRef=str(sender.objectName()[0])
              # print('ref',nbRef)
               self.conf[0].setValue(self.motor[0]+"/ref"+nbRef+"Pos",tposLat)
               self.conf[0].sync()
               self.absLatRef[int(nbRef)-1].setValue(tposLat/self.unitChangeLat)
               print ("Position Lat saved")
               tposVert=self.MOT[1].position()
               
               self.conf[1].setValue(self.motor[1]+"/ref"+nbRef+"Pos",tposVert)
               self.conf[1].sync()
               self.absVertRef[int(nbRef)-1].setValue(tposVert/self.unitChangeVert)
               print ("Position Vert saved")
               tposFoc=self.MOT[2].position()
               print('tposFoc',tposFoc)
               self.conf[2].setValue(self.motor[2]+"/ref"+nbRef+"Pos",tposFoc)
               self.conf[2].sync()
               self.absFocRef[int(nbRef)-1].setValue(tposFoc/self.unitChangeFoc)
               print ("Position Foc saved")
#
    def ref(self):  
        '''
        Move the motor to the reference value in step : GO button
        Fait bouger le moteur a la valeur de reference en step : bouton Go 
        '''
        sender=QtCore.QObject.sender(self)
        reply=QMessageBox.question(None,'Go to this Position ?',"Do you want to GO to this position ?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            nbRef=str(sender.objectName()[0])
            for i in range (0,3):
                # print(i)
                vref=int(self.conf[i].value(self.motor[i]+"/ref"+nbRef+"Pos"))
                if vref<self.buteNeg[i] :
                    print( "STOP : negative switch")
                    self.butNegButt.setChecked(True)
                    self.MOT[i].stopMotor()
                elif vref>self.butePos[i] :
                    print( "STOP : positive switch")
                    self.butPosButt.setChecked(True)
                    self.MOT[i].stopMotor()
                else :
                    self.MOT[i].move(vref)
                    time.sleep(1)
                    self.butNegButt.setChecked(False)
                    self.butPosButt.setChecked(False) 
#
    def savName(self) :
        '''
        Save reference name
        '''
        sender=QtCore.QObject.sender(self)
        #print('sender',sender.objectName())
        nbRef=sender.objectName()[0] #PosTExt1
        vname=self.posText[int(nbRef)-1].text()
        for i in range (0,3):
            self.conf[i].setValue(self.motor[i]+"/ref"+nbRef+"Name",str(vname))
            self.conf[i].sync()
#
    def savRefLat (self) :
        '''
        save reference lat value
        '''
        sender=QtCore.QObject.sender(self)
        nbRefLat=sender.objectName()[0] # nom du button ABSref1
        #print('nbref=',nbRefLat)
        vrefLat=int(self.absLatRef[int(nbRefLat)-1].value()*self.unitChangeLat)
        self.conf[0].setValue(self.motor[0]+"/ref"+nbRefLat+"Pos",vrefLat)
        self.conf[0].sync()
        
    def savRefVert (self) : 
        '''
        save reference Vert value
        '''
        sender=QtCore.QObject.sender(self)
        nbRefVert=sender.objectName()[0] 
        vrefVert=int(self.absVertRef[int(nbRefVert)-1].value()*self.unitChangeVert)
        self.conf[1].setValue(self.motor[1]+"/ref"+nbRefVert+"Pos",vrefVert)
        self.conf[1].sync()
        
    def savRefFoc (self) :
        '''
        save reference Foc value
        '''
        sender=QtCore.QObject.sender(self)
        nbRefFoc=sender.objectName()[0] 
        vrefFoc=int(self.absFocRef[int(nbRefFoc)-1].value()*self.unitChangeFoc)
        self.conf[2].setValue(self.motor[2]+"/ref"+nbRefFoc+"Pos",vrefFoc)
        self.conf[2].sync()  
        
    def ShootAct(self):
        self.tir.TirAct()
        
    def closeEvent(self, event):
        """ 
        When closing the window
        """
        self.fini()
        time.sleep(0.1)
        event.accept()
        
    def fini(self): 
        '''
        a the end we close all the thread 
        '''
        self.threadLat.stopThread()
        self.threadVert.stopThread()
        self.threadFoc.stopThread()
        self.isWinOpen=False
        time.sleep(0.1)    
        
        
class REF3M(QWidget):
    
    def __init__(self,num=0, parent=None):
        QtCore.QObject.__init__(self)
        super(REF3M, self).__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
        self.wid=QWidget()
        self.id=num
        self.vboxPos=QVBoxLayout()
        
        self.posText=QLineEdit('ref')
        self.posText.setStyleSheet("font: bold 15pt")
        self.posText.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.posText.setObjectName('%s'%self.id)
        self.vboxPos.addWidget(self.posText)
        self.take=QPushButton()
        self.take.setObjectName('%s'%self.id)
        self.take.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/disquette.png);background-color: rgb(0, 0,0) ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/disquette.png);background-color: rgb(0, 0,0) ;border-color: blue}")
        self.take.setMaximumWidth(30)
        self.take.setMinimumWidth(30)
        self.take.setMinimumHeight(30)
        self.take.setMaximumHeight(30)
        self.takeLayout=QHBoxLayout()
        self.takeLayout.addWidget(self.take)
        self.Pos=QPushButton()
        self.Pos.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/playGreen.png);background-color: rgb(0, 0,0) ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/playGreen.png);background-color: rgb(0, 0, 0) ;border-color: blue}")
        self.Pos.setMinimumHeight(40)
        self.Pos.setMaximumHeight(40)
        self.Pos.setMinimumWidth(40)
        self.Pos.setMaximumWidth(40)
        self.PosLayout=QHBoxLayout()
        self.PosLayout.addWidget(self.Pos)
        self.Pos.setObjectName('%s'%self.id)
        
        LabeLatref=QLabel('Lat:')
        self.ABSLatref=QDoubleSpinBox()
        self.ABSLatref.setObjectName('%s'%self.id)
        self.ABSLatref.setMaximum(5000000000)
        self.ABSLatref.setMinimum(-5000000000)
        
        LabelVertref=QLabel('Vert:')
        self.ABSVertref=QDoubleSpinBox()
        self.ABSVertref.setObjectName('%s'%self.id)
        self.ABSVertref.setMaximum(5000000000)
        self.ABSVertref.setMinimum(-5000000000)
        
        LabelFocref=QLabel('Foc:')
        self.ABSFocref=QDoubleSpinBox()
        self.ABSFocref.setObjectName('%s'%self.id)
        self.ABSFocref.setMaximum(5000000000)
        self.ABSFocref.setMinimum(-5000000000)
        
        grid_layoutPos = QGridLayout()
        grid_layoutPos.setVerticalSpacing(5)
        grid_layoutPos.setHorizontalSpacing(10)
        grid_layoutPos.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        grid_layoutPos.addLayout(self.takeLayout,0,0)
        grid_layoutPos.addLayout(self.PosLayout,0,1)
        grid_layoutPos.addWidget(LabeLatref,1,0)
        grid_layoutPos.addWidget(self.ABSLatref,1,1)
        grid_layoutPos.addWidget(LabelVertref,2,0)
        grid_layoutPos.addWidget(self.ABSVertref,2,1)
        grid_layoutPos.addWidget(LabelFocref,3,0)
        grid_layoutPos.addWidget(self.ABSFocref,3,1)
        self.vboxPos.addLayout(grid_layoutPos)
#        self.vboxPos.setContentsMargins(-10,-10,-10,-10)
        self.wid.setStyleSheet("background-color: rgb(60, 77, 87)")
        self.wid.setLayout(self.vboxPos)
#        self.setContentsMargins(-10,-10,-10,-10)
        mainVert=QVBoxLayout()
        mainVert.addWidget(self.wid)
        mainVert.setContentsMargins(0,0,0,0)
        self.setLayout(mainVert)
       
        
        
        
class PositionThread(QtCore.QThread):
    '''
    Secon thread  to display the position
    '''
    import time #?
    POS=QtCore.pyqtSignal(float) # signal of the second thread to main thread  to display motors position
    ETAT=QtCore.pyqtSignal(str)
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
                time.sleep(0.5)
                Posi=(self.MOT.position())
                
                try :
                    self.POS.emit(Posi)
                    
                    time.sleep(0.1)
                except:
                    print('error emit')
                try :
                    
                    etat=self.MOT.etatMotor()
                        
                    self.ETAT.emit(etat)
                    # print(etat)
                except: pass
                    #print('error emit etat')  
                    
    def ThreadINIT(self):
        self.stop=False   
                        
    def stopThread(self):
        self.stop=True
        time.sleep(0.1)
        self.terminate()
        



if __name__ =='__main__':
   
    appli=QApplication(sys.argv)
    mot5=motLat=THREEMOTORGUI( motLat='camLat',motorTypeName0='RSAI', motVert='camVert',motorTypeName1='RSAI',motFoc='camFoc',motorTypeName2='RSAI',nomWin='Camera Tache Focale',nomTilt='',nomFoc='Cam Foc')
    mot5.show()
    mot5.startThread2()
    appli.exec_()
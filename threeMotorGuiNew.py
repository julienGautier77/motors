# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:16:50 2019

@author: sallejaune
"""
#%%Import
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget,QMessageBox,QLineEdit
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QPushButton,QGridLayout,QDoubleSpinBox
from PyQt5.QtWidgets import QComboBox,QLabel
from PyQt5.QtGui import QIcon
import sys,time,os
import qdarkstyle
import pathlib
import __init__

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
        self.configPath="./fichiersConfig/"#"/.fichiersConfig/"
        self.isWinOpen=False
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.refShowId=showRef
        self.indexUnit=unit
        self.indexUnitFoc=unitFoc
        self.jogValue=jogValue
        self.jogValueFoc=jogValueFoc
        self.LatWidget=ONEMOTORGUI(mot=self.motor[0],motorTypeName0=self.configMotName[0],nomWin='Control One Motor : ',showRef=False,unit=2)
        self.VertWidget=ONEMOTORGUI(mot=self.motor[1],motorTypeName0=self.configMotName[1],nomWin='Control One Motor : ',showRef=False,unit=2)
        self.FocWidget=ONEMOTORGUI(mot=self.motor[2],motorTypeName0=self.configMotName[2],nomWin='Control One Motor : ',showRef=False,unit=2)
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        self.version=__version__
        
        
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
                
            self.conf[zi]=QtCore.QSettings(self.configMotName[zi], QtCore.QSettings.IniFormat) # fichier config motor fichier .ini
        
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
        
        self.threadVert=PositionThread(mot=self.MOT[1],motorType=self.motorType[1]) # thread for displaying  position Vert
        self.threadVert.POS.connect(self.PositionVert)
        
        self.threadFoc=PositionThread(mot=self.MOT[2],motorType=self.motorType[2]) # thread for displaying  position Foc
        self.threadFoc.POS.connect(self.PositionFoc)
        
        self.setup()
        ## initialisation of the jog value 
        if self.indexUnitFoc==0: #  step
            self.unitChangeFoc=1
            self.unitNameFoc='step'
            
        if self.indexUnitFoc==1: # micron
            self.unitChangeFoc=float((1*self.stepmotor[0])) 
            self.unitNameFoc='um'
        if self.indexUnitFoc==2: #  mm 
            self.unitChangeFoc=float((1000*self.stepmotor[0]))
            self.unitNameFoc='mm'
        if self.indexUnitFoc==3: #  ps  double passage : 1 microns=6fs
            self.unitChangeFoc=float(1*self.stepmotor[0]/0.0066666666) 
            self.unitNameFoc='ps'
        if self.indexUnitFoc==4: #  en degres
            self.unitChangeFoc=1 *self.stepmotor[0]
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
        
        
        self.unitFoc()
        self.unitTrans()
        

        
        
        
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
        
        hboxTitre.addWidget(self.nomTilt)
        
        self.unitTransBouton=QComboBox()
        self.unitTransBouton.setMaximumWidth(80)
        self.unitTransBouton.setMinimumWidth(80)
        self.unitTransBouton.addItem('Step')
        self.unitTransBouton.addItem('um')
        self.unitTransBouton.addItem('mm')
        self.unitTransBouton.addItem('ps')
        self.unitTransBouton.setCurrentIndex(self.indexUnit)
        
        
        hboxTitre.addWidget(self.unitTransBouton)
        hboxTitre.addStretch(1)
        vbox1.addLayout(hboxTitre)
        
        hLatBox=QHBoxLayout()
        hbox1=QHBoxLayout()
        
        self.posLat=QPushButton('Lateral:')
        self.posLat.setMaximumHeight(20)
        self.position_Lat=QLabel('12345667')
        self.position_Lat.setStyleSheet("font: bold 25pt" )
        self.position_Lat.setMaximumHeight(30)
        self.enPosition_Lat=QLineEdit('?')
        self.enPosition_Lat.setMaximumWidth(50)
        self.zeroButtonLat=QPushButton('Zero')
        self.zeroButtonLat.setMaximumWidth(50)
        hLatBox.addWidget(self.posLat)
        hLatBox.addWidget(self.position_Lat)
        hLatBox.addWidget(self.enPosition_Lat)
        hLatBox.addWidget(self.zeroButtonLat)
       
        hVertBox=QHBoxLayout()
        self.posVert=QPushButton('Vertical:')
        self.posVert.setMaximumHeight(20)
        self.position_Vert=QLabel('1234556')
        self.position_Vert.setStyleSheet("font: bold 25pt" )
        self.position_Vert.setMaximumHeight(30)
        self.enPosition_Vert=QLineEdit('?')
        self.enPosition_Vert.setMaximumWidth(50)
        self.zeroButtonVert=QPushButton('Zero')
        self.zeroButtonVert.setMaximumWidth(50)
        
        
        hVertBox.addWidget(self.posVert)
        hVertBox.addWidget(self.position_Vert)
        hVertBox.addWidget(self.enPosition_Vert)
        hVertBox.addWidget(self.zeroButtonVert)
        
        vboxLatVert=QVBoxLayout() 
        vboxLatVert.addLayout(hLatBox)
        vboxLatVert.addLayout(hVertBox)
        
        hbox1.addLayout(vboxLatVert)
        
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(0)
        grid_layout.setHorizontalSpacing(10)
        self.haut=QPushButton('Up')
        self.haut.setMinimumHeight(60)
        
        self.bas=QPushButton('Down')
        self.bas.setMinimumHeight(60)
        self.gauche=QPushButton('Left')
        self.gauche.setMinimumHeight(60)
        self.gauche.setMinimumWidth(60)
        self.droite=QPushButton('right')
        self.droite.setMinimumHeight(60)
        self.droite.setMinimumWidth(60)
        self.jogStep=QDoubleSpinBox()
        self.jogStep.setMaximum(10000)
        self.jogStep.setValue(100)
        self.unitChangeLat=1
    
        center=QHBoxLayout()
        center.addWidget(self.jogStep)
        
        grid_layout.addWidget(self.haut, 0, 1)
        grid_layout.addWidget(self.bas,2,1)
        grid_layout.addWidget(self.gauche, 1, 0)
        grid_layout.addWidget(self.droite, 1, 2)
        grid_layout.addLayout(center,1,1)
        hbox1.addLayout(grid_layout)
        vbox1.addLayout(hbox1)     
        
        hboxFoc=QHBoxLayout()
        self.posFoc=QPushButton('Foc:')
        self.posFoc.setMaximumHeight(20)
        
        self.position_Foc=QLabel('1234567')
        self.position_Foc.setStyleSheet("font: bold 25pt" )
        self.position_Foc.setMaximumHeight(30)
        self.unitFocBouton=QComboBox()
        self.unitFocBouton.addItem('Step')
        self.unitFocBouton.addItem('um')
        self.unitFocBouton.addItem('mm')
        self.unitFocBouton.addItem('ps')
        self.unitFocBouton.setMinimumWidth(80)
        self.unitFocBouton.setCurrentIndex(self.indexUnitFoc)
        
        
        self.enPosition_Foc=QLineEdit()
        self.enPosition_Foc.setMaximumWidth(60)
        self.zeroButtonFoc=QPushButton('Zero')
        
        hboxFoc.addWidget(self.posFoc)
        
        hboxFoc.addWidget(self.position_Foc)
        hboxFoc.addWidget(self.unitFocBouton)
        hboxFoc.addWidget(self.enPosition_Foc)
        hboxFoc.addWidget(self.zeroButtonFoc)
        
        self.moins=QPushButton(' - ')
        self.moins.setMinimumWidth(60)
        self.moins.setMinimumHeight(60)
        hboxFoc.addWidget(self.moins)
        self.jogStep_2=QDoubleSpinBox()
        self.jogStep_2.setMaximum(10000)
        
        if self.indexUnitFoc==2 or self.indexUnitFoc==3:
            self.jogStep_2.setValue(1)
        else :
            self.jogStep_2.setValue(100)
        hboxFoc.addWidget(self.jogStep_2)
         
        
        self.plus=QPushButton(' + ')
        self.plus.setMinimumWidth(60)
        self.plus.setMinimumHeight(60)
    
        hboxFoc.addWidget(self.plus)
        
        vbox1.addLayout(hboxFoc)
        
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
        grid_layoutRef.addWidget(self.REF3,1,0)
        grid_layoutRef.addWidget(self.REF4,1,1)
        grid_layoutRef.addWidget(self.REF5,2,0)
        grid_layoutRef.addWidget(self.REF6,2,1)
       
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
            absButton.setValue(int(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))) # save reference lat  value
            #print('absButtonvalue',int(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos")))
            absButton.editingFinished.connect(self.savRefLat) # sauv value
            eee+=1
        eee=1     
        for absButton in self.absVertRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Pos"))) #save reference vert value 
            absButton.editingFinished.connect(self.savRefVert) # save  value
            eee+=1
        eee=1     
        for absButton in self.absFocRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Pos"))) # save reference foc value
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
            self.setFixedSize(600,800)
            
            
        else:
            #print(self.geometry())
            self.widget6REF.hide()
            self.refShowId=True

            self.showRef.setText('Show Ref')
#            
            self.setFixedSize(600,376)
           
            #self.updateGeometry()      
    

       
    def pMove(self):
        '''
        action jog + foc 
        '''
        a=float(self.jogStep_2.value())
        a=float(a*self.unitChangeFoc)
        b=self.MOT[2].position()
        if b+a<self.buteNeg[2] :
            print( "STOP : Positive switch")
            self.MOT[2].stopMotor()
        elif b+a>self.butePos[2] :
            print( "STOP : Negative switch")
            self.MOT[2].stopMotor()
        else :
            self.MOT[2].rmove(a)

    def mMove(self): 
        '''
        action jog - foc
        '''
        a=float(self.jogStep_2.value())
        a=float(a*self.unitChangeFoc)
        b=self.MOT[2].position()
        if b-a<self.buteNeg[2] :
            print( "STOP : Positive switch")
            self.MOT[2].stopMotor()
        elif b-a>self.butePos[2] :
            print( "STOP : Negative switch")
            self.MOT[2].stopMotor()
        else :
            self.MOT[2].rmove(-a)


    def gMove(self):
        '''
        action button left
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeLat)
        b=self.MOT[0].position()
        if b-a<self.buteNeg[0] :
            print( "STOP : Positive switch")
            self.MOT[0].stopMotor()
        elif b-a>self.butePos[0] :
            print( "STOP : Negative switch")
            self.MOT[0].stopMotor()
        else :
            self.MOT[0].rmove(a)
            
    def dMove(self):
        '''
        action bouton left
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeLat)
        b=self.MOT[0].position()
        if b-a<self.buteNeg[0] :
            print( "STOP : Positive switch")
            self.MOT[0].stopMotor()
        elif b-a>self.butePos[0] :
            print( "STOP : Negative switch")
            self.MOT[0].stopMotor()
        else :
            self.MOT[0].rmove(-a)
        
    def hMove(self): 
        '''
        action button up
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeVert)
        b=self.MOT[1].position()
        if b-a<self.buteNeg[1] :
            print( "STOP : Positive switch")
            self.MOT[1].stopMotor()
        elif b-a>self.butePos[1] :
            print( "STOP : Negative switch")
            self.MOT[1].stopMotor()
        else :
            self.MOT[1].rmove(a)   
        
        
    def bMove(self):
        '''
        action button up
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeVert)
        b=self.MOT[1].position()
        if b-a<self.buteNeg[1] :
            print( "STOP : Positive switch")
            self.MOT[1].stopMotor()
        elif b-a>self.butePos[1] :
            print( "STOP : Negative switch")
            self.MOT[1].stopMotor()
        else :
            self.MOT[1].rmove(-a)           
        
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
            absButton.setValue(int(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Pos"))) # save reference foc value
            absButton.setSuffix(" %s" % self.unitNameFoc)
            eee+=1
        
    def unitTrans(self):
        '''
         unit change mot foc
        '''
        valueJog=self.jogStep.value()*self.unitChangeLat
        print(valueJog)
        
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
            absButton.setValue(int(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))) # save reference lat  value
            absButton.setSuffix(" %s" % self.unitNameTrans)
            eee+=1
        eee=1     
        for absButton in self.absVertRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Pos"))) #save reference vert value 
            absButton.setSuffix(" %s" % self.unitNameTrans)
            eee+=1
        
        
        
        
    def StopMot(self):
        '''
        stop all motors
        '''
        for zzi in range(0,3):
            self.MOT[zzi].stopMotor();

    def PositionLat(self,Posi):
        ''' 
        Position Lat  display with the second thread
        '''
        a=float(Posi)
        b=a # value in step
        a=a/self.unitChangeLat # value with unit changed
        self.position_Lat.setText(str(round(a,2))) 
        positionConnue_Lat=0 # 
        precis=1
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
        self.position_Vert.setText(str(round(a,2))) 
        positionConnue_Vert=0 # 
        precis=1
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
        self.position_Foc.setText(str(round(a,2))) 
        positionConnue_Foc=0
        precis=1
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
        print ('sender name',sender)
        reply=QMessageBox.question(None,'Save Position ?',"Do you want to save this position ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
               tposLat=self.MOT[0].position()
               nbRef=str(sender.objectName()[0])
              # print('ref',nbRef)
               self.conf[0].setValue(self.motor[0]+"/ref"+nbRef+"Pos",tposLat)
               self.conf[0].sync()
               self.absLatRef[int(nbRef)-1].setValue(tposLat)
               print ("Position Lat saved")
               tposVert=self.MOT[1].position()
               
               self.conf[1].setValue(self.motor[1]+"/ref"+nbRef+"Pos",tposVert)
               self.conf[1].sync()
               self.absVertRef[int(nbRef)-1].setValue(tposVert)
               print ("Position Vert saved")
               tposFoc=self.MOT[2].position()
               print('tposFoc',tposFoc)
               self.conf[2].setValue(self.motor[2]+"/ref"+nbRef+"Pos",tposFoc)
               self.conf[2].sync()
               self.absFocRef[int(nbRef)-1].setValue(tposFoc)
               print ("Position Foc saved")
#
    def ref(self):  
        '''
        Move the motor to the reference value in step : GO button
        Fait bouger le moteur a la valeur de reference en step : bouton Go 
        '''
        sender=QtCore.QObject.sender(self)
        reply=QMessageBox.question(None,'Go to this Position ?',"Do you want to GO to this position ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            nbRef=str(sender.objectName()[0])
            for i in range (0,3):
                print(i)
                vref=int(self.conf[i].value(self.motor[i]+"/ref"+nbRef+"Pos"))
                if vref<self.buteNeg[i] :
                    print( "STOP : negative switch")
                    self.MOT[i].stopMotor()
                elif vref>self.butePos[i] :
                    print( "STOP : positive switch")
                    self.MOT[i].stopMotor()
                else :
                    self.MOT[i].move(vref)
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
        vrefFoc=int(self.absLatRef[int(nbRefFoc)-1].value()*self.unitChangeFoc)
        self.conf[2].setValue(self.motor[2]+"/ref"+nbRefFoc+"Pos",vrefFoc)
        self.conf[2].sync()        
    
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
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.wid=QWidget()
        self.id=num
        self.vboxPos=QVBoxLayout()
        
        self.posText=QLineEdit('ref')
        self.posText.setObjectName('%s'%self.id)
        self.vboxPos.addWidget(self.posText)
        
        self.take=QPushButton('Take')
        self.take.setObjectName('%s'%self.id)
        self.take.setStyleSheet("background-color: rgb(255,85,0)")
        
        self.Pos=QPushButton('Go')
        self.Pos.setStyleSheet("background-color: rgb(85, 170, 255)")
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
        grid_layoutPos.setVerticalSpacing(0)
        grid_layoutPos.setHorizontalSpacing(10)
        grid_layoutPos.addWidget(self.take,0,0)
        grid_layoutPos.addWidget(self.Pos,0,1)
        grid_layoutPos.addWidget(LabeLatref,1,0)
        grid_layoutPos.addWidget(self.ABSLatref,1,1)
        grid_layoutPos.addWidget(LabelVertref,2,0)
        grid_layoutPos.addWidget(self.ABSVertref,2,1)
        grid_layoutPos.addWidget(LabelFocref,3,0)
        grid_layoutPos.addWidget(self.ABSFocref,3,1)
        self.vboxPos.addLayout(grid_layoutPos)
        self.wid.setStyleSheet("background-color: rgb(60, 77, 87)")
        self.wid.setLayout(self.vboxPos)
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
        

#%%#####################################################################


if __name__ =='__main__':
    motor0="testMot1"
    motor1="testMot2"
    motor2="testMot3"
    appli=QApplication(sys.argv)
    mot5=THREEMOTORGUI( motLat=motor0,motorTypeName0='test', motVert=motor1,motorTypeName1='test',motFoc=motor2,motorTypeName2='test',nomWin='Control 3 motors',nomTilt='Target',unit=1,unitFoc=2,jogValue=100,jogValueFoc=1)
    mot5.show()
    mot5.startThread2()
    appli.exec_()
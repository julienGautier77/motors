# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:16:50 2019

@author: sallejaune
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

class THREEMOTORGUI(QWidget) :
    """
    User interface Motor class : 
    MOTOGUI(str(mot1), str(motorTypeName),str(mot2), str(motorTypeName), nomWin,nomTilt, )
    mot0= lat  'name of the motor ' (child group of the ini file)
    mot1 =vert
    mot 2 =foc
    nonWin= windows name
    nonTilt =windows tilt name
    nomFoc= windows Focus name
    motorTypeName= Controler name  : 'RSAI' or 'A2V' or 'NewFocus' or 'SmartAct' or 'Newport' , Servo
    fichier de config des moteurs : 'configMoteurRSAI.ini' 'configMoteurA2V.ini' 'configMoteurNewFocus.ini' 'configMoteurSmartAct.ini'
    """

    def __init__(self, motLat='',motorTypeName0='', motVert='',motorTypeName1='',motFoc='',motorTypeName2='',nomWin='',nomTilt='',nomFoc='',parent=None):
        
        super(THREEMOTORGUI, self).__init__()
        self.motor=[str(motLat),str(motVert),str(motFoc)]
        self.motorTypeName=[motorTypeName0,motorTypeName1,motorTypeName2]
        self.motorType=[0,0,0]
        self.MOT=[0,0,0]
        self.configMotName=[0,0,0]
        self.conf=[0,0,0]
        self.configPath="/.fichiersConfig/"
        self.isWinOpen=False
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setup()
        self.setWindowTitle(nomWin)
        self.actionButton()
        
        for zi in range (0,3): #  list configuration et moor types 
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
            else:
                print('Error config motor Type name')
           
            self.conf[zi]=QtCore.QSettings(self.configMotName[zi], QtCore.QSettings.IniFormat) # fichier config motor fichier .ini
        
        self.stepmotor=[0,0,0]
        self.butePos=[0,0,0]
        self.buteNeg=[0,0,0]
        
        for zzi in range(0,3):
            self.stepmotor[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/stepmotor")) #list of stepmotor values for unit conversion
            self.butePos[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteePos")) # list 
            self.buteNeg[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteeneg"))
        
        self.unitFoc()
        self.unitTrans()
        
        self.threadLat=PositionThread(mot=self.MOT[0],motorType=self.motorType[0]) # thread for displaying position Lat
        self.threadLat.POS.connect(self.PositionLat)
        
        
        self.threadVert=PositionThread(mot=self.MOT[1],motorType=self.motorType[1]) # thread for displaying  position Vert
        self.threadVert.POS.connect(self.PositionVert)
        
        
        self.threadFoc=PositionThread(mot=self.MOT[2],motorType=self.motorType[2]) # thread for displaying  position Foc
        self.threadFoc.POS.connect(self.PositionFoc)
        
        
        self.absLatRef=[self.ABSLatref1,self.ABSLatref2,self.ABSLatref3,self.ABSLatref4,self.ABSLatref5] 
        self.absVertRef=[self.ABSVertref1,self.ABSVertref2,self.ABSVertref3,self.ABSVertref4,self.ABSVertref5]
        self.absFocRef=[self.ABSFocref1,self.ABSFocref2,self.ABSFocref3,self.ABSFocref4,self.ABSFocref5] # to save positions
        self.posText=[self.posText1,self.posText2,self.posText3,self.posText4,self.posText5]
        self.POS=[self.Pos1,self.Pos2,self.Pos3,self.Pos4,self.Pos5]
        self.Take=[self.take1,self.take2,self.take3,self.take4,self.take5]
        
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
        
        self.setGeometry(0,0,200,200)
        vbox1=QVBoxLayout() 
        hboxTitre=QHBoxLayout()
        self.nomTilt=QLabel('Target Translation')
        
        hboxTitre.addWidget(self.nomTilt)
        
        self.unitTransBouton=QComboBox()
        self.unitTransBouton.setMaximumWidth(80)
        self.unitTransBouton.setMinimumWidth(80)
        self.unitTransBouton.addItem('Step')
        self.unitTransBouton.addItem('um')
        self.unitTransBouton.addItem('mm')
        self.unitTransBouton.addItem('ps')
        
        
        hboxTitre.addWidget(self.unitTransBouton)
        hboxTitre.addStretch(1)
        vbox1.addLayout(hboxTitre)
        
        hLatBox=QHBoxLayout()
        hbox1=QHBoxLayout()
        
        posLAT=QLabel('Lateral:')
        posLAT.setMaximumHeight(20)
        self.position_Lat=QLabel('12345667')
        self.position_Lat.setMaximumHeight(20)
        self.enPosition_Lat=QLineEdit('?')
        self.enPosition_Lat.setMaximumWidth(50)
        self.zeroButtonLat=QPushButton('Zero')
        self.zeroButtonLat.setMaximumWidth(50)
        hLatBox.addWidget(posLAT)
        hLatBox.addWidget(self.position_Lat)
        hLatBox.addWidget(self.enPosition_Lat)
        hLatBox.addWidget(self.zeroButtonLat)
       
        hVertBox=QHBoxLayout()
        posVert=QLabel('Vertical:')
        posVert.setMaximumHeight(20)
        self.position_Vert=QLabel('1234556')
        self.position_Vert.setMaximumHeight(20)
        self.enPosition_Vert=QLineEdit('?')
        self.enPosition_Vert.setMaximumWidth(50)
        self.zeroButtonVert=QPushButton('Zero')
        self.zeroButtonVert.setMaximumWidth(50)
        
        
        hVertBox.addWidget(posVert)
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
        self.jogStep=QSpinBox()
        self.jogStep.setMaximum(10000)
        
        
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
        posFoc=QLabel('Foc:')
        posFoc.setMaximumHeight(20)
        
        self.position_Foc=QLabel('1234567')
        self.position_Foc.setMaximumHeight(20)
        self.unitFocBouton=QComboBox()
        self.unitFocBouton.addItem('Step')
        self.unitFocBouton.addItem('um')
        self.unitFocBouton.addItem('mm')
        self.unitFocBouton.addItem('ps')
        self.unitFocBouton.setMinimumWidth(80)
        
        self.enPosition_Foc=QLineEdit()
        self.enPosition_Foc.setMaximumWidth(50)
        self.zeroButtonFoc=QPushButton('Zero')
        
        hboxFoc.addWidget(posFoc)
        
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
        hboxFoc.addWidget(self.jogStep_2)
         
        
        self.plus=QPushButton(' + ')
        self.plus.setMinimumWidth(60)
        self.plus.setMinimumHeight(60)
    
        hboxFoc.addWidget(self.plus)
        
        vbox1.addLayout(hboxFoc)
        
        
        hboxRef=QHBoxLayout()
        
        self.REF1 = REF(self)
        hboxRef.addWidget(self.REF1)
        self.REF2 = REF(self)
        hboxRef.addWidget(self.REF2)
        self.REF3 = REF(self)
        hboxRef.addWidget(self.REF3)
        self.REF4 = REF(self)
        hboxRef.addWidget(self.REF4)
        self.REF5 = REF(self)
        hboxRef.addWidget(self.REF5)
        hboxRef.setContentsMargins(0,0,0,0)
        
        vbox1.addLayout(hboxRef)
        
        
        
        self.stopButton=QPushButton('STOP')
        self.stopButton.setStyleSheet("background-color: red")
        hbox3=QHBoxLayout()
        hbox3.addWidget(self.stopButton)
        vbox1.addLayout(hbox3)
        self.setLayout(vbox1)
        
        
        self.absLatRef=[self.REF1.ABSLatref,self.REF2.ABSLatref,self.REF3.ABSLatref,self.REF4.ABSLatref,self.REF5.ABSLatref] 
        self.absVertRef=[self.REF1.ABSVertref,self.REF2.ABSVertref,self.REF3.ABSVertref,self.REF4.ABSVertref,self.REF5.ABSVertref]
        self.absFocRef=[self.REF1.ABSFocref,self.REF2.ABSFocref,self.REF3.ABSFocref,self.REF4.ABSFocref,self.REF5.ABSFocref] # pour memoriser les positions
        self.posText=[self.REF1.posText,self.REF2.posText,self.REF3.posText,self.REF4.posText,self.REF5.posText]
        self.POS=[self.REF1.Pos,self.REF2.Pos,self.REF3.Pos,self.REF4.Pos,self.REF5.Pos]
        self.Take=[self.REF1.take,self.REF2.take,self.REF3.take,self.REF4.take,self.REF5.take]
        
        
        
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
        
        self.stopButton.clicked.connect(self.StopMot)#stop motors 
       
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
            absButton.valueChanged.connect(self.savRefLat) # sauv value
            eee+=1
        eee=1     
        for absButton in self.absVertRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Pos"))) #save reference vert value 
            absButton.valueChanged.connect(self.savRefVert) # save  value
            eee+=1
        eee=1     
        for absButton in self.absFocRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Pos"))) # save reference foc value
            absButton.valueChanged.connect(self.savRefFoc) #
            eee+=1
            
        for takeButton in self.Take:
            takeButton.clicked.connect(self.take) # take the value 
        
        
    

       
    def pMove(self):
        '''
        action jog + foc 
        '''
        a=float(self.jogStep_2.value())
        print(a)
        a=float(a*self.unitChangeFoc)
        b=self.MOT[2].position()
        if b+a<self.buteNeg[2] :
            print( "STOP : positive switch")
            self.MOT[2].stopMotor()
        elif b+a>self.butePos[2] :
            print( "STOP : Butée Négative")
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
            print( "STOP : positive switch")
            self.MOT[2].stopMotor()
        elif b-a>self.butePos[2] :
            print( "STOP : negative switch")
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
            print( "STOP : positive switch")
            self.MOT[0].stopMotor()
        elif b-a>self.butePos[0] :
            print( "STOP : negative switch")
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
            print( "STOP : positive switch")
            self.MOT[0].stopMotor()
        elif b-a>self.butePos[0] :
            print( "STOP : negative switch")
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
            print( "STOP : positive switch")
            self.MOT[1].stopMotor()
        elif b-a>self.butePos[1] :
            print( "STOP : negative switch")
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
            print( "STOP : positive switch")
            self.MOT[1].stopMotor()
        elif b-a>self.butePos[1] :
            print( "STOP : negative switch")
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
        ii=self.unitFocBouton.currentIndex()
        if ii==0: #  step
            self.unitChangeFoc=1
        if ii==1: # micron
            self.unitChangeFoc=float((1*self.stepmotor[2]))  
        if ii==2: #  mm 
            self.unitChangeFoc=float((1000*self.stepmotor[2]))
        if ii==3: #  ps  double passage : 1 microns=6fs
            self.unitChangeFoc=float(1*self.stepmotor[2]/0.0066666666)    
        if self.unitChangeFoc==0:
            self.unitChangeFoc=1 #avoid 0 

    def unitTrans(self):
        '''
         unit change mot foc
        '''
        ii=self.unitTransBouton.currentIndex()
        if ii==0: # step
            self.unitChangeLat=1
            self.unitChangeVert=1
        if ii==1: # micron
            self.unitChangeLat=float((1*self.stepmotor[0]))  
            self.unitChangeVert=float((1*self.stepmotor[1]))  
        if ii==2: 
            self.unitChangeLat=float((1000*self.stepmotor[0]))
            self.unitChangeVert=float((1000*self.stepmotor[1]))
        if ii==3: #  ps  en compte le double passage : 1 microns=6fs
            self.unitChangeLat=float(1*self.stepmotor[0]/0.0066666666)  
            self.unitChangeVert=float(1*self.stepmotor[1]/0.0066666666)  
        if self.unitChangeLat==0:
            self.unitChangeLat=1 # if / par 0
        if self.unitChangeVert==0:
            self.unitChangeVert=1 #if / 0
    
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
        self.win.position_Lat.setText(str(round(a,2))) 
        positionConnue_Lat=0 # 
        precis=1
        if self.motorTypeName[0]=='SmartAct':
            precis=10000
        for nbRefInt in range(1,5):
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
        self.win.position_Vert.setText(str(round(a,2))) 
        positionConnue_Vert=0 # 
        precis=1
        if self.motorTypeName[1]=='SmartAct':
            precis=10000
        for nbRefInt in range(1,5):
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
        self.win.position_Foc.setText(str(round(a,2))) 
        positionConnue_Foc=0
        precis=1
        if self.motorTypeName[2]=='SmartAct':
            precis=10000
        for nbRefInt in range(1,5):
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
               nbRef=str(sender.objectName()[4])
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
            nbRef=str(sender.objectName()[3])
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
        nbRef=sender.objectName()[7] #PosTExt1
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
        nbRefLat=sender.objectName()[9] # nom du button ABSref1
        print('nbref=',nbRefLat)
        vrefLat=int(self.absLatRef[int(nbRefLat)-1].value())
        self.conf[0].setValue(self.motor[0]+"/ref"+nbRefLat+"Pos",vrefLat)
        self.conf[0].sync()
        
    def savRefVert (self) : 
        '''
        save reference Vert value
        '''
        sender=QtCore.QObject.sender(self)
        nbRefVert=sender.objectName()[10] 
        vrefVert=int(self.absVertRef[int(nbRefVert)-1].value())
        self.conf[1].setValue(self.motor[1]+"/ref"+nbRefVert+"Pos",vrefVert)
        self.conf[1].sync()
        
    def savRefFoc (self) :
        '''
        save reference Foc value
        '''
        sender=QtCore.QObject.sender(self)
        nbRefFoc=sender.objectName()[9] 
        vrefFoc=int(self.absLatRef[int(nbRefFoc)-1].value())
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
        
        
class REF(QWidget):
    
    def __init__(self, parent=None):
        super(REF, self).__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.wid=QWidget()
        
        self.vboxPos=QVBoxLayout()
        self.posText=QLineEdit('ref')
        self.vboxPos.addWidget(self.posText)
        self.take=QPushButton('Take')
        self.take.setStyleSheet("background-color: rgb(255,85,0)")
        self.Pos=QPushButton('Go')
        self.Pos.setStyleSheet("background-color: rgb(85, 170, 255)")
        LabeLatref=QLabel('Lat:')
        self.ABSLatref=QSpinBox()
        LabelVertref=QLabel('Vert:')
        self.ABSVertref=QSpinBox()
        
        LabelFocref=QLabel('Foc:')
        self.ABSLatref=QSpinBox()
        LabelFocref=QLabel('Foc:')
        self.ABSFocref=QSpinBox()
        
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
    motor0="Cible_Trans_Lat"
    motor1="Cible_Trans_Vert"
    motor2="Cible_Foc"
    appli=QApplication(sys.argv)
    #mot6=MOTORGUI(motor,motorTypeName='Servo')
    mot5=THREEMOTORGUI( motLat='Cible_Trans_Lat',motorTypeName0='RSAI', motVert='Cible_Trans_Vert',motorTypeName1='RSAI',motFoc='Foc_Microscope',motorTypeName2='SmartAct',nomWin='MICROSCOPE',nomTilt='Micro Trans',nomFoc='Micro FOC')
    mot5.show()
    mot5.startThread2()
    appli.exec_()
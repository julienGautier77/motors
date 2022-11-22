# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:16:50 2019

@author: sallejaune
"""

#%%Import
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget,QMessageBox,QLineEdit
from PyQt6.QtWidgets import QVBoxLayout,QHBoxLayout,QPushButton,QGridLayout,QDoubleSpinBox,QCheckBox
from PyQt6.QtWidgets import QComboBox,QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QRect

import sys,time,os
import qdarkstyle
import pathlib

        
from scanMotor import SCAN

import TirGui
#__version__=__init__.__version__



class ONEMOTORGUI(QWidget) :
    """
    User interface Motor class : 
    MOTOGUI(str(mot1), str(motorTypeName),, nomWin,nomTilt, )
    mot0=  'name of the motor ' (child group of the ini file)
    
    nonWin= windows name

    motorTypeName= Controler name  : 'RSAI' or 'A2V' or 'NewFocus' or 'SmartAct' or 'Newport' , Servo
    showRef =True show refrence widget
    unit : 0: step 1: um 2: mm 3: ps 4: °
    
    
    
    fichier de config des moteurs : 'configMoteurRSAI.ini' 'configMoteurA2V.ini' 'configMoteurNewFocus.ini' 'configMoteurSmartAct.ini'
    """

    def __init__(self, mot='',motorTypeName='',nomWin='',showRef=False,unit=2,jogValue=1,parent=None):
       
        super(ONEMOTORGUI, self).__init__(parent)
        
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        self.motor=[str(mot)]
        self.motorTypeName=[motorTypeName]
        self.motorType=[0]
        self.MOT=[0]
        self.configMotName=[0]
        self.conf=[0]
        self.configPath=str(p.parent / "fichiersConfig")+sepa
        self.isWinOpen=False
        appli.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
        self.refShowId=showRef
        self.indexUnit=unit
        self.jogValue=jogValue
        self.etat='ok'
        self.tir=TirGui.TIRGUI()
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        
        for zi in range (0,1): #  list configuration et motor types 
            
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
                 self.motorType[zi]=NewFoc
                 self.MOT[zi]=self.motorType[zi].MOTORNEWFOCUS(self.motor[zi])
                 
            elif self.motorTypeName[zi]=='newport':
                 self.configMotName[zi]=self.configPath+'confNewport.ini'
                 import newportMotors as Newport
                 self.motorType[zi]=Newport
                 self.MOT[zi]=self.motorType[zi].MOTORNEWPORT(self.motor[zi])
                 
            elif self.motorTypeName[zi]=='Servo':
                 self.configMotName[zi]=self.configPath+'configMoteurServo.ini'
                 import servo as servo
                 self.motorType[zi]=servo
                 self.MOT[zi]=self.motorType[zi].MOTORSERVO(self.motor[zi])
                 
            elif self.motorTypeName[zi]=='Arduino':
                self.configMotName[zi]=self.configPath+'configMoteurArduino.ini'
                import moteurArduino as arduino
                self.motorType[zi]=arduino
                self.MOT[zi]=self.motorType[zi].MOTORARDUINO(self.motor[zi])
             
            else:
                print('Error config motor Type name')
                self.configMotName[zi]=self.configPath+'configMoteurTest.ini'
                import moteurtest as test
                self.motorType[zi]=test
                self.MOT[zi]=self.motorType[zi].MOTORTEST(self.motor[zi])
                print(self.configMotName[zi])
                
            self.conf[zi]=QtCore.QSettings(self.configMotName[zi], QtCore.QSettings.Format.IniFormat) # fichier config motor fichier .ini
       
        self.scanWidget=SCAN(MOT=self.MOT[0],motor=self.motor[0],configMotName=self.configMotName[0]) # for the scan
        
        self.stepmotor=[0,0,0]
        self.butePos=[0,0,0]
        self.buteNeg=[0,0,0]
        self.name=[0,0,0]
        
        for zzi in range(0,1):
            
            self.stepmotor[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/stepmotor")) #list of stepmotor values for unit conversion
            self.butePos[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteePos")) # list 
            self.buteNeg[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteeneg"))
            self.name[zzi]=str(self.conf[zzi].value(self.motor[zzi]+"/Name"))
        
        self.setWindowTitle(nomWin+' : '+ self.name[0]+'             V.')
        
        self.thread=PositionThread(self,mot=self.MOT[0],motorType=self.motorType[0]) # thread for displaying position
        self.thread.POS.connect(self.Position)
        self.thread.ETAT.connect(self.Etat)
        
        
        
        ## initialisation of the jog value 
        if self.indexUnit==0: #  step
            self.unitChange=1
            self.unitName='step'
            
        if self.indexUnit==1: # micron
            self.unitChange=float((1*self.stepmotor[0])) 
            self.unitName='um'
        if self.indexUnit==2: #  mm 
            self.unitChange=float((1000*self.stepmotor[0]))
            self.unitName='mm'
        if self.indexUnit==3: #  ps  double passage : 1 microns=6fs
            self.unitChange=float(1*self.stepmotor[0]/0.0066666666) 
            self.unitName='ps'
        if self.indexUnit==4: #  en degres
            self.unitChange=1 *self.stepmotor[0]
            self.unitName='°'    
        self.setup()
        self.unit()
        
        
    def startThread2(self):
        self.thread.ThreadINIT()
        self.thread.start()
        time.sleep(0.1)
        
        
    def setup(self):
        
        vbox1=QVBoxLayout() 
        hboxTitre=QHBoxLayout()
        self.nom=QLabel(self.name[0])
        self.nom.setStyleSheet("font: bold 20pt;color:yellow")
        hboxTitre.addWidget(self.nom)
        
        self.enPosition=QLineEdit()
        #self.enPosition.setMaximumWidth(50)
        self.enPosition.setStyleSheet("font: bold 15pt")
        self.enPosition.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        hboxTitre.addWidget(self.enPosition)
        self.butNegButt=QCheckBox('But Neg',self)
        hboxTitre.addWidget(self.butNegButt)
       
        self.butPosButt=QCheckBox('But Pos',self)
        hboxTitre.addWidget(self.butPosButt)
        vbox1.addLayout(hboxTitre)
        #vbox1.addSpacing(10)
        
        hShoot=QHBoxLayout()
        self.shootCibleButton=QPushButton('Shot')
        self.shootCibleButton.setStyleSheet("font: 12pt;background-color: red")
        self.shootCibleButton.setMaximumWidth(100)
        self.shootCibleButton.setMinimumWidth(100)
        hShoot.addWidget(self.shootCibleButton)
        vbox1.addLayout(hShoot)
        
        
        hbox0=QHBoxLayout()
        self.position=QLabel('1234567')
        self.position.setMaximumWidth(300)
        self.position.setStyleSheet("font: bold 40pt" )
        
        self.unitBouton=QComboBox()
        self.unitBouton.addItem('Step')
        self.unitBouton.addItem('um')
        self.unitBouton.addItem('mm')
        self.unitBouton.addItem('ps')
        self.unitBouton.addItem('°')
        self.unitBouton.setMaximumWidth(100)
        self.unitBouton.setMinimumWidth(100)
        self.unitBouton.setStyleSheet("font: bold 12pt")
        self.unitBouton.setCurrentIndex(self.indexUnit)
        
        
        self.zeroButton=QPushButton('Zero')
        self.zeroButton.setMaximumWidth(50)
        
        hbox0.addWidget(self.position)
        hbox0.addWidget(self.unitBouton)
        hbox0.addWidget(self.zeroButton)
        vbox1.addLayout(hbox0)
        #vbox1.addSpacing(10)
        
        hboxAbs=QHBoxLayout()
        absolueLabel=QLabel('Absolue mouvement')
#        absolueLabel.setStyleSheet("background-color: green")
        self.MoveStep=QDoubleSpinBox()
        self.MoveStep.setMaximum(1000000)
        self.MoveStep.setMinimum(-1000000)
        #self.MoveStep.setStyleSheet("background-color: green")
        
        self.absMvtButton=QPushButton()
        self.absMvtButton.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/playGreen.png);background-color: transparent;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/playGreen.png) ;background-color: transparent;border-color: blue}")
        self.absMvtButton.setMinimumHeight(50)
        self.absMvtButton.setMaximumHeight(50)
        self.absMvtButton.setMinimumWidth(50)
        self.absMvtButton.setMaximumWidth(50)
        #self.absMvtButton.setStyleSheet("background-color: green")
        hboxAbs.addWidget(absolueLabel)
        hboxAbs.addWidget(self.MoveStep)
        hboxAbs.addWidget(self.absMvtButton)
        vbox1.addLayout(hboxAbs)
        vbox1.addSpacing(10)
        hbox1=QHBoxLayout()
        self.moins=QPushButton()
        self.moins.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/moinsBleu.png);background-color: transparent ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/moinsBleu.png);background-color: transparent;border-color: blue}")
        
        self.moins.setMinimumHeight(70)
        self.moins.setMaximumHeight(70)
        self.moins.setMinimumWidth(70)
        self.moins.setMaximumWidth(70)
        
        #self.moins.setStyleSheet("border-radius:20px")
        hbox1.addWidget(self.moins)
        
        self.jogStep=QDoubleSpinBox()
        self.jogStep.setMaximum(10000)
        self.jogStep.setMaximumWidth(130)
        self.jogStep.setStyleSheet("font: bold 12pt")
        self.jogStep.setValue(self.jogValue)
  
        hbox1.addWidget(self.jogStep)
         
        
        self.plus=QPushButton()
        self.plus.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/plusBleu.png) ;background-color: transparent;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/plusBleu.png) ;background-color: transparent;border-color: blue}")
        self.plus.setMinimumHeight(70)
        self.plus.setMaximumHeight(70)
        self.plus.setMinimumWidth(70)
        self.plus.setMaximumWidth(70)
        #self.plus.setStyleSheet("border-radius:20px")
        hbox1.addWidget(self.plus)
        
        vbox1.addLayout(hbox1)
        #vbox1.addStretch(10)
        vbox1.addSpacing(10)
        
        hbox2=QHBoxLayout()
        self.stopButton=QPushButton()
        self.stopButton.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/close.png);background-color: transparent;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/close.png) ;background-color: transparent;border-color: blue}")
        #self.stopButton.setStyleSheet("border-radius:20px;background-color: red")
        self.stopButton.setMaximumHeight(70)
        self.stopButton.setMaximumWidth(70)
        self.stopButton.setMinimumHeight(70)
        self.stopButton.setMinimumWidth(70)
        hbox2.addWidget(self.stopButton)
        vbox2=QVBoxLayout()
        
        self.showRef=QPushButton('Show Ref')
        self.showRef.setMaximumWidth(90)
        vbox2.addWidget(self.showRef)
        self.scan=QPushButton('Scan')
        self.scan.setMaximumWidth(90)
        vbox2.addWidget(self.scan)
        hbox2.addLayout(vbox2)
        
        vbox1.addLayout(hbox2)
        vbox1.addSpacing(10)
        
        self.REF1 = REF1M(num=1)
        self.REF2 = REF1M(num=2)
        self.REF3 = REF1M(num=3)
        self.REF4 = REF1M(num=4)
        self.REF5 = REF1M(num=5)
        self.REF6 = REF1M(num=6)
        
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
       # vbox1.setContentsMargins(0,0,0,0)
        self.setLayout(vbox1)
        
        
        self.absRef=[self.REF1.ABSref,self.REF2.ABSref,self.REF3.ABSref,self.REF4.ABSref,self.REF5.ABSref,self.REF6.ABSref] 
        self.posText=[self.REF1.posText,self.REF2.posText,self.REF3.posText,self.REF4.posText,self.REF5.posText,self.REF6.posText]
        self.POS=[self.REF1.Pos,self.REF2.Pos,self.REF3.Pos,self.REF4.Pos,self.REF5.Pos,self.REF6.Pos]
        self.Take=[self.REF1.take,self.REF2.take,self.REF3.take,self.REF4.take,self.REF5.take,self.REF6.take]
        
        self.actionButton()
        self.jogStep.setFocus()
        self.refShow()
        
        
        
        
    def actionButton(self):
        '''
           buttons action setup 
        '''
        
        self.unitBouton.currentIndexChanged.connect(self.unit) #  unit change
        self.absMvtButton.clicked.connect(self.MOVE)
        self.plus.clicked.connect(self.pMove) # jog + foc
        self.plus.setAutoRepeat(False)
        self.moins.clicked.connect(self.mMove)# jog - fo
        self.moins.setAutoRepeat(False) 
        self.scan.clicked.connect(lambda:self.open_widget(self.scanWidget) )    
        self.zeroButton.clicked.connect(self.Zero) # reset display to 0
       
        #self.refZeroButton.clicked.connect(self.RefMark) # todo
        
        self.stopButton.clicked.connect(self.StopMot)#stop motors 
        self.showRef.clicked.connect(self.refShow) # show references widgets
        self.shootCibleButton.clicked.connect(self.ShootAct)
        iii=1
        for saveNameButton in self.posText: # reference name
            nbRef=str(iii)
            saveNameButton.textChanged.connect(self.savName)
            saveNameButton.setText(str(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Name"))) # print  ref name
            iii+=1        
        for posButton in self.POS: # button GO
            posButton.clicked.connect(self.ref)    # go to reference value
        eee=1   
        for absButton in self.absRef: 
            nbRef=str(eee)
            absButton.setValue(float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))/self.unitChange) # save reference value
            absButton.editingFinished.connect(self.savRef) # sauv value
            eee+=1
       
        for takeButton in self.Take:
            takeButton.clicked.connect(self.take) # take the value 
        
        
    def open_widget(self,fene):
        
        """ open new widget 
        """
        
        if fene.isWinOpen==False:
            #New widget"
            fene.show()
            fene.isWinOpen=True
    
        else:
            #fene.activateWindow()
            fene.raise_()
            fene.showNormal()
        
        
        
    def refShow(self):
        
        if self.refShowId==True:
            #self.resize(368, 345)
            self.widget6REF.show()
            self.refShowId=False
            self.showRef.setText('Hide Ref')
            self.setFixedSize(430,800)
             
        else:
            #print(self.geometry())
            
            self.widget6REF.hide()
            self.refShowId=True
            #self.setGeometry(QRect(107, 75, 429, 315))
            #self.setMaximumSize(368, 345)
            self.showRef.setText('Show Ref')
#            print(self.sizeHint())
#            self.minimumSizeHint()
#            print(self.sizeHint())
#            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            #self.setMaximumSize(300,300)
            self.setFixedSize(430,380)
           
            #self.updateGeometry()
    
    def MOVE(self):
        '''
        absolue mouvment
        '''
        
        a=float(self.MoveStep.value())
        a=float(a*self.unitChange) # changement d unite
        if a<self.buteNeg[0] :
            print( "STOP : Butée Négative")
            self.butNegButt.setChecked(True)
            self.MOT[0].stopMotor()
        elif a>self.butePos[0] :
            print( "STOP : Butée Positive")
            self.butPosButt.setChecked(True)
            self.MOT[0].stopMotor()
        else :
            self.MOT[0].move(a)
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False)
    
    def pMove(self):
        '''
        action jog + foc 
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChange)
        b=self.MOT[0].position()
        
        if b+a>self.butePos[0] :
            print( "STOP :  Positive switch")
            self.MOT[0].stopMotor()
            self.butPosButt.setChecked(True)
        else :
            self.MOT[0].rmove(a)
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False)
    def mMove(self): 
        '''
        action jog - foc
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChange)
        b=self.MOT[0].position()
        if b-a<self.buteNeg[0] :
            print( "STOP : negative switch")
            self.MOT[0].stopMotor()
            self.butNegButt.setChecked(True)
        else :
            self.MOT[0].rmove(-a)
            self.butNegButt.setChecked(False)
            self.butPosButt.setChecked(False)
  
    def Zero(self): #  zero 
        self.MOT[0].setzero()

    def RefMark(self): # 
        """
            todo ....
        """
        #self.motorType.refMark(self.motor)
   
    def unit(self):
        '''
        unit change mot foc
        '''
        self.indexUnit=self.unitBouton.currentIndex()
        valueJog=self.jogStep.value()*self.unitChange
        
        if self.indexUnit==0: #  step
            self.unitChange=1
            self.unitName='step'
            
        if self.indexUnit==1: # micron
            self.unitChange=float((1*self.stepmotor[0])) 
            self.unitName='um'
        if self.indexUnit==2: #  mm 
            self.unitChange=float((1000*self.stepmotor[0]))
            self.unitName='mm'
        if self.indexUnit==3: #  ps  double passage : 1 microns=6fs
            self.unitChange=float(1*self.stepmotor[0]/0.0066666666) 
            self.unitName='ps'
        if self.indexUnit==4: #  en degres
            self.unitChange=1 *self.stepmotor[0]
            self.unitName='°'    
            
        if self.unitChange==0:
            self.unitChange=1 #avoid /0 
            
        self.jogStep.setSuffix(" %s" % self.unitName)
        self.jogStep.setValue(valueJog/self.unitChange)
        self.MoveStep.setSuffix(" %s" % self.unitName)

        eee=1
        for absButton in self.absRef: 
            nbRef=str(eee)
            absButton.setValue(float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))/self.unitChange)
            absButton.setSuffix(" %s" % self.unitName)
            eee+=1
        
        
        
    def StopMot(self):
        '''
        stop all motors
        '''
        self.REF1.show()
        for zzi in range(0,1):
            self.MOT[zzi].stopMotor();

    def Position(self,Posi):
        ''' 
        Position  display with the second thread
        '''
        a=float(Posi)
        b=a # value in step
        a=a/self.unitChange # value with unit changed
        
        if self.etat=='FDC-':
            self.position.setText('FDC -')
            self.position.setStyleSheet('font: bold 40pt;color:red')
            
        elif self.etat=='FDC+':
            self.position.setText('FDC +')
            self.position.setStyleSheet('font: bold 40pt;color:red')
        elif self.etat=='Power off' :
            self.position.setText('Power Off')
            self.position.setStyleSheet('font: bold 30pt;color:red')
        else:   
            self.position.setText(str(round(a,2))) 
            self.position.setStyleSheet('font: bold 40pt;color:white')
            
        positionConnue=0 # 
        precis=5
        if self.motorTypeName[0]=='SmartAct':
            precis=10000
        for nbRefInt in range(1,7):
            nbRef=str(nbRefInt)
            if float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))-precis<b< float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))+precis:
                self.enPosition.setText(str(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Name")))
                positionConnue=1
        if positionConnue==0:
            self.enPosition.setText('?' ) 
   
    def Etat(self,etat):
#        print(etat)
        self.etat=etat
    
    
    def take (self) : 
        ''' 
        take and save the reference
        '''
        sender=QtCore.QObject.sender(self) # take the name of  the button 
        
        nbRef=str(sender.objectName()[0])
        
        reply=QMessageBox.question(None,'Save Position ?',"Do you want to save this position ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
               tpos=float(self.MOT[0].position())
               
               self.conf[0].setValue(self.motor[0]+"/ref"+nbRef+"Pos",tpos)
               self.conf[0].sync()
               
               self.absRef[int(nbRef)-1].setValue(tpos/self.unitChange)
               print ("Position saved",tpos)
               
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
            for i in range (0,1):
                
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
                    self.butNegButt.setChecked(False)
                    self.butPosButt.setChecked(False) 
#
    def savName(self) :
        '''
        Save reference name
        '''
        sender=QtCore.QObject.sender(self)
        nbRef=sender.objectName()[0] #PosTExt1
        vname=self.posText[int(nbRef)-1].text()
        for i in range (0,1):
            self.conf[i].setValue(self.motor[i]+"/ref"+nbRef+"Name",str(vname))
            self.conf[i].sync()
#
    def savRef (self) :
        '''
        save reference  value
        '''
        sender=QtCore.QObject.sender(self)
        nbRef=sender.objectName()[0] # nom du button ABSref1
        
        vref=int(self.absRef[int(nbRef)-1].value())*self.unitChange
        self.conf[0].setValue(self.motor[0]+"/ref"+nbRef+"Pos",vref) # on sauvegarde en step dans le fichier ini
        self.conf[0].sync()
        
    def ShootAct(self):
        try: 
            self.tir.TirAct()  
        except: pass
    
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
        self.thread.stopThread()
        self.isWinOpen=False
        time.sleep(0.1)    
        if self.scanWidget.isWinOpen==True:
            self.scanWidget.close()
        
class REF1M(QWidget):
    
    def __init__(self,num=0, parent=None):
        super(REF1M, self).__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.wid=QWidget()
        self.id=num
        self.vboxPos=QVBoxLayout()
        
        self.posText=QLineEdit('ref')
        self.posText.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.posText.setStyleSheet("font: bold 15pt")
        self.posText.setObjectName('%s'%self.id)
#        self.posText.setMaximumWidth(80)
        self.vboxPos.addWidget(self.posText)
        
        self.take=QPushButton()
        self.take.setObjectName('%s'%self.id)
        self.take.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/disquette.png);background-color: rgb(0, 0, 0,0) ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/disquette.png);background-color: rgb(0, 0, 0,0) ;border-color: blue}")
        self.take.setMaximumWidth(30)
        self.take.setMinimumWidth(30)
        self.take.setMinimumHeight(30)
        self.take.setMaximumHeight(30)
        self.takeLayout=QHBoxLayout()
        self.takeLayout.addWidget(self.take)
        self.Pos=QPushButton()
        self.Pos.setStyleSheet("QPushButton:!pressed{border-image: url(./Iconeslolita/playGreen.png);background-color: rgb(0, 0, 0,0) ;border-color: green;}""QPushButton:pressed{image: url(./IconesLolita/playGreen.png);background-color: rgb(0, 0, 0,0) ;border-color: blue}")
        self.Pos.setMinimumHeight(40)
        self.Pos.setMaximumHeight(40)
        self.Pos.setMinimumWidth(40)
        self.Pos.setMaximumWidth(40)
        self.PosLayout=QHBoxLayout()
        self.PosLayout.addWidget(self.Pos)
        self.Pos.setObjectName('%s'%self.id)
        #○self.Pos.setStyleSheet("background-color: rgb(85, 170, 255)")
        Labelref=QLabel('Pos :')
        Labelref.setMaximumWidth(30)
        Labelref.setStyleSheet("font: 9pt" )
        self.ABSref=QDoubleSpinBox()
        self.ABSref.setMaximum(500000000)
        self.ABSref.setMinimum(-500000000)
        self.ABSref.setValue(123456)
        self.ABSref.setMaximumWidth(80)
        self.ABSref.setObjectName('%s'%self.id)
        self.ABSref.setStyleSheet("font: 9pt" )
        
        grid_layoutPos = QGridLayout()
        grid_layoutPos.setVerticalSpacing(5)
        grid_layoutPos.setHorizontalSpacing(10)
        grid_layoutPos.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        grid_layoutPos.addLayout(self.takeLayout,0,0)
        grid_layoutPos.addLayout(self.PosLayout,0,1)
        grid_layoutPos.addWidget(Labelref,1,0)
        grid_layoutPos.addWidget(self.ABSref,1,1)
        
        
        self.vboxPos.addLayout(grid_layoutPos)
        self.wid.setStyleSheet("background-color: rgb(60, 77, 87);border-radius:10px")
       
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
    ETAT=QtCore.pyqtSignal(str)
    def __init__(self,parent=None,mot='',motorType=''):
        super(PositionThread,self).__init__(parent)
        self.MOT=mot
        self.motorType=motorType
        self.parent=parent
        self.motorTypeName=self.parent.motorTypeName
        self.stop=False
#        print('motor type',self.motorTypeName)
    def run(self):
        while True:
            if self.stop==True:
                break
            else:
                
                Posi=(self.MOT.position())
                time.sleep(0.5)
                
                try :
                    self.POS.emit(Posi)
    
                    time.sleep(0.1)
                
                except:
                    print('error emit')
                if self.motorTypeName[0]=='RSAI':   
                    try :
                        etat=self.MOT.etatMotor()
#                        print(etat)
                        self.ETAT.emit(etat)
                    except: pass
                        #print('error emit etat')  
                    
    def ThreadINIT(self):
        self.stop=False   
                        
    def stopThread(self):
        self.stop=True
        time.sleep(0.1)
        self.terminate()
        

#%%#####################################################################


if __name__ =='__main__':
    
    appli=QApplication(sys.argv)
    
        
    mot5=ONEMOTORGUI( mot='camFoc',motorTypeName='RSAI',showRef=False,unit=4,jogValue=1)
    mot5.show()
    mot5.startThread2()
    appli.exec_()
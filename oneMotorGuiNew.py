# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:16:50 2019

@author: sallejaune
"""
#%%Import
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QMessageBox,QLineEdit
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QPushButton,QGridLayout,QDoubleSpinBox
from PyQt5.QtWidgets import QComboBox,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect

import sys,time,os
import qdarkstyle
import pathlib
from scanMotor import SCAN
__version__=2019.05
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

    def __init__(self, mot='',motorTypeName0='',nomWin='',showRef=False,unit=2,jogValue=1,parent=None):
       
        super(ONEMOTORGUI, self).__init__(parent)
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.icon=str(p.parent) + sepa + 'icons' +sepa
        self.motor=[str(mot)]
        self.motorTypeName=[motorTypeName0]
        self.motorType=[0]
        self.MOT=[0]
        self.configMotName=[0]
        self.conf=[0]
        self.configPath=str(p.parent / "fichiersConfig")+sepa
        self.isWinOpen=False
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.refShowId=showRef
        self.indexUnit=unit
        self.jogValue=jogValue
        self.version=__version__
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
                
            self.conf[zi]=QtCore.QSettings(self.configMotName[zi], QtCore.QSettings.IniFormat) # fichier config motor fichier .ini
       
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
        
        self.setWindowTitle(nomWin+' : '+ self.name[0]+'                     V.'+str(self.version))
        
        self.thread=PositionThread(mot=self.MOT[0],motorType=self.motorType[0]) # thread for displaying position
        self.thread.POS.connect(self.Position)
        
        self.setup()
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
        
        self.unit()
        
    def startThread2(self):
        self.thread.ThreadINIT()
        self.thread.start()
        time.sleep(0.1)
        
        
    def setup(self):
        
        
        vbox1=QVBoxLayout() 
        hboxTitre=QHBoxLayout()
        self.nom=QLabel(self.name[0])
        self.nom.setStyleSheet("font: bold 30pt")
        hboxTitre.addWidget(self.nom)
        
        self.enPosition=QLineEdit()
        #self.enPosition.setMaximumWidth(50)
        self.enPosition.setStyleSheet("font: bold 15pt")
        hboxTitre.addWidget(self.enPosition)
        
        vbox1.addLayout(hboxTitre)
        #vbox1.addSpacing(10)
        
        hbox0=QHBoxLayout()
        self.position=QLabel('1234567')
        self.position.setMaximumWidth(300)
        self.position.setStyleSheet("font: bold 50pt" )
        
        self.unitBouton=QComboBox()
        self.unitBouton.addItem('Step')
        self.unitBouton.addItem('um')
        self.unitBouton.addItem('mm')
        self.unitBouton.addItem('ps')
        self.unitBouton.addItem('°')
        self.unitBouton.setMaximumWidth(100)
        self.unitBouton.setMinimumWidth(100)
        self.unitBouton.setCurrentIndex(self.indexUnit)
        
        self.zeroButton=QPushButton('Zero')
        self.zeroButton.setMaximumWidth(50)
        
        hbox0.addWidget(self.position)
        hbox0.addWidget(self.unitBouton)
        hbox0.addWidget(self.zeroButton)
        vbox1.addLayout(hbox0)
        #vbox1.addSpacing(10)
        
        hbox1=QHBoxLayout()
        self.moins=QPushButton(' - ')
        self.moins.setMaximumWidth(70)
        self.moins.setMinimumHeight(70)
        self.moins.setStyleSheet("border-radius:20px")
        hbox1.addWidget(self.moins)
        
        
        self.jogStep=QDoubleSpinBox()
        self.jogStep.setMaximum(10000)
        self.jogStep.setMaximumWidth(100)
        
        self.jogStep.setValue(self.jogValue)
  
        hbox1.addWidget(self.jogStep)
         
        
        self.plus=QPushButton(' + ')
        self.plus.setMaximumWidth(70)
        self.plus.setMinimumHeight(70)
        self.plus.setStyleSheet("border-radius:20px")
        hbox1.addWidget(self.plus)
        
        vbox1.addLayout(hbox1)
        #vbox1.addStretch(10)
        vbox1.addSpacing(10)
        
        hbox2=QHBoxLayout()
        self.stopButton=QPushButton('STOP')
        self.stopButton.setStyleSheet("border-radius:20px;background-color: red")
        self.stopButton.setMinimumHeight(50)
        #self.stopButton.setMinimumWidth(80)
        hbox2.addWidget(self.stopButton)
        vbox2=QVBoxLayout()
        
        self.showRef=QPushButton('Show Ref')
        self.showRef.setMaximumWidth(70)
        vbox2.addWidget(self.showRef)
        self.scan=QPushButton('Scan')
        self.scan.setMaximumWidth(70)
        vbox2.addWidget(self.scan)
        hbox2.addLayout(vbox2)
        
        vbox1.addLayout(hbox2)
        
        
        
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
        
        self.plus.clicked.connect(self.pMove) # jog + foc
        self.plus.setAutoRepeat(False)
        self.moins.clicked.connect(self.mMove)# jog - fo
        self.moins.setAutoRepeat(False) 
        self.scan.clicked.connect(lambda:self.open_widget(self.scanWidget) )    
        self.zeroButton.clicked.connect(self.Zero) # reset display to 0
       
        #self.refZeroButton.clicked.connect(self.RefMark) # todo
        
        self.stopButton.clicked.connect(self.StopMot)#stop motors 
        self.showRef.clicked.connect(self.refShow) # show references widgets
        
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
            absButton.setValue(int(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))) # save reference value
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
            self.setFixedSize(429,673)
            
            
        else:
            #print(self.geometry())
            self.resize(368, 345)
            self.widget6REF.hide()
            self.refShowId=True
            self.setGeometry(QRect(107, 75, 429, 315))
            #self.setMaximumSize(368, 345)
            self.showRef.setText('Show Ref')
#            print(self.sizeHint())
#            self.minimumSizeHint()
#            print(self.sizeHint())
#            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            #self.setMaximumSize(300,300)
            self.setFixedSize(429,315)
           
            #self.updateGeometry()
       
    def pMove(self):
        '''
        action jog + foc 
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChange)
        b=self.MOT[0].position()
        if b+a<self.buteNeg[0] :
            print( "STOP : positive switch")
            self.MOT[0].stopMotor()
        elif b+a>self.butePos[0] :
            print( "STOP :  Negative switch")
            self.MOT[0].stopMotor()
        else :
            self.MOT[0].rmove(a)

    def mMove(self): 
        '''
        action jog - foc
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChange)
        b=self.MOT[0].position()
        if b-a<self.buteNeg[0] :
            print( "STOP : positive switch")
            self.MOT[0].stopMotor()
        elif b-a>self.butePos[0] :
            print( "STOP : negative switch")
            self.MOT[0].stopMotor()
        else :
            self.MOT[0].rmove(-a)

  
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
        print(valueJog)
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
#        if self.indexUnit==2 or self.indexUnit==3:
#            self.jogStep.setValue(1)
#        else :
#            self.jogStep.setValue(100)
        
        eee=1
        for absButton in self.absRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))/self.unitChange)
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
        self.position.setText(str(round(a,2))) 
        positionConnue=0 # 
        precis=1
        if self.motorTypeName[0]=='SmartAct':
            precis=10000
        for nbRefInt in range(1,5):
            nbRef=str(nbRefInt)
            if float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))-precis<b< float(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))+precis:
                self.enPosition.setText(str(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Name")))
                positionConnue=1
        if positionConnue==0:
            self.enPosition.setText('?' ) 
   

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
        self.posText.setObjectName('%s'%self.id)
        self.posText.setMaximumWidth(80)
        self.vboxPos.addWidget(self.posText)
        
        self.take=QPushButton('Take')
        self.take.setObjectName('%s'%self.id)
        self.take.setStyleSheet("background-color: rgb(255,85,0)")
        self.take.setMaximumWidth(80)
        self.Pos=QPushButton('Go')
        self.Pos.setMaximumWidth(60)
        self.Pos.setObjectName('%s'%self.id)
        self.Pos.setStyleSheet("background-color: rgb(85, 170, 255)")
        Labelref=QLabel('Pos:')
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
        grid_layoutPos.setVerticalSpacing(0)
        grid_layoutPos.setHorizontalSpacing(5)
        grid_layoutPos.addWidget(self.take,0,0)
        grid_layoutPos.addWidget(self.Pos,0,1)
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
    
    appli=QApplication(sys.argv)
    
    mot5=ONEMOTORGUI( mot='testMot',motorTypeName0='test',nomWin='Control One Motor',showRef=False,unit=2,jogValue=1,parent=None)
    mot5.show()
    mot5.startThread2()
    appli.exec_()
# -*- coding: utf-8 -*-
"""
Interface Graphique pour le pilotage de deux moteurs tilt
Controleurs possible : A2V RSAI NewFocus SmartAct ,newport, Polulu
Thread secondaire pour afficher les positions
import files : moteurRSAI.py smartactmot.py moteurNewFocus.py  moteurA2V.py newportMotors.py servo.py
memorisation de 5 positions
python 3.X PyQt5 
System 32 bit (at least python MSC v.1900 32 bit (Intel)) 
@author: Gautier julien loa
Created on Tue Jan 4 10:42:10 2018
Modified on Tue july 17  10:49:32 2018
"""
#%%Import
from PyQt5 import QtCore,uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QMessageBox
from PyQt5.QtWidgets import QWidget,QMessageBox,QSpinBox
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QWidget,QPushButton,QGridLayout,QTextEdit,QDoubleSpinBox
from PyQt5.QtWidgets import QInputDialog,QComboBox,QSlider,QCheckBox,QLabel,QSizePolicy,QLineEdit,QPlainTextEdit,QMessageBox,QMenu
import qdarkstyle

import time
import sys
PY = sys.version_info[0]
if PY<3:
    print('wrong version of python : Python 3.X must be used')
#%%class TiltMORTGUI
class TiltMOTORGUI(QWidget) :
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
#%% ini    
    def __init__(self, motLat='',motorTypeName0='', motVert='',motorTypeName1='',nomWin='',nomTilt='',parent=None):
        
        super(TiltMOTORGUI, self).__init__()
        self.motor=[str(motLat),str(motVert)]
        self.motorTypeName=[motorTypeName0,motorTypeName1]
        self.motorType=[0,0]
        self.MOT=[0,0]
        self.configMotName=[0,0]
        self.conf=[0,0]
        self.configPath="./fichiersConfig/"
        self.isWinOpen=False
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setup()
        self.actionButton()
        
        for zi in range (0,2): #• creation list configuration et type de moteurs
            if self.motorTypeName[zi]=='RSAI':
                self.configMotName[zi]=self.configPath+'configMoteurRSAI.ini'
                import moteurRSAI as RSAI
                self.motorType[zi]=RSAI
                self.MOT[zi]=self.motorType[zi].MOTORRSAI(self.motor[zi])
                
            elif self.motorTypeName=='SmartAct':
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
                 print('NewFocus')
                 
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
            else:
                print('Error config motor Type name')
            
            self.conf[zi]=QtCore.QSettings(self.configMotName[zi], QtCore.QSettings.IniFormat) # fichier config motor fichier .ini
        
        
        
        self.setWindowTitle(nomWin) # affichage nom du moteur sur la barre de la fenetre
        # affichage nom du moteur
        #self.show()
        self.stepmotor=[0,0]
        self.butePos=[0,0]
        self.buteNeg=[0,0]
        
        
        for zzi in range(0,2):
            self.stepmotor[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/stepmotor")) #list of stepmotor values for unit conversion
            self.butePos[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteePos")) # list 
            self.buteNeg[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteeneg"))
        
        
        self.unitChangeLat=1
        self.unitChangeVert=1
        
        self.threadLat=PositionThread(mot=self.MOT[0],motorType=self.motorType[0]) # thread pour afficher position Lat
        self.threadLat.POS.connect(self.PositionLat)
        time.sleep(0.1)
        
        self.threadVert=PositionThread(mot=self.MOT[1],motorType=self.motorType[1]) # thread pour afficher position Vert
        self.threadVert.POS.connect(self.PositionVert)
        
        
    def setup(self):
        
        vbox1=QVBoxLayout() 
        
        hbox1=QHBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(0)
        grid_layout.setHorizontalSpacing(10)
        self.haut=QPushButton('Haut')
        self.haut.setMinimumHeight(60)
        
        self.bas=QPushButton('Bas')
        self.bas.setMinimumHeight(60)
        self.gauche=QPushButton('Gauche')
        self.gauche.setMinimumHeight(60)
        self.gauche.setMinimumWidth(60)
        self.droite=QPushButton('Droite')
        self.droite.setMinimumHeight(60)
        self.droite.setMinimumWidth(60)
        self.jogStep=QSpinBox()
        self.jogStep.setMaximum(10000)
        grid_layout.addWidget(self.haut, 0, 1)
        grid_layout.addWidget(self.bas,2,1)
        grid_layout.addWidget(self.gauche, 1, 0)
        grid_layout.addWidget(self.droite, 1, 2)
        grid_layout.addWidget(self.jogStep,1,1)
        hbox1.addLayout(grid_layout)
        vbox1.addLayout(hbox1)
        posLAT=QLabel('Lateral:')
        posLAT.setMaximumHeight(20)
        posVERT=QLabel('Vertical :')
        posVERT.setMaximumHeight(20)
        hbox2=QHBoxLayout()
        hbox2.addWidget(posLAT)
        hbox2.addWidget(posVERT)
        vbox1.addLayout(hbox2)
        
        self.position_Lat=QLabel('pos')
        self.position_Lat.setMaximumHeight(20)
        self.position_Vert=QLabel('pos')
        self.position_Vert.setMaximumHeight(20)
        hbox3=QHBoxLayout()
        hbox3.addWidget(self.position_Lat)
        
        hbox3.addWidget(self.position_Vert)
        vbox1.addLayout(hbox3)
        
        hbox4=QHBoxLayout()
        self.zeroButtonLat=QPushButton('Zero Lat')
        self.zeroButtonVert=QPushButton('Zero Vert')
        
        hbox4.addWidget(self.zeroButtonLat)
        hbox4.addWidget(self.zeroButtonVert)
        vbox1.addLayout(hbox4)
        
        self.stopButton=QPushButton('STOP')
        hbox5=QHBoxLayout()
        hbox5.addWidget(self.stopButton)
        vbox1.addLayout(hbox5)
        self.setLayout(vbox1)       
        
#%% Start threads       
    def startThread2(self):
        self.threadLat.ThreadINIT()
        self.threadLat.start()
        time.sleep(0.5)
        self.threadVert.ThreadINIT()
        self.threadVert.start()
        
        
#%% SETUP       
    def actionButton(self):
        '''
           Definition des boutons 
        '''
       
        self.haut.clicked.connect(self.hMove) # jog haut
        self.haut.setAutoRepeat(False)
        self.bas.clicked.connect(self.bMove) # jog bas
        self.bas.setAutoRepeat(False)
        self.gauche.clicked.connect(self.gMove)
        self.gauche.setAutoRepeat(False)
        self.droite.clicked.connect(self.dMove)
        self.droite.setAutoRepeat(False)
                
        self.zeroButtonLat.clicked.connect(self.ZeroLat)# remet a zero l'affichage
        self.zeroButtonVert.clicked.connect(self.ZeroVert)
        
        #self.refZeroButton.clicked.connect(self.RefMark) # va en butée et fait un zero

        self.stopButton.clicked.connect(self.StopMot)# arret moteur
       
 #%% Def des actions des bouttons       
    def closeEvent(self, event):
        """ 
        When closing the window
        """
        self.fini()
        time.sleep(0.1)
        event.accept()
            

    def gMove(self):
        '''
        action bouton left
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeLat)
        b=self.MOT[0].position()
        if b-a<self.buteNeg[0] :
            print( "STOP : Butée Positive")
            self.MOT[0].stopMotor()
        elif b-a>self.butePos[0] :
            print( "STOP : Butée Négative")
            self.MOT[0].stopMotor()
        else :
            self.MOT[0].rmove(-a)
            
    def dMove(self):
        '''
        action bouton left
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeLat)
        b=self.MOT[0].position()
        if b-a<self.buteNeg[0] :
            print( "STOP : Butée Positive")
            self.MOT[0].stopMotor()
        elif b-a>self.butePos[0] :
            print( "STOP : Butée Négative")
            self.MOT[0].stopMotor()
        else :
            self.MOT[0].rmove(a)
        
    def hMove(self): 
        '''
        action bouton up
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeVert)
        b=self.MOT[1].position()
        if b-a<self.buteNeg[1] :
            print( "STOP : Butée Positive")
            self.MOT[1].stopMotor()
        elif b-a>self.butePos[1] :
            print( "STOP : Butée Négative")
            self.MOT[1].stopMotor()
        else :
            self.MOT[1].rmove(a)   
        
        
    def bMove(self):
        '''
        action bouton up
        '''
        a=float(self.jogStep.value())
        a=float(a*self.unitChangeVert)
        b=self.MOT[1].position()
        if b-a<self.buteNeg[1] :
            print( "STOP : Butée Positive")
            self.MOT[1].stopMotor()
        elif b-a>self.butePos[1] :
            print( "STOP : Butée Négative")
            self.MOT[1].stopMotor()
        else :
            self.MOT[1].rmove(-a)           
        
    def ZeroLat(self): # remet le compteur a zero 
        self.MOT[0].setzero()
    def ZeroVert(self): # remet le compteur a zero 
        self.MOT[1].setzero()
 

    def RefMark(self): # Va en buttée et fait un zero
        """
            a faire ....
        """
        #self.motorType.refMark(self.motor)
   

    def StopMot(self):
        '''
        stop les moteurs
        '''
        for zzi in range(0,2):
            self.MOT[zzi].stopMotor();

    def PositionLat(self,Posi):
        ''' 
        affichage de la position a l aide du second thread
        '''
        a=float(Posi)
       
        a=a/self.unitChangeLat # valeur tenant compte du changement d'unite
        self.position_Lat.setText(str(round(a,2))) 
       
    def PositionVert(self,Posi): 
        ''' 
        affichage de la position a l aide du second thread
        '''
        a=float(Posi)
    
        a=a/self.unitChangeVert # valeur tenant compte du changement d'unite
        self.position_Vert.setText(str(round(a,2))) 
      
    def fini(self): 
        '''
        a la fermeture de la fenetre on arrete le thread secondaire
        '''
        self.threadLat.stopThread()
        self.threadVert.stopThread()
        self.isWinOpen=False
        time.sleep(0.1)    

#
#
#%%######Position Thread    
class PositionThread(QtCore.QThread):
    '''
    thread secondaire pour afficher la position
    '''
    import time #?
    POS=QtCore.pyqtSignal(float) # signal transmit par le second thread au thread principal pour aff la position
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
                time.sleep(0.2)
                Posi=(self.MOT.position())
                try :
                    time.sleep(1)
                    self.POS.emit(Posi)
                   
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
    #mot6=MOTORGUI(motor,motorTypeName='Servo')
    mot5=TiltMOTORGUI( motLat='NF_Lat', motorTypeName0='NewFocus', motVert='NF_Vert', motorTypeName1='NewFocus', nomWin='Tilts Sample ', nomTilt='Tilts Sample')
    mot5.show()
    mot5.startThread2()
    appli.exec_()
    


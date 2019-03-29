# -*- coding: utf-8 -*-
"""
Interface Graphique pour le pilotage d'un moteur 
Controleurs possible : A2V RSAI NewFocus SmartAct ,rack newport
Thread secondaire pour afficher les positions
memorisation de 4 positions
python 3.X PyQt5 
System 32 bit (at least python MSC v.1900 32 bit (Intel)) 
@author: Gautier julien loa
Created on Tue Jan 4 10:42:10 2018
Modified on Mon july 16  10:49:32 2018
"""
#%%
from PyQt5 import QtCore,uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QMessageBox
import time
import sys
PY = sys.version_info[0]
if PY<3:
    print('wrong version of python : Python 3.X must be used')
#%%
class MOTORGUI(QWidget) :
    """
    User interface Motor class : 
    MOTOGUI(str(mot1), str(motorTypeName)  )
    mot1= :  'name of the motor' (child group of the ini file)
    motorTypeName= Controler name  : 'RSAI' or 'A2V' or 'NewFocus' or 'SmartAct' or 'Newport' , Servo, Arduino
    fichier de config des moteurs : 'configMoteurRSAI.ini' 'configMoteurA2V.ini' 'configMoteurNewFocus.ini' 'configMoteurSmartAct.ini'
    """
    
    def __init__(self, mot1='',motorTypeName='',parent=None):
        
        super(MOTORGUI, self).__init__()
        self.motor=str(mot1)
#        print('motor name:',self.motor)
#        print('motor type:',motorTypeName)
        self.isWinOpen=False
        guiName='GuiOneMotor.ui'
        self.motorTypeName=motorTypeName
        
        if motorTypeName=='RSAI':
            configMotName='configMoteurRSAI.ini'
            import moteurRSAI as RSAI
            self.motorType=RSAI
            self.MOT=self.motorType.MOTORRSAI(self.motor)
            
        elif motorTypeName=='SmartAct':
             configMotName='configMoteurSmartAct.ini'
             import smartactmot as SmartAct
             self.motorType=SmartAct
             self.MOT=self.motorType.MOTORSMART(self.motor)
             
        elif motorTypeName=='A2V':
             configMotName='configMoteurA2V.ini'
             import moteurA2V  as A2V
             self.motorType=A2V
             self.MOT=self.motorType.MOTORA2V(self.motor)
             
        elif motorTypeName=='NewFocus':
             configMotName='configMoteurNewFocus.ini'
             import moteurNewFocus as NewFoc
             self.motorType=NewFoc
             self.MOT=self.motorType.MOTORNEWFOCUS(self.motor)
             
        elif motorTypeName=='newport':
             configMotName='confNewport.ini'
             import newportMotors as Newport
             self.motorType=Newport
             self.MOT=self.motorType.MOTORNEWPORT(self.motor)
             
        elif motorTypeName=='Servo':
             configMotName='configMoteurServo.ini'
             import servo as servo
             self.motorType=servo
             self.MOT=self.motorType.MOTORSERVO(self.motor)
             
        elif motorTypeName=='Arduino':
             configMotName='configMoteurArduino.ini'
             import moteurArduino as arduino
             self.motorType=arduino
             self.MOT=self.motorType.MOTORARDUINO(self.motor)
             
        else:
            print('Error config motor Type name')
            
        configMotName="C:/Users/loa/Desktop/MoteursV7/fichiersConfig/"+ configMotName  
        self.conf=QtCore.QSettings(configMotName, QtCore.QSettings.IniFormat) # fichier config motor fichier .ini
        self.win=uic.loadUi(guiName,self)
        
        
        self.stepmotor=float(self.conf.value(self.motor+"/stepmotor"))
        self.butePos=float(self.conf.value(self.motor+"/buteePos"))
        self.buteNeg=float(self.conf.value(self.motor+"/buteeneg"))
        self.unitF()
        
        self.thread2=PositionThread(mot=self.MOT,motorType=self.motorType) # thread pour afficher position
        self.thread2.POS.connect(self.Position)
        
        self.absRef=[self.ABSref1,self.ABSref2,self.ABSref3,self.ABSref4] # pour les positions
        self.posText=[self.posText1,self.posText2,self.posText3,self.posText4]
        self.POS=[self.Pos1,self.Pos2,self.Pos3,self.Pos4]
        self.Take=[self.take1,self.take2,self.take3,self.take4]
        self.setup()
    
    def startThread2(self):
        self.thread2.ThreadINIT()
        self.thread2.start()
        
    def setup(self):
        ## def des boutons 
        self.setWindowTitle(str(self.conf.value(self.motor+"/Name")))# affichage nom du moteur sur la barre de la fenetre
        self.Nom.setText(str(self.conf.value(self.motor+"/Name"))) # affichage nom du moteur
        self.unit.currentIndexChanged.connect(self.unitF) # Chg unités
        self.rMoveButton.clicked.connect(self.rMove) # Mvt relatif
        self.plus.clicked.connect(self.pMove) # jog +
        self.plus.setAutoRepeat(True)
        self.moins.clicked.connect(self.mMove)# jog -
        self.moins.setAutoRepeat(True) 
        self.speedButton.stateChanged.connect(self.Speed) # vitesse
        self.MoveButton.clicked.connect(self.Move) # Mvt Absolue
        self.zeroButton.clicked.connect(self.Zero) # remet a zero l'affichage
        self.refZeroButton.clicked.connect(self.RefMark) # va en butée et fait un zero
        self.zeroButton.clicked.connect(self.Zero) # remet a zero l'affichage
        self.stopButton.clicked.connect(self.StopMot)# arret moteur
        self.Slow.setValue(int(self.conf.value(self.motor+"/velocitySlow"))) # Valeur de la vitesse lente ou rapide
        self.Slow.valueChanged.connect(self.slowchange) # changement vitesse lente
        self.Fast.setValue(int(self.conf.value(self.motor+"/velocityFast")))
        self.Fast.valueChanged.connect(self.fastchange)
        iii=1
        for saveNameButton in self.posText: # nom de la refference
            nbRef=str(iii)
            saveNameButton.textChanged.connect(self.savName)
            saveNameButton.setText(str(self.conf.value(self.motor+"/ref"+nbRef+"Name"))) # ecrit le nom de la ref
            iii+=1        
        for posButton in self.POS: # button GO
            posButton.clicked.connect(self.ref)    # Va à la valeur de la ref
        eee=1   
        for absButton in self.absRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf.value(self.motor+"/ref"+nbRef+"Pos"))) # ecrit la valeur de la ref
            absButton.valueChanged.connect(self.savRef) # sauv la valeur
            eee+=1
        for takeButton in self.Take:
            takeButton.clicked.connect(self.take) # prend la valeur 
        
        
    def closeEvent(self, event):
        """ when closing the window
        """
        self.fini()
        time.sleep(0.1)
        event.accept()
            
    def Move(self):  # Action du buton absolute move
        a=float(self.MoveStep.value())
        a=float(a*self.unitChange) # changement d unite
        if a<self.buteNeg :
            print( "STOP : Butée Négative")
            self.MOT.stopMotor()
        elif a>self.butePos :
            print( "STOP : Butée Positive")
            self.MOT.stopMotor()
        else :
            self.MOT.move(a)
        
    def rMove(self): # action mvt en relatif
        a=float(self.rMoveStep.value())
        a=float(a*self.unitChange)
        b=self.MOT.position()
        if b+a<self.buteNeg :
            print ("STOP : Butée Positive")
            self.MOT.stopMotor()
        elif b+a>self.butePos :
            print( "STOP : Butée Négative")
            self.MOT.stopMotor()
        else :
            self.MOT.rmove(a)
        
    def pMove(self):# action jog +
        print('jog+')
        a=float(self.jogStep.value())
        print(a)
        a=float(a*self.unitChange)
        b=self.MOT.position()
        if b+a<self.buteNeg :
            print( "STOP : Butée Positive")
            self.MOT.stopMotor()
        elif b+a>self.butePos :
            print( "STOP : Butée Négative")
            self.MOT.stopMotor()
        else :
            self.MOT.rmove(a)

    def mMove(self): # action jog -
        a=float(self.jogStep.value())
        a=float(a*self.unitChange)
        b=self.MOT.position()
        if b-a<self.buteNeg :
            print( "STOP : Butée Positive")
            self.MOT.stopMotor()
        elif b-a>self.butePos :
            print( "STOP : Butée Négative")
            self.MOT.stopMotor()
        else :
            self.MOT.rmove(-a)
        
    def speedfast(self):
        fast=int(self.Fast.value())
        vit=fast
        return vit
    
    def speedslow(self):
        slow=int(self.Slow.value())
        vit=slow
        return vit
    
    def Speed(self): # action choix vitesse lente ou rapide
        if self.speedButton.isChecked()==1:
            vit=self.speedfast()
        else:
            vit=self.speedslow()
        return vit

    def slowchange (self): #  action si changement de vitesse
        self.conf.setValue(self.motor+"/velocitySlow",self.Slow.value())
        self.conf.sync()
        self.Slow.setValue(self.conf.value(self.motor+"/velocitySlow"))
        if self.speedButton.isChecked()==0:
            self.speedslow() 
            
    def fastchange (self): #  action si changement de vitesse
        self.conf.setValue(motor+"/velocityFast",self.Fast.value())
        self.conf.sync()
        self.Fast.setValue(self.conf.value(self.motor+"/velocityFast"))
        if self.speedButton.isChecked()==1: # si Fast est coché ca change la vitesse
            self.speedfast() # evite de cocher decocher la case
            
    def Zero(self): # remet le compteur a zero 
        self.MOT.setzero()

    def RefMark(self): # Va en buttée et fait un zero
        """
            a faire ....
        """
        #self.motorType.refMark(self.motor)
    
    def unitF(self): # chg d'unité
        ii=self.unit.currentIndex()
        if ii==0: # en micron
            self.unitChange=float((1*self.stepmotor))
            self.unit.setStyleSheet("color: rgb(0, 0, 0)")  ;
            self.win.positionVal.setStyleSheet("color: rgb(0, 0, 0)")
            
        if ii==1: # en mm
            self.unitChange=float((1000*self.stepmotor))  
            self.unit.setStyleSheet("color: rgb(255, 0, 0)")  ;
            self.win.positionVal.setStyleSheet("color: rgb(255, 0, 0)")
            
        if ii==2: # en ps tient en compte le double passage : 1 microns=6fs
            self.unitChange=float(1*self.stepmotor/0.0066666666)
            self.unit.setStyleSheet("color: rgb(0, 255, 0)")
            self.win.positionVal.setStyleSheet("color: rgb(0, 255, 0)")
            
        if ii==3: # en step
            self.unitChange=1    
            self.unit.setStyleSheet("color: rgb(170, 0, 255)")
            self.win.positionVal.setStyleSheet("color: rgb(170, 0, 255)")
            
        if self.unitChange==0:
            self.unitChange=1 #evite de diviser par 0
         
    
    def StopMot(self): # stop le moteur
       self.MOT.stopMotor();

    def Position(self,Posi): # affichage de la position a l aide du second thread
        
        a=float(Posi)
        b=a # valeur en pas moteur pour sauvegarder en pas 
        a=round(a/self.unitChange,3) # valeur tenant compte du changement d'unite
        self.win.positionVal.setText(str(a)) 
        positionConnue=0 # evite l affichage de ? dans la boucle for
        precis=1
        if self.motorTypeName=='SmartAct':
            precis=10000
        for nbRefInt in range(1,5):
            nbRef=str(nbRefInt)
            if float(self.conf.value(self.motor+"/ref"+nbRef+"Pos"))-precis<b< float(self.conf.value(self.motor+"/ref"+nbRef+"Pos"))+precis:
                self.enPosition.setText(str(self.conf.value(self.motor+"/ref"+nbRef+"Name")))
                positionConnue=1
        if positionConnue==0:
            self.enPosition.setText('?' )

    def fini(self): # a la fermeture de la fenetre on arrete le thread secondaire
        self.thread2.stopThread()
        self.isWinOpen=False
        time.sleep(0.1)    
    
#%% Action des Bouttons pour definir des positions de references################################################
    
    def take (self) : 
        # Prend la valeur de la reference et la sauvegarde
        sender=QtCore.QObject.sender(self) # prend le nom du bouton cliquer
        reply=QMessageBox.question(None,'Save Position ?',"Do you want to save this position ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:

            tpos=self.MOT.position()
            nbRef=str(sender.objectName()[4])
            self.conf.setValue(self.motor+"/ref"+nbRef+"Pos",tpos)
            self.conf.sync()
            print ("Position save")
            self.absRef[int(nbRef)-1].setValue(tpos)

    def ref(self):  
        # Fait bouger le moteur a la valeur de reference en step : bouton Go 
        sender=QtCore.QObject.sender(self)
        reply=QMessageBox.question(None,'Go to this Position ?',"Do you want to GO to this position ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            nbRef=str(sender.objectName()[3])
            vref=int(self.conf.value(self.motor+"/ref"+nbRef+"Pos"))
            vit=self.Speed()
            if vref<self.buteNeg :
                print( "STOP : butee negative")
                self.MOT.stopMotor()
            elif vref>self.butePos :
                print( "STOP : butte positive")
                self.MOT.stopMotor()
            else :
                self.MOT.move(vref,vit)

    def savName(self) :
        #Sauvegarde du nom de la ref
        sender=QtCore.QObject.sender(self)
        nbRef=sender.objectName()[7] #PosTExt1
        vname=self.posText[int(nbRef)-1].text()
        self.conf.setValue(self.motor+"/ref"+nbRef+"Name",str(vname))
        self.conf.sync()

    def savRef (self) :
        # Sauvegarde la valeur de la ref si elle change
        sender=QtCore.QObject.sender(self)
        nbRef=sender.objectName()[6] # nom du button ABSref1
        vref=int(self.absRef[int(nbRef)-1].value())
        self.conf.setValue(self.motor+"/ref"+nbRef+"Pos",vref)
        self.conf.sync()


#%%#################################################################################       
class PositionThread(QtCore.QThread):
    ### thread secondaire pour afficher la position
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
    motor='Cible_Trans_Lat'
    motorTypeName='RSAI'
    appli=QApplication(sys.argv)
    #mot6=MOTORGUI(motor,motorTypeName='Servo')
    mot5=MOTORGUI(motor,motorTypeName)
    mot5.startThread2()
    mot5.show()
    appli.exec_()
    


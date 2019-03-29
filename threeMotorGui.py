# -*- coding: utf-8 -*-
"""
Interface Graphique pour le pilotage de trois moteurs
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
class THREEMOTORGUI(QWidget) :
    """
    User interface Motor class : 
    MOTOGUI(str(mot1), str(motorTypeName),str(mot2), str(motorTypeName),str(mot3), str(motorTypeName) nomWin,nomTilt,nomFoc )
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
        
        self.configPath="C:/Users/loa/Desktop/MoteursV7/fichiersConfig/"
        self.isWinOpen=False
        guiName='GuiThreeMotors.ui'
        
        for zi in range (0,3): #• creation list configuration et type de moteurs
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
        
        
        self.win=uic.loadUi(guiName,self)
        self.setWindowTitle(nomWin) # affichage nom du moteur sur la barre de la fenetre
        self.nomTilt.setText(str(nomTilt)) # affichage nom du moteur
        self.nomFoc.setText(str(nomFoc))
        
        self.stepmotor=[0,0,0]
        self.butePos=[0,0,0]
        self.buteNeg=[0,0,0]
        
        for zzi in range(0,3):
            self.stepmotor[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/stepmotor")) #list of stepmotor values for unit conversion
            self.butePos[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteePos")) # list 
            self.buteNeg[zzi]=float(self.conf[zzi].value(self.motor[zzi]+"/buteeneg"))
        
        self.unitFoc()
        self.unitTrans()
        
        self.threadLat=PositionThread(mot=self.MOT[0],motorType=self.motorType[0]) # thread pour afficher position Lat
        self.threadLat.POS.connect(self.PositionLat)
        
        
        self.threadVert=PositionThread(mot=self.MOT[1],motorType=self.motorType[1]) # thread pour afficher position Vert
        self.threadVert.POS.connect(self.PositionVert)
        
        
        self.threadFoc=PositionThread(mot=self.MOT[2],motorType=self.motorType[2]) # thread pour afficher position Foc
        self.threadFoc.POS.connect(self.PositionFoc)
        
        
        self.absLatRef=[self.ABSLatref1,self.ABSLatref2,self.ABSLatref3,self.ABSLatref4,self.ABSLatref5] 
        self.absVertRef=[self.ABSVertref1,self.ABSVertref2,self.ABSVertref3,self.ABSVertref4,self.ABSVertref5]
        self.absFocRef=[self.ABSFocref1,self.ABSFocref2,self.ABSFocref3,self.ABSFocref4,self.ABSFocref5] # pour memoriser les positions
        self.posText=[self.posText1,self.posText2,self.posText3,self.posText4,self.posText5]
        self.POS=[self.Pos1,self.Pos2,self.Pos3,self.Pos4,self.Pos5]
        self.Take=[self.take1,self.take2,self.take3,self.take4,self.take5]
        
        self.setup()
#   
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
        '''
           Definition des boutons 
        '''
        self.unitFocBouton.currentIndexChanged.connect(self.unitFoc) # Chg unités Foc
        self.unitTransBouton.currentIndexChanged.connect(self.unitTrans) # Chg unités Trnas
        
        self.haut.clicked.connect(self.hMove) # jog haut
        self.haut.setAutoRepeat(False)
        self.bas.clicked.connect(self.bMove) # jog bas
        self.bas.setAutoRepeat(False)
        self.gauche.clicked.connect(self.gMove)
        self.gauche.setAutoRepeat(False)
        self.droite.clicked.connect(self.dMove)
        self.droite.setAutoRepeat(False)
        
        self.plus.clicked.connect(self.pMove) # jog + foc
        self.plus.setAutoRepeat(False)
        self.moins.clicked.connect(self.mMove)# jog -
        self.moins.setAutoRepeat(False) 
        self.AbsMove.clicked.connect(self.Move)
                
        self.zeroButtonFoc.clicked.connect(self.ZeroFoc)
        self.zeroButtonLat.clicked.connect(self.ZeroLat)# remet a zero l'affichage
        self.zeroButtonVert.clicked.connect(self.ZeroVert)
        
        #self.refZeroButton.clicked.connect(self.RefMark) # va en butée et fait un zero
        
        self.stopButton.clicked.connect(self.StopMot)# arret moteur
       
        iii=1
        for saveNameButton in self.posText: # nom de la refference
            nbRef=str(iii)
            saveNameButton.textChanged.connect(self.savName)
            saveNameButton.setText(str(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Name"))) # ecrit le nom de la ref
            iii+=1        
        for posButton in self.POS: # button GO
            posButton.clicked.connect(self.ref)    # Va à la valeur de la ref
        eee=1   
        for absButton in self.absLatRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[0].value(self.motor[0]+"/ref"+nbRef+"Pos"))) # ecrit la valeur de la ref
            absButton.valueChanged.connect(self.savRefLat) # sauv la valeur
            eee+=1
        eee=1     
        for absButton in self.absVertRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[1].value(self.motor[1]+"/ref"+nbRef+"Pos"))) # ecrit la valeur de la ref
            absButton.valueChanged.connect(self.savRefVert) # sauv la valeur
            eee+=1
        eee=1     
        for absButton in self.absFocRef: 
            nbRef=str(eee)
            absButton.setValue(int(self.conf[2].value(self.motor[2]+"/ref"+nbRef+"Pos"))) # ecrit la valeur de la ref
            absButton.valueChanged.connect(self.savRefFoc) # sauv la valeur
            eee+=1
            
        for takeButton in self.Take:
            takeButton.clicked.connect(self.take) # prend la valeur 
        
        
    def closeEvent(self, event):
        """ 
        When closing the window
        """
        self.fini()
        time.sleep(0.1)
        event.accept()
            
    def Move(self): 
        '''
        Action du buton absolute move pour le mot2 (foc)
        '''
        a=float(self.MoveVal.value())
        a=float(a*self.unitChangeFoc) # changement d unite
        print(0,'moveabs')
        if a<self.buteNeg[2] :
            print( "STOP : Butée Négative")
            self.MOT.stopMotor()
        elif a>self.butePos[2] :
            print( "STOP : Butée Positive")
            self.MOT[2].stopMotor()
        else :
            self.MOT[2].move(int(a))

       
    def pMove(self):
        '''
        action jog + foc 
        '''
        a=float(self.jogStep_2.value())
        print(a)
        a=float(a*self.unitChangeFoc)
        b=self.MOT[2].position()
        if b+a<self.buteNeg[2] :
            print( "STOP : Butée Positive")
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
            print( "STOP : Butée Positive")
            self.MOT[2].stopMotor()
        elif b-a>self.butePos[2] :
            print( "STOP : Butée Négative")
            self.MOT[2].stopMotor()
        else :
            self.MOT[2].rmove(-a)


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
            self.MOT[0].rmove(a)
            
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
            self.MOT[0].rmove(-a)
        
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
    def ZeroFoc(self): # remet le compteur a zero 
        self.MOT[2].setzero()

    def RefMark(self): # Va en buttée et fait un zero
        """
            a faire ....
        """
        #self.motorType.refMark(self.motor)
   
    def unitFoc(self):
        '''
        chg d'unité mot foc
        '''
        ii=self.unitFocBouton.currentIndex()
        if ii==0: # en step
            self.unitChangeFoc=1
        if ii==1: # en micron
            self.unitChangeFoc=float((1*self.stepmotor[2]))  
        if ii==2: # en mm 
            self.unitChangeFoc=float((1000*self.stepmotor[2]))
        if ii==3: # en ps tient en compte le double passage : 1 microns=6fs
            self.unitChangeFoc=float(1*self.stepmotor[2]/0.0066666666)    
        if self.unitChangeFoc==0:
            self.unitChangeFoc=1 #evite de diviser par 0

    def unitTrans(self):
        '''
         chg d'unité mot foc
        '''
        ii=self.unitTransBouton.currentIndex()
        if ii==0: # en step
            self.unitChangeLat=1
            self.unitChangeVert=1
        if ii==1: # en micron
            self.unitChangeLat=float((1*self.stepmotor[0]))  
            self.unitChangeVert=float((1*self.stepmotor[1]))  
        if ii==2: 
            self.unitChangeLat=float((1000*self.stepmotor[0]))
            self.unitChangeVert=float((1000*self.stepmotor[1]))
        if ii==3: # en ps  en compte le double passage : 1 microns=6fs
            self.unitChangeLat=float(1*self.stepmotor[0]/0.0066666666)  
            self.unitChangeVert=float(1*self.stepmotor[1]/0.0066666666)  
        if self.unitChangeLat==0:
            self.unitChangeLat=1 #evite de diviser par 0
        if self.unitChangeVert==0:
            self.unitChangeVert=1 #evite de diviser par 0
    
    def StopMot(self):
        '''
        stop les moteurs
        '''
        for zzi in range(0,3):
            self.MOT[zzi].stopMotor();

    def PositionLat(self,Posi):
        ''' 
        affichage de la position a l aide du second thread
        '''
        a=float(Posi)
        b=a # valeur en pas moteur 
        a=a/self.unitChangeLat # valeur tenant compte du changement d'unite
        self.win.position_Lat.setText(str(round(a,2))) 
        positionConnue_Lat=0 # evite l affichage de ? dans la boucle for
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
        affichage de la position a l aide du second thread
        '''
        a=float(Posi)
        b=a # valeur en pas moteur 
        a=a/self.unitChangeVert # valeur tenant compte du changement d'unite
        self.win.position_Vert.setText(str(round(a,2))) 
        positionConnue_Vert=0 # evite l affichage de ? dans la boucle for
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
        affichage de la position a l aide du second thread
        '''
        a=float(Posi)
        b=a # valeur en pas moteur
        a=a/self.unitChangeFoc # valeur tenant compte du changement d'unite
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
        
    def fini(self): 
        '''
        a la fermeture de la fenetre on arrete le thread secondaire
        '''
        self.threadLat.stopThread()
        self.threadVert.stopThread()
        self.threadFoc.stopThread()
        self.isWinOpen=False
        time.sleep(0.1)    
#    
##%% Action des Bouttons pour definir des positions de references################################################
#    
    def take (self) : 
        ''' 
        Prend la valeur de la reference et la sauvegarde
        '''
        sender=QtCore.QObject.sender(self) # prend le nom du bouton cliquer
        reply=QMessageBox.question(None,'Save Position ?',"Do you want to save this position ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
               tposLat=self.MOT[0].position()
               nbRef=str(sender.objectName()[4])
               self.conf[0].setValue(self.motor[0]+"/ref"+nbRef+"Pos",tposLat)
               self.conf[0].sync()
               self.absLatRef[int(nbRef)-1].setValue(tposLat)
               print ("Position Lat save")
               tposVert=self.MOT[1].position()
               
               self.conf[1].setValue(self.motor[1]+"/ref"+nbRef+"Pos",tposVert)
               self.conf[1].sync()
               self.absVertRef[int(nbRef)-1].setValue(tposVert)
               print ("Position Vert save")
               tposFoc=self.MOT[2].position()
               print('tposFoc',tposFoc)
               self.conf[2].setValue(self.motor[2]+"/ref"+nbRef+"Pos",tposFoc)
               self.conf[2].sync()
               self.absFocRef[int(nbRef)-1].setValue(tposFoc)
               print ("Position Foc save")
#
    def ref(self):  
        '''
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
                    print( "STOP : butee negative")
                    self.MOT[i].stopMotor()
                elif vref>self.butePos[i] :
                    print( "STOP : butte positive")
                    self.MOT[i].stopMotor()
                else :
                    self.MOT[i].move(vref)
#
    def savName(self) :
        '''
        Sauvegarde du nom de la ref
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
        Sauvegarde la valeur de la ref si Lat change
        '''
        sender=QtCore.QObject.sender(self)
        nbRefLat=sender.objectName()[9] # nom du button ABSref1
        print('nbref=',nbRefLat)
        vrefLat=int(self.absLatRef[int(nbRefLat)-1].value())
        self.conf[0].setValue(self.motor[0]+"/ref"+nbRefLat+"Pos",vrefLat)
        self.conf[0].sync()
        
    def savRefVert (self) : 
        '''
        Sauvegarde la valeur de la ref si Vert change
        '''
        sender=QtCore.QObject.sender(self)
        nbRefVert=sender.objectName()[10] 
        vrefVert=int(self.absVertRef[int(nbRefVert)-1].value())
        self.conf[1].setValue(self.motor[1]+"/ref"+nbRefVert+"Pos",vrefVert)
        self.conf[1].sync()
        
    def savRefFoc (self) :
        '''
        Sauvegarde la valeur de la ref si Foc change
        '''
        sender=QtCore.QObject.sender(self)
        nbRefFoc=sender.objectName()[9] 
        vrefFoc=int(self.absLatRef[int(nbRefFoc)-1].value())
        self.conf[2].setValue(self.motor[2]+"/ref"+nbRefFoc+"Pos",vrefFoc)
        self.conf[2].sync()
#
#
#%%#################################################################################       
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
    


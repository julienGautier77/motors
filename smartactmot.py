# -*- coding: utf-8
""" Control des moteurs smartact ##
utilise la dll MSCControl.dll presente dans le meme repertoire
python 3.X and PyQt5
@author: Gautier julien loa
Created on Tue Feb 27 15:49:32 2018
"""

#%% Imports
try:
    from PyQt6.QtCore import QSettings
    from PyQt6 import uic,QtCore
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtWidgets import QMessageBox
    import time
except:
    print("error QT6import")

import ctypes
import sys

#%% import dll with cdll et non windll sinon error 4 bytes in excess (cf :https://ammous88.wordpress.com/2014/12/31/ctypes-cdll-vs-windll/)
dll_file = 'DLL/MCSControl' 

confSmart = QSettings('./fichiersConfig/configMoteurSmartAct.ini', QSettings.Format.IniFormat) # motor configuration  files

configuration=ctypes.c_uint32(0) 

#configuration flags for SA_InitDevices : 
#define SA_SYNCHRONOUS_COMMUNICATION            0
#define SA_ASYNCHRONOUS_COMMUNICATION           1
#define SA_HARDWARE_RESET                       2

#SA_Status=SMART.SA_InitSystems(ctypes.pointer(ctypes.c_uint(2)) )
#print "Hardware RESET :",SA_Status
#version=ctypes.c_uint(0)
#vers=SMART.SA_GetDLLVersion(ctypes.pointer(version))
#print version

SMART = ctypes.cdll.LoadLibrary(dll_file)  #
zz=SMART.SA_ClearInitSystemsList()
#SA_Status=SMART.SA_InitSystems(ctypes.pointer(ctypes.c_uint(2)) )
#idlist=ctypes.c_uint32()
#idlistsize=ctypes.c_uint32()
#status=SMART.SA_GetAvailableSystems(idlist,idlistsize)
#print (status,idlist,idlistsize)


aa=SMART.SA_AddSystemToInitSystemsList(ctypes.c_ulong(2565091029))
bb=SMART.SA_AddSystemToInitSystemsList(ctypes.c_ulong(3504615125))
cc=SMART.SA_AddSystemToInitSystemsList(ctypes.c_ulong(316944085))


SA_Status=SMART.SA_InitSystems(ctypes.pointer(configuration))


nbS=ctypes.c_int()
SA_nbSys=SMART.SA_GetNumberOfSystems(ctypes.pointer(nbS))
print ("SmartAct initialisation ...")

if nbS.value<1:
    SMART.SA_ReleaseSystems() # Deconnexion
    print ("Controller not connected")
    SA_Status=SMART.SA_InitSystems(ctypes.pointer(configuration))
if SA_Status==0:
    print ("SmartAct Intitialisation  : OK!!!")
    print( "Number of SmartAct controller connected : ",nbS.value)
    in0=ctypes.c_ulong(0)
    in1=ctypes.c_ulong(1)
    in2=ctypes.c_ulong(2)
    inS=ctypes.c_ulong()
    sys0=ctypes.c_ulong()
    sys1=ctypes.c_ulong()
    sys2=ctypes.c_ulong()
    
    sysid0=SMART.SA_GetSystemID(in0,ctypes.pointer(sys0))
    sysid1=SMART.SA_GetSystemID(in1,ctypes.pointer(sys1))
    sysid2=SMART.SA_GetSystemID(in2,ctypes.pointer(sys2))
    print ("sytemsIndex 0 ID:",sys0.value)
    print ("sytemsIndex 1 ID:",sys1.value)
    print ("sytemsIndex 2 ID:",sys2.value)
#    if nbS.value<4:
#            msg = QMessageBox()
#            msg.setIcon(QMessageBox.Critical)
#            msg.setText("Controler Smartact pb !")
#            msg.setInformativeText("All smart controller are not connected, please reboot... !")
#            msg.setWindowTitle("Warning ...")
#            msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#            msg.exec_()
else : #◙ again a new connexion
    SMART.SA_ReleaseSystems() # Deconnexion
    print( "Deconnexion smartAct")
    print ("Connexion smartAct...")
    SMART.SA_ClearInitSystemsList()
    SMART.SA_AddSystemToInitSystemsList(ctypes.c_ulong(2565091029))
    SMART.SA_AddSystemToInitSystemsList(ctypes.c_ulong(3504615125))
    SMART.SA_AddSystemToInitSystemsList(ctypes.c_ulong(316944085))
    SA_Status=SMART.SA_InitSystems(ctypes.pointer(configuration))
    
    if SA_Status==0:
        print ("Intitialization SmartAct : now OK ")
        in0=ctypes.c_ulong(0)
        in1=ctypes.c_ulong(1)
        inS=ctypes.c_ulong()
        nbS=ctypes.c_int()
        SA_nbSys=SMART.SA_GetNumberOfSystems(ctypes.pointer(nbS))
        print ("Number of SmartAct controller connected :",nbS.value)
        if nbS.value<4:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Controler Smartact pb !")
            msg.setInformativeText("All smart controller are not connected, please reboot... !")
            msg.setWindowTitle("Warning ...")
            msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msg.exec_()
        index1=SMART.SA_GetSystemID(in0,ctypes.pointer(inS))
        index2=SMART.SA_GetSystemID(in1,ctypes.pointer(inS))
        
    else :
       print (" SmartAct not initialized ! ")
       ap=QApplication(sys.argv)
       az=uic.loadUi('attention.ui')
       az.show()
       ap.exec_()


iniState=ctypes.c_uint(0)
SMART.SA_GetInitState(ctypes.pointer(iniState))
print (" dll smartAct state : ",iniState.value)
SA_HCM_DISABLED=0 # enleve l'affichage sur les controleur
SMART.SA_SetHCMEnabled(0,SA_HCM_DISABLED);
SMART.SA_SetHCMEnabled(1,SA_HCM_DISABLED);
SMART.SA_SetHCMEnabled(2,SA_HCM_DISABLED);
print ("HCM Disabled")


def stopConnexion():
    """
    ## Deconnexion
    """
    SA_HCM_DISABLED=1 # remet l'affichage sur les controleur
    print ("SmartAct connexion stopped  : HCM enabled")
    SMART.SA_SetHCMEnabled(0,SA_HCM_DISABLED);
    SMART.SA_SetHCMEnabled(1,SA_HCM_DISABLED);
    SMART.SA_SetHCMEnabled(2,SA_HCM_DISABLED);
    SMART.SA_ReleaseSystems() 

#%%  class MotorSmartAct
class MOTORSMART():
    def __init__(self, mot1='',parent=None):
        self.moteurname=mot1
        self.numControleur=int(confSmart.value(self.moteurname+'/numControleur'))
        self.numMoteur=int(confSmart.value(self.moteurname+'/numMoteur'))
        #SMART.SA_SetClosedLoopMaxFrequency_S(self.numControleur,self.numMoteur,18000)
        #SMART.SA_SetClosedLoopMoveSpeed_S(self.numControleur,self.numMoteur,100000000)
        
    def position(self):
        """
        ## position(motor): Get position actuelle
        """
        
        poss=ctypes.c_int()
        SMART.SA_GetPosition_S(self.numControleur,self.numMoteur,ctypes.pointer(poss))
        #print(poss.value)
        return poss.value

    def stopMotor(self) :
        """
        stopmot(motor) : Stop motor
        """
    
        SMART.SA_Stop_S(self.numControleur,self.numMoteur)
        print( self.moteurname, "STOP")

    def rmove(self,pos,vitesse=10000):
        """
         rmove(motor,pos):Mouvement relatif en nm
        """
        SMART.SA_GotoPositionRelative_S(self.numControleur,self.numMoteur,int(pos),0)
        print (time.strftime("%A %d %B %Y %H:%M:%S"))
        print (self.moteurname, "position before moving :", self.position(),"(step)")
        print (self.moteurname, "relative move of :",pos,"(step)")
        

    def move(self,pos,vitesse=10000):
        """
        ## Mouvement Absolue en nm : move(motor,pos)
        """
        SMART.SA_GotoPositionAbsolute_S(self.numControleur,self.numMoteur,int(pos),0)
        print (time.strftime("%A %d %B %Y %H:%M:%S"))
        print (self.moteurname, "position before moving :", self.position(),"(step)")
        print (self.moteurname, "move at :",pos,"(step)")
    
    def setvelocity(self,v=10000):
        """
        ## setvelocity(motor,velocity): Set Velocity en nm /s
        """
        result = SMART.SA_SetClosedLoopMaxFrequency_S(self.numControleur,self.numMoteur,18000)
        print( "frequency",result)
        if v>100000000:
            print ("vitesse Too Hight !!!")
        else:
            v1=int(v)
            SMART.SA_SetClosedLoopMoveSpeed_S(self.numControleur,self.numMoteur,v1)
            print (self.moteurname,"velocity ", v,"nm/s")
        return v

    def getvelocity(self):
        """
        ## getvelocity(motor):
        """
        velocity=ctypes.c_uint()
        SMART.SA_GetClosedLoopMoveSpeed_S(self.numControleur,self.numMoteur,ctypes.pointer(velocity))
        print ("velocity ", self.moteurname, velocity.value,"nm/s")
        return velocity.value



    def setzero(self):
        """
        ## setzero(motor):Set Zero
        """
        SMART.SA_SetZeroPosition_S(self.numControleur,self.numMoteur)
        print (self.moteurname,"zero set")

    def refMark(self):
        """
        ## refMark(motor): refMark(motor): move to reference Mark  #SA_STATUS SA_FindReferenceMark_S(SA_INDEX systemIndex,SA_INDEX channelIndex,unsigned int direction,unsigned int holdTimeunsigned int autoZero);
        #define SA_FORWARD_DIRECTION                    0
        #define SA_BACKWARD_DIRECTION                   1
        #define SA_FORWARD_BACKWARD_DIRECTION           2
        #define SA_BACKWARD_FORWARD_DIRECTION           3
        """
        SA_FORWARD_DIRECTION=0
        SA_AUTO_ZERO=1 #SA_NO_AUTO_ZERO=0
        SMART.SA_FindReferenceMark_S(self.numControleur,self.numMoteur,SA_FORWARD_DIRECTION,0,SA_AUTO_ZERO)
        print (self.moteurname,"zero set at reference Mark")
    


#%%
if __name__ == "__main__":
    print("test")
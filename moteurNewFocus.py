# -*- coding: utf-8
""" Control des moteurs NewFocus
protocole TC/IP
python 3.X and PyQt5
@author: Gautier julien loa
Created on Wed Feb 28 11:59:41 2018
"""
#%% import
import socket
import time
from PyQt5.QtCore import QSettings

#%% initialisation and connexion
IP='10.0.2.60'
Port=23
bufferSize=1024
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try :
    s.connect((IP,Port))
except:
    print('connexion newFocus error IP')
    
time.sleep(0.1)
try :
    s.send(('*IDN?'+'\n').encode())
    nameFocus=s.recv(bufferSize)
    nameFocus=s.recv(bufferSize)
    #print(nameFocus.decode())
except:
    print('connexion newFocus error')
try:    
    s.send(('IPADDR?'+'\r' +'\n').encode())
    IP_Focus=s.recv(bufferSize)
    print (nameFocus.decode(), "connected @ :",IP_Focus.decode())
except:
    print('connexion newFocus error')
    
def stopConnexion():
    print('stop new Focus')
    s.close()
    
confNewFocus=QSettings('fichiersConfig/configMoteurNewFocus.ini',QSettings.IniFormat)

#%%  class motorNewfocus

class MOTORNEWFOCUS():
    
    def __init__(self, mot1='',parent=None):
        #super(MOTORNEWFOCUS, self).__init__()
        self.moteurname=mot1
        self.numMoteur=str(confNewFocus.value(self.moteurname+'/numMoteur'))
        
        
    def position (self):
        """
        position (motor) : donne la position de motor
        """
        
        s.send((self.numMoteur+'TP?'+'\n').encode())
        pos=s.recv(bufferSize)
        #pos1=pos.decode('utf-8')#.upper()
        return int(pos)

    def stopMotor(self): # stop le moteur motor
        """stopMotor(motor): stop le moteur motor
        """
        
        s.send((self.numMoteur+'ST'+'\n').encode())
        print ("stop", self.moteurname )
        print (self.moteurname, "stopped @", self.position())

    def move(self,pos,vitesse=10000): 
        """
        move(motor,pos): mouvement absolu du moteur (motor) a la position pos 
        """
        print (self.moteurname,"position before ",self.position(),"(step)")
       
        s.send((self.numMoteur+'PA'+str(pos) +'\n').encode())
        print (self.moteurname, "absolu move  to",pos,"(step)")

    def rmove(self,posrelatif,vitesse=10000):
        """
        rmove(motor,posrelatife): : mouvement relatif du moteur (motor) a la position posrelatif 
        """
        posActuel=self.position()
        print (time.strftime("%A %d %B %Y %H:%M:%S"))
        print (self.moteurname,"position before ",posActuel,"(step)")
        
        s.send((self.numMoteur+'PR'+str(int(posrelatif)) +'\n').encode())
        print (self.moteurname , "relative move of",posrelatif,"(step)")

    def setzero(self):
        """
        setzero(motor):Set Zero
        """
        
        s.send((self.numMoteur+'DH'+'\n').encode())
        print (time.strftime("%A %d %B %Y %H:%M:%S"))
        print (self.moteurname,"set to zero")

    def setvelocity(self,v=2000):
        """
        setvelocity(motor,velocity): Set Velocity en step/s
        """
        
        
        if v>2001:
            print ("speed Too Hight !!!")
        else:
            v1=int(v)
            s.send((self.numMoteur+'VA'+str(v)+'\n')).encode()
            print ("velocity of",self.moteurname,"set to",str(v))
        return v1

#%%
if __name__ == "__main__":
    print("test")
    #startConnexion()

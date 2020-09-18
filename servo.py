# -*- coding: utf-8
""" Control Servo motor Polulu with pololu card (usb)
protocole serial
python 3.X and PyQt5
@author: Gautier julien loa
Created on Wed Feb 28 14:46:32 2018
"""


from serial import Serial,serialutil
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from PyQt5 import uic
import time,sys

portServo=('com18')
ser=Serial()
try:
    ser.port=portServo
    ser.timeout=1
    if ser.is_open==False:
        ser.open()
    else:
        ser.close()
        time.sleep(0.1)
        ser.open()
    print("polulu servo motors connected on port:...",portServo)
    
except serialutil.SerialException :
    print ('the port is already open')
    ap=QApplication(sys.argv)
    az=uic.loadUi('attention.ui')
    az.show()
    ap.exec_()
    pass

def stopConnexion():
    try :
        ser.close()
        print('servo closed')
    except:
       pass

confServo=QSettings('fichiersConfig/configMoteurServo.ini', QSettings.IniFormat) # motor configuration  files



class MOTORSERVO():
    
    def __init__(self, mot1='',parent=None,device=0x0c):
        #super(MOTORSERVO, self).__init__()
        self.moteurname=mot1
        self.confServo=confServo
        self.numMoteur=chr(int(self.confServo.value(self.moteurname+'/numMoteur')))
        self.device=chr(device)
        self.posOFF=int(self.confServo.value(self.moteurname+'/posOFF'))
        self.posIN=int(self.confServo.value(self.moteurname+'/posIN'))
        self.servoType=str(self.confServo.value(self.moteurname+'/moteurType'))
        
    def getPosition(self):  # Mesure la position du servo numServo
        cmd=chr(0xaa)+self.device+chr(0x10)+self.numMoteur # pololu protocol 0xAA
        ser.write(bytes(cmd,'latin-1'))
        lsb = ord(ser.read())
        msb = ord(ser.read())
        vpos=((msb << 8) + lsb)/4
        self.confServo.setValue(self.moteurname+'/pos',vpos)
        return vpos
    
    def position(self):
        # retourne la postion sauvegarder
        return self.confServo.value(self.moteurname+'/pos')
    
    def setPosition(self,pos):
        # ecrit la postion à sauvegarder
       self.confServo.setValue(self.moteurname+'/pos',pos)
       
    def move(self,target):  # Compact protocol 0x84 chanel number ,target low bits, target high bits
        ser.write(chr(0x84).encode())
        ser.write(self.numMoteur.encode())
        pos=target*4
        bitcourt=pos & 0x7F
        bitlong=(pos>>7) & 0x7F
        cmd = chr(0xaa) +self.device + chr(0x04)+self.numMoteur+chr( bitcourt) + chr(bitlong)
        ser.write(bytes(cmd,'latin-1'))       
            
    def rmove(self,pos=0,vitesse=10000):
        posActuel = self.position()
        print(time.strftime("%A %d %B %Y %H:%M:%S"))
        print(self.moteurname,"position before ",posActuel,"(step)")
        postomove  = int(posActuel+pos)
        self.move(postomove)
        print(self.moteurname,"relative move of ",pos,"(step)")

    def stopMotor(self):
    	#ser.write(chr(0xA4).encode())
    	#ser.write(chr(self.numMoteur).encode())
        self.move(0)
        
    def setzero(self):
        """ to do
        """
        print ('zero')

    def goPositionOFF(self):
        self.move(self.posOFF)
        if self.servoType=="ServoOld":
            time.sleep(3)  
        
    def goPositionIN(self):
        self.move(self.posIN)
        if self.servoType=="ServoOld": 
            time.sleep(3)

if __name__ == "__main__":
    print("test")
    ser='Servo'+str(0)
    SERVO1=MOTORSERVO(ser)
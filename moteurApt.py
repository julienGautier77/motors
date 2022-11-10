
try :
    from PyQt6.QtCore import QSettings
except ImportError:
    print('error PYQT6 import')
confApt=QSettings('./fichiersConfig/configMoteurApt.ini', QSettings.Format.IniFormat)
from DLL.apt import core
import time
import logging


class MOTORAPT():
    def __init__(self, mot1='',parent=None):
        #super(MOTORNEWPORT, self).__init__()
        self.moteurname=mot1
        self.numMoteur=int(confApt.value(self.moteurname+'/numMoteur'))
        print(self.numMoteur)
        date=time.strftime("%Y_%m_%d")
        fileNameLog='logMotor_'+date+'.log'
        logging.basicConfig(filename=fileNameLog, encoding='utf-8', level=logging.INFO,format='%(asctime)s %(message)s')
        self.aptMotor=core.Motor(self.numMoteur)
        
    def stopMotor(self): # stop le moteur motor
        """ stopMotor(motor): stop le moteur motor """
        self.numMoteur.stop_profiled
    
    def rmove(self,pas,vitesse=1000):
        actualPosition=int(confApt.value(self.moteurname+'/Pos'))
        
        position=actualPosition+pas
        
        self.aptMotor.move_by(pas)
       
        confApt.setValue(self.moteurname+"/Pos",position)
        confApt.sync()

        tx='motor ' +self.moteurname +' rmove  of ' + str(pas) + ' step  ' + '  position is :  ' + str(self.position())

        logging.info(tx)

        #return recu

    def move(self,position,vitesse=1000):
        
        actualPosition=float(confApt.value(self.moteurname+'/Pos'))
        pas=(position)-(actualPosition)
        
        self.aptMotor.move_by(pas)
        
        #self.aptMotor.move_to(position)
        confApt.setValue(self.moteurname+"/Pos",position)
        confApt.sync()
        tx='motor ' +self.moteurname +'  absolute move to ' + str(position) + ' step  ' + '  position is :  ' + str(self.position())
        logging.info(tx)
        #return recu
    
    def position(self):
        #position = self.aptMotor.position()
        position=float(confApt.value(self.moteurname+'/Pos'))
        return position
    
    def setzero(self):
        confApt.setValue(self.moteurname+"/Pos",0)
        

    

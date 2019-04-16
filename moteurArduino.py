
import socket
from PyQt5.QtCore import QSettings

confArduino=QSettings('fichiersConfig/configMoteurArduino.ini', QSettings.IniFormat)




class MOTORARDUINO():
    def __init__(self, mot1='',parent=None):
        #super(MOTORNEWPORT, self).__init__()
        self.moteurname=mot1
        self.numMoteur=int(confArduino.value(self.moteurname+'/numMoteur'))
        
        self.client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connexion()
        
    def connexion(self):
        self.ad=str(confArduino.value(self.moteurname+'/adress'))
        self.port=int(confArduino.value(self.moteurname+'/port'))
        self.adress=(self.ad,self.port)
        print (self.moteurname,'arduino connecté @',self.adress)
        self.client.connect(self.adress)
    
    
    
    def rmove(self,pas,vitesse=1000):
        
        command=str(self.numMoteur)+' '+str(pas)+' '+str(vitesse)
        self.client.send(command.encode())
        #recu=self.client.recvfrom(512)[0]
        actualPosition=int(confArduino.value(self.moteurname+'/Pos'))
        position=actualPosition+pas
        confArduino.setValue(self.moteurname+"/Pos",position)
        confArduino.sync()
        #return recu

    def move(self,position,vitesse=1000):
        actualPosition=int(confArduino.value(self.moteurname+'/Pos'))
        pas=int(position)-(actualPosition)
        command=str(self.numMoteur)+' '+str(pas)+' '+str(vitesse)
        self.client.send(command.encode())
        #recu,adressRemote=self.client.recvfrom(512)
        confArduino.setValue(self.moteurname+"/Pos",position)
        confArduino.sync()
        #return recu
    
    def position(self):
        actualPosition=int(confArduino.value(self.moteurname+'/Pos'))
        print(actualPosition)
        return actualPosition
    
    def setzero(self):
        confArduino.setValue(self.moteurname+"/Pos",0)

    
    def stopConnexion(self):
        self.client.close()


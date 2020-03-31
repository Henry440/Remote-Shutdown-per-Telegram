from configs import *
from InternMSG import  internMSG
import socket
import os
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

serverKey = "firstKontakt"
MY_TOKEN = "PC-1"

knownCommands = (("shutdown", True, "doIt"), ("test", True, "test"))
#Commands on System
def test():
    print(f"Test Erfolgreich ")

def shutdown():
    pass


#Send Commands to Server
def regAddServer():
    msg = internMSG(MY_TOKEN, serverKey, "registration", "hereAmI")
    sendMsg(msg)

def goOffline():
    msg = internMSG(MY_TOKEN, serverKey, "offline", "bye")
    sendMsg(msg)


#Handel In and out Messages
def recvMesg():
    pass

def sendMsg(msg):
    client_socket.send(bytes(msg, "utf8"))

def handleCommand(msg):
    if(msg.forMe(MY_TOKEN) or True):
        if(msg.turst(serverKey) or True):
            for command in knownCommands:
                if(command[0] == msg.command):
                    if(command[1]):
                        if(msg.key == command[2]):
                            pass
                        else:
                            print("Unautorisierter Key")
                    else:
                        pass
        else:
            print("Nachicht ist nicht von Server gesendet wurden")
    else:
        print(f"Nachicht nicht für diesen PC / Nachicht für {msg.reciver}")

regAddServer()
t = Thread(target=recvMesg)
t.start()
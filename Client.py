from configs import *
from InternMSG import  *
import socket
import os
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

serverKey = "SV1"
MY_TOKEN = "PC-1"

knownCommands = (("shutdown", True, "doIt"), ("test", True, "test"))
#Commands on System
def test():
    print(f"Test Erfolgreich ")

def shutdown():
    print("Shutdown")
    goOffline()
    print("Abgemeldet")


#Send Commands to Server
def regAddServer():
    msg = internMSG(MY_TOKEN, serverKey, "registration", "hereAmI")
    sendMsg(msg)

def goOffline():
    msg = internMSG(MY_TOKEN, serverKey, "offline", "bye")
    sendMsg(msg)


#Handel In and out Messages
def recvMesg():
    while True:
        data = client_socket.recv(2048)
        if(len(data) <= 0):
            pass
        data = str(data, "utf8")
        print(data)
        conv = StringToMsg(data)
        msg = internMSG(conv[0], conv[1], conv[2], conv[3])
        handleCommand(msg)

def sendMsg(msg):
    client_socket.send(bytes(msg.toString(), "utf8"))

def handleCommand(msg):
    if(msg.forMe(MY_TOKEN)):
        if(msg.turst(serverKey)):
            for command in knownCommands:
                if(command[0] == msg.command):
                    if(command[1]):
                        if(msg.key == command[2]):
                            if(msg.command == "shutdown"):
                                shutdown()
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
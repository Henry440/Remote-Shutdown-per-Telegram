from configs import *
from InternMSG import  *
import socket
import os
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

serverKey = "SV1"
MY_TOKEN = "Tower"

knownCommands = (("shutdown", True, "doIt"), ("test", True, "test"), ("online", False, ""))
#Commands on System
def test():
    print(f"Test Erfolgreich ")

def shutdown():
    print("Shutdown")
    goOffline()
    print("Abgemeldet")
    os.system("shutdown -s -t 240 -f -c \"EINSATZ zum Abbrechen shutdown -a in CMD\"")

def onlineRegeust(msg):
    msg = internMSG(MY_TOKEN, serverKey, "online", str(msg.key))
    print(f"Sende --> {msg}")
    sendMsg(msg)


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
            continue
        print("Empfange")
        data = str(data, "utf8")
        print(data)
        conv = StringToMsg(data)
        msg = internMSG(conv[0], conv[1], conv[2], conv[3])
        handleCommand(msg)

def sendMsg(msg):
    print("It Work 2")
    client_socket.send(bytes(msg.toString(), "utf8"))

def executeCommand(msg):
    if(msg.command == "shutdown"):
        shutdown()
    elif(msg.command == "test"):
        test()
    elif (msg.command == "online"):
        print("It Work 1")
        onlineRegeust(msg)

def handleCommand(msg):
    if(msg.forMe(MY_TOKEN)):
        if(msg.turst(serverKey)):
            for command in knownCommands:
                if(command[0] == msg.command):
                    if(command[1]):
                        if(msg.key == command[2]):
                            executeCommand(msg)
                        else:
                            print("Unautorisierter Key")
                    else:
                        executeCommand(msg)
        else:
            print("Nachicht ist nicht von Server gesendet wurden")
    else:
        print(f"Nachicht nicht für diesen PC / Nachicht für {msg.reciver}")

regAddServer()
t = Thread(target=recvMesg)
t.start()
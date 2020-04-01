import telebot
import json
from Message import Message
import socket
from configs import *
from InternMSG import  *
from threading import Thread

import time

bot = telebot.TeleBot(TOKEN)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((IP, PORT))
SERVER_TOKEN = "SV1"

REG_USER = []
USER_IP = []
USER_LIST = [] #(REG_USER, USER_IP)

knownCommands = (("registration", True, "hereAmI"), ("offline", True, "bye"), ("online", False, ""))

#Functions Incomming
def addClient(msg):
    REG_USER.append(msg.sender)

def remClient(msg):
    for i in range(len(REG_USER)):
        if(REG_USER[i] == msg.sender):
            USER_LIST.remove((REG_USER[i], USER_IP[i]))
            print(str(msg.sender) + " wurde Entfernt")

#Gen Userdatas
def genUserList():
    USER_LIST.clear()
    if(len(USER_IP) == len(REG_USER)):
        for i in range(len(USER_IP)):
            USER_LIST.append((REG_USER[i], USER_IP[i]))
    for user in USER_LIST:
        print(user)

#SystemBridge Commands
def online(message):
    data = Message(message)
    target = "all"
    data = msgBuilder(target, "online", str(data.chatID))
    msgs = data[1]
    if(data[0] == 0):
        for msg in msgs:
            sendMsg(msg)
    elif(data[0] == -1):
        print("Error Kann nicht Fortgesetzt werden")

def onlineBack(msg):
    bot.send_message(msg.key, f"{msg.sender} ist Online")


#Send Functions
def pcSchutdown():
    target = "all"
    data = msgBuilder(target, "shutdown", "doIt")
    
    msgs = data[1]

    if(data[0] == 0):
        for msg in msgs:
            sendMsg(msg)
    elif(msgs[0] == -1):
        print("Error Kann nicht Fortgesetzt werden")

def msgBuilder(target, command, key):
    genUserList()
    if(target == "all"):
        msg_list = []
        if(len(REG_USER) > 0):
            for targ in REG_USER:
                msg_list.append(internMSG(SERVER_TOKEN, targ, command, key))
                for msg in msg_list:
                    print(msg.key)
            return(0, msg_list)
        else:
            print("Keine Registrirte Nutzer")
            return(-1,-1)
    else:
        msg = internMSG(SERVER_TOKEN, target, command, key)
        return(1, msg)

#Handel In and out Messages

def waitOfClient():
    while True:
        if(len(USER_IP) > 0):
            for client in USER_IP:
                data = client.recv(2048)
                if(len(data) <= 0):
                    continue
                data = str(data, "utf8")
                print(data)
                conv = StringToMsg(data)
                msg = internMSG(conv[0], conv[1], conv[2], conv[3])
                msgHandler(msg)
        else:
            time.sleep(10)


def recvMesg():
    serverSocket.listen()
    print("Server is Running")
    while True:
        (client_socket, addr) = serverSocket.accept()
        print(addr)
        inIP = False
        for ip in USER_IP:
            if(ip == client_socket):
                inIP = True
        if(inIP == False):
            USER_IP.append(client_socket)
        data = client_socket.recv(2048)
        data = str(data, "utf8")
        print(data)
        conv = StringToMsg(data)
        msg = internMSG(conv[0], conv[1], conv[2], conv[3])
        msgHandler(msg)

def sendMsg(msg):
    to = str(msg.reciver)
    for empf in USER_LIST:
        if(empf[0] == to):
            print(f"Sende Nachicht zu {to}")
            empf[1].send(bytes(msg.toString(), "utf8"))

def msgHandler(msg):
    if(msg.forMe(SERVER_TOKEN)):
        for command in knownCommands:
            if(command[0] == msg.command):
                if(command[1]):
                    if(msg.key == command[2]):
                        commandList(msg)
                    else:
                        print("Unautorisierter Key")
                else:
                    commandList(msg)
    else:
        print(f"Nachicht nicht für diesen PC / Nachicht für {msg.reciver}")

def commandList(msg):
    if(msg.command == "registration"):
        addClient(msg)
    elif(msg.command == "offline"):
        remClient(msg)
    elif(msg.command == "online"):
        onlineBack(msg)

#Telegram Bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Kennen wir uns?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "/start --> Starte den Telegrambot\n/fire --> PC Shutdown")

@bot.message_handler(commands=['online'])
def send_help(message):
    bot.reply_to(message, "Execute Online Command")
    online(message)


@bot.message_handler(commands=['fire'])
def alarmFeuer(message):
    data = Message(message)
    send = False
    for user in AUTH_USER:
        if(data.chatID == user):
            print("Befehl Shutdown Recived")
            pcSchutdown()
            bot.reply_to(message, "PC Shutdown wird ausgeführt")
            send = True
            break
    if(send == False):
        bot.reply_to(message, "Du bist nicht Berechtigt")
        

@bot.message_handler(content_types=["text"])
def echo_all(message):
    data = Message(message)
    bot.send_message(data.chatID, f"Deine ChatID ist {data.chatID} \nDeine Nachicht war : {data.text}")
    print(message.json)

try:
    
    t = Thread(target=recvMesg)
    t.start()
    cl = Thread(target=waitOfClient)
    cl.start()
    print("Telegram Bot is Running")
    bot.polling()
except KeyboardInterrupt:
    print("Beende")
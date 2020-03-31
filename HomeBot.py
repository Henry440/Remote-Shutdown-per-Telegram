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
USER_LIST = []

knownCommands = (("registration", True, "hereAmI"), ("offline", True, "bye"))

#Functions Incomming
def addClient(msg):
    REG_USER.append(msg.sender)
    genUserList()

def remClient(msg):
    REG_USER.remove(msg.sender)
    print(str(msg.sender) + " wurde Entfernt")
    genUserList()

#Gen Userdatas
def genUserList():
    USER_LIST = []
    if(len(USER_IP) == len(REG_USER)):
        for i in range(len(USER_IP)):
            USER_LIST.append((REG_USER[i], USER_IP[i]))

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
            return(0, msg_list)
        else:
            print("Keine Registrirte Nutzer")
            return(-1,-1)
    else:
        msg = internMSG(SERVER_TOKEN, target, command, key)
        return(1, msg)

#Handel In and out Messages
def recvMesg():
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
        client_socket.close()
        print(data)
        conv = StringToMsg(data)
        msg = internMSG(conv[0], conv[1], conv[2], conv[3])
        msgHandler(msg)

def sendMsg(msg):
    to = str(msg.reciver)
    for empf in USER_LIST:
        if(empf[0] == to):
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
                    command(msg)
    else:
        print(f"Nachicht nicht für diesen PC / Nachicht für {msg.reciver}")

def commandList(msg):
    if(msg.command == "registration"):
        addClient(msg)
    elif(msg.command == "offline"):
        remClient(msg)

#Telegram Bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Kennen wir uns?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "/start --> Starte den Telegrambot\nfire --> PC Shutdown")

@bot.message_handler(commands=['fire'])
def alarmFeuer(message):
    data = Message(message)
    send = False
    for user in AUTH_USER:
        if(data.chatID == user):
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
    serverSocket.listen(5)
    t = Thread(target=recvMesg)
    t.start()
    print("Telegram Bot is Running")
    bot.polling()
except KeyboardInterrupt:
    print("Beende")
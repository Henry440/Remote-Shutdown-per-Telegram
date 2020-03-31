import telebot
import json
from Message import Message
import socket
from configs import *
from InternMSG import  internMSG

bot = telebot.TeleBot(TOKEN)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((IP, PORT))
SERVER_TOKEN = "SV1"

REG_USER = []
#Functions Incomming
def addClient(msg):
    REG_USER.append(msg.sender)

def remClient(msg):
    REG_USER.remove(msg.sender)

#Send Functions
def pcSchutdown():
    target = "all"
    msgs = msgBuilder(target, "shutdown", "doIt")
    if(msgs[0] == 0):
        for msg in msgs:
            sendMsg(msg)
    elif(msgs[0] == -1):
        print("Error Kann nicht Fortgesetzt werden")

def msgBuilder(target, command, key):
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
    pass

def sendMsg(msg):
    pass

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

bot.polling()
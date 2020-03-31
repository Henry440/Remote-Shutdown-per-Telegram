import telebot
import json
from Message import Message
import socket
from configs import *

bot = telebot.TeleBot(TOKEN)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((IP, PORT))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=["text"])
def echo_all(message):
    data = Message(message)
    bot.send_message(data.chatID, f"Deine ChatID ist {data.chatID} \nDeine Nachicht war : {data.text}")
    print(message.json)

bot.polling()
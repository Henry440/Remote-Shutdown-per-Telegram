import telebot
import json

class Message:
    
    def __init__(self, tbMessage):
        self.tbMessage = tbMessage
        self.data = tbMessage.json
        self.chatID = self.data["from"]["id"]
        self.isBot = self.data["from"]["is_bot"]
        self.firstName = self.data["from"]["first_name"]
        self.lastName = self.data["from"]["last_name"]
        self.username = self.data["from"]["username"]
        self.languagecode = self.data["from"]["language_code"]
        self.chatType = self.data["chat"]["type"]
        self.date = self.data["date"]
        self.text = self.data["text"]
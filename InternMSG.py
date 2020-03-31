
class internMSG:

    def __init__(self, sender, reciver, command, key):
        self.sender = sender
        self.reciver = reciver
        self.command = command
        self.key = key

    def forMe(self, token):
        if(self.reciver == token):
            return True
        else:
            return False

    def turst(self, serverToken):
        if(self.sender == serverToken):
            return True
        else:
            return False
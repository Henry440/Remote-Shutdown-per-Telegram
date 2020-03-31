
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

    def toString(self):
        ret = ""
        ret = ret + str(self.sender) + "#!#"
        ret = ret + str(self.reciver) + "#!#"
        ret = ret + str(self.command) + "#!#"
        ret = ret + str(self.key)
        return ret

def StringToMsg(msg):
        datas = msg.split("#!#")
        return datas
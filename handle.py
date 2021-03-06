class Message:
    def __init__(self, data):
        self.uid = data['uid']
        self.time = data['time']
        self.data = data['payload']

    def getTime(self):
        return self.time

    def getUID(self):
        return self.uid

    def getData(self):
        return self.data

    def __repr__(self):
        return "Message, time: %s, uid: %s, data: %s" % (self.time, self.uid, self.data)

    def __str__(self):
        return self.__repr__()



class Room(object):

    def __init__(self):
        self.source = {}
        self.recievers = {}
        self.reflectors = {}
        self.ctime = 1000. # cuttoff time in miliseconds
        self.rays = {}

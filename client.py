from errors import ConnectionError
import logging as log
import socket

log.basicConfig(format = "%(asctime)s %(message)s")

class Client:
    def __init__(self):
        self.connected = False

    def connect(self, ip, port):
        if self.connected:
            log.log(30, "Client already connected!")

        self._connection = socket.socket(socket.AF_INET)
        self._connection.connect(

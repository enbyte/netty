import crypttools as crypt
import socket, threading, pickle, handle, json, sys
import time

class ErrorDisconnectedFromServer(Exception):
    pass

class ErrorReceivingMessage(Exception):
    pass

class ErrorSendingMessage(Exception):
    pass

class ErrorMessageNotFromServer(Exception):
    pass

class ErrorConnectingToServer(Exception):
    pass

class Client:
  def __init__(self, ip, port, onReceive=lambda x: None):
    self.ip = ip
    
    self.port = port
    
    self.uid = crypt.strHash(str(self.ip) + str(self.port))
    
    self.connected = False
    
    self.connection = None
    self.onReceive = onReceive
  
  def _dict_wrapper(self, data, type_='data'):
        return {
            'uid': self.uid,
            'time': time.time(),
            'payload': data,
            'type': type_
        }
    
  def _receive_once(self):
    try:
      received = self.connection.recv(1024)
      try:
          mes = pickle.loads(received)
          mes = handle.Message(mes)
      except:
          raise ErrorReceivingMessage
      if mes != None:
        self.onReceive(mes)
    except:
        print("Closing...")
        self.connection.close()
        raise ErrorDisconnectedFromServer

  def _rec_forever(self):
      while True:
          self._receive_once()
          
  def connect(self):
    assert not self.connected
    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.connection.connect((str(self.ip), int(self.port)))
      self.connected = True
    except:
      self.connected = False
      self.connection = None
      raise ErrorConnectingToServer

  def send(self, data):
    assert self.connected
    wrapper = self._dict_wrapper(data)
    try:
        self.connection.send(pickle.dumps(wrapper))
    except:
        raise ErrorSendingMessage

  def start(self):
      assert not self.connected
      self.connect()
      thread = threading.Thread(target=self._rec_forever)
      thread.start()
      



class Server:
    def __init__(self, port, onReceive=lambda x, y: None):
        self.port = port
        self.ip = ''
        self.started = False
        self._clients = []
        self.clients = []
        self.onReceive = onReceive

    def _handle_all(self):
        for c in self._clients:
            data = c.recv(1024)
            if not data == b'':
                data = pickle.loads(data)
                self.onReceive(data, self._clients)
                print("Completed non-empty send-check cycle")
    def _handle_forever(self):
        while True:
            self._handle_all()

    def _accept_once(self):
        print("before accept")
        client, address = self.listener.accept()
        self._clients.append(client)
        print("Got client: %s" % client)
        print("after accept")

    def _accept_forever(self):
        while True:
            self._accept_once()

    def start(self):
        assert not self.started
        print("Starting server")
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((self.ip, self.port))
        self.listener.listen(5)
        self.handleThread = threading.Thread(target=self._handle_forever)
        self.acceptThread = threading.Thread(target=self._accept_forever)
        self.handleThread.start()
        self.acceptThread.start()
            
            
            
        
        
    

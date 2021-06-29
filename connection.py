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

__HEADER_SIZE__ = 4
__HEADER_AMOUNT__ = 4

class Client:
  def __init__(self, ip, port, onReceive=lambda x: None):
    self.ip = ip
    
    self.port = port
    
    self.uid = crypt.strHash(str(self.ip) + '$@lt' + str(self.port))
    
    self.connected = False
    
    self.connection = None
    self.onReceive = onReceive
    self.timeLast = time.time()
  
  def _dict_wrapper(self, data, type_='data'):
        return {
            'uid': self.uid,
            'time': time.time(),
            'payload': data,
            'type': type_
        }
    
  def _receive_once(self):
    try:
      received = self.connection.recv(__HEADER_SIZE__)
      received = int(received)
      #print("Client got data amount:", received)
      if received == b'': return
      received = int(received)
      mes = None
      try:
          data = self.connection.recv(received)
          mes = pickle.loads(data)
          mes = handle.Message(mes)
      except Exception as e:
          print("Error:", e)
          mes = None
      if mes != None:
        self.onReceive(mes)
    except:
        print("Closing...")
        self.connection.close()
        raise ErrorDisconnectedFromServer

  def _rec_forever(self):
      assert self.connected
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
        dumped_wrapper = pickle.dumps(wrapper)
        try:
            x = str(len(dumped_wrapper)).encode().rjust(4, b'0')
            #print("Client sent packet with length:", x)
            self.connection.sendall(x + dumped_wrapper)
        except:
            raise ErrorSendingMessage

  def start(self):
      assert not self.connected
      self.connect()
      self.rec_thread = threading.Thread(target=self._rec_forever)
      self.rec_thread.start()
      



class Server:
    def __init__(self, port, onReceive=lambda x, y: None, _newthread_client=True):
        self.port = port
        self.ip = ''
        self.started = False
        self._clients = []
        self._clientthreads = []
        self.clients = []
        self.onReceive = onReceive
        self._newthread_client = True
        
    def _handle_single(self, client):
        while True:
            numchars = client.recv(__HEADER_AMOUNT__)
            if numchars == b'':
                continue
            #print("Server numchars recv len:", numchars) 
            numchars = int(numchars)
            data = client.recv(numchars)
            if not data == b'':
                data = pickle.loads(data)
                #print(data, type(data))
                self.onReceive(data, self._clients)
            

    def _handle_all(self):
        clientno = 0
        clientmax = len(self._clients)
        for c in range(clientmax):
            try:
                client = self._clients[c]
                things = c.recv(__HEADER_AMOUNT__)
                if things == b'':
                    continue
                chars = int(things)
                data = c.recv(chars)
                #print("Number of characters:", chars)
                if not data == b'':
                    data = pickle.loads(data)
                    self.onReceive(data, self._clients)
            except:
                pass
    def _handle_forever(self):
        while True:
            self._handle_all()

    def _accept_once(self):
        #print("before accept")
        client, address = self.listener.accept()
        self._clients.append(client)
        
        print("Got client: %s" % client)
        #print("after accept")

    def _accept_forever(self):
        while True:
            self._accept_once()
    def _accept_newthread_forever(self):
        while True:
            #print("newthread -- before accept")
            client, address = self.listener.accept()
            self._clients.append(client)
            point = len(self._clientthreads)
            print("Got client:", client)
            self._clientthreads.append(threading.Thread(target=self._handle_single, args = (client, )))
            self._clientthreads[point].start()

    def start(self):
        assert not self.started
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((self.ip, self.port))
        self.listener.listen(5)
        print("Server successfully created on port %s" % self.port)
        if not self._newthread_client:
            self.acceptThread = threading.Thread(target=self._accept_forever)
            self.acceptThread.start()
            self.handleThread = threading.Thread(target=self._handle_forever)
            self.handleThread.start()
        else:
            self.acceptThread = threading.Thread(target=self._accept_newthread_forever)
            self.acceptThread.start()

            
            
            
        
        
    

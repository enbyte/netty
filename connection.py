import utils
import socket
import threading
import pickle
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
  def __init__(self, ip, port, on_receive=lambda x: None, uid=None):
    self.ip = ip
    
    self.port = port
    
    self.uid = (
        (utils.generate_random_uid(
            str(self.ip) + '$@lt' + str(self.port) + str(time.time())
        ) 
        if uid is None else uid))
    
    self.connected = False
    
    self.connection = None
    self.on_receive = on_receive
    self.timeLast = time.time()
  
  def _dict_wrapper(self, data, type_='data'):
        return {
            'uid': self.uid,
            'time': time.time(),
            'data': data,
            'type': type_
        }
    
  def _receive_once(self):
    try:
      received = self.connection.recv(__HEADER_SIZE__)
      if received == b'':
            return  
      received = int(received)
      mes = None
      try:
          data = self.connection.recv(received)
          mes = pickle.loads(data)
          mes = utils.Message(mes)
      except Exception as e:
          print("Error:", e)
          mes = None
      if mes is not None:
        self.on_receive(mes)
    except:
        print("Closing...")
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

  def send(self, data, type_='data'):
        assert self.connected
        wrapper = self._dict_wrapper(data, type_=type_)
        dumped_wrapper = pickle.dumps(wrapper)
        try:
            length = str(len(dumped_wrapper)).encode().rjust(4, b'0')
            self.connection.sendall(length + dumped_wrapper)
        except Exception as e:
            print(e)
            raise ErrorSendingMessage

  def start(self):
      assert not self.connected
      self.connect()
      self.rec_thread = threading.Thread(target=self._rec_forever)
      self.rec_thread.start()

  def stop(self):
        assert self.connected
        self.connection.close()
        self.connected = False
        self.connection = None
        self.rec_thread.join()
      



class Server:
    def __init__(self, port, on_receive=lambda x, y, z, w: None, _newthread_client=True):
        self.port = port
        self.ip = ''
        self.started = False
        self._clients = []
        self._clientthreads = []
        self.on_receive = on_receive
        self._newthread_client = True


    def send_single(self, client_or_client_index, data):
        client = self.clients[client_or_client_index] if type(client_or_client_index) == int else client_or_client_index

        dump = pickle.dumps(data) # data is the dict already
        try:
            length = str(len(dump)).encode().rjust(4, b'0')
            client.sendall(length + dump)
        except Exception as e:
            print(e)
            raise ErrorSendingMessage
        
    def send_all(self, data):
        for client in self._clients:
            self.send_single(client, data)

    def send_all_except(self, data, client):
        for client in self._clients:
            if not client == client:
                self.send_single(client, data)
        
    def _handle_single(self, client):
        while True:
            try:
                numchars = client.recv(__HEADER_AMOUNT__)
                if numchars == b'':
                    continue
                numchars = int(numchars)
                data = client.recv(numchars)
                if not data == b'':
                    data = pickle.loads(data)
                    self.on_receive(data, self._clients, self, client)
            except ConnectionResetError:
                print('Client disconnected:', client)

    def remove_client(self, client):
        self._clients.remove(client)
            

    def _handle_all(self):
        for client in self._clients:
            self._handle_single(client)

    def _handle_forever(self):
        while True:
            self._handle_all()

    def _accept_once(self):
        client, address = self.listener.accept()
        self._clients.append(client)
        
        print("Got client: %s" % client)

    def _accept_forever(self):
        while True:
            self._accept_once()

    def _accept_newthread_forever(self):
        while True:
            client, address = self.listener.accept()
            self._clients.append(client)
            point = len(self._clientthreads)
            self._clientthreads.append(threading.Thread(target=self._handle_single, args=(client,)))
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

            
            
            
        
        
    

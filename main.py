from __init__ import *

def echo(message):
    print("Client got a message!")
    print(message['payload'])

def broadcast_all(mes, clients):
    print("Server got message:", mes['payload'])
    for client in clients:
        client.sendall(encode(mes['payload']))
        print("Server echoed message %s to client %s" % (mes['payload'], mes['uid']))
        

client = connection.Client('', 3000, onReceive=echo)

server = connection.Server(3000, onReceive=broadcast_all)

server.start()

client.start()

client.send("Hi!")

client.send(5)

client.send( {'a': 'b'} )

client.send( ["netty supports", 'pickleable data types'])

from __init__ import *


__PORT__ = 3009


def echo(mes):
    print("Client type of mes:", type(mes))
    print(mes)

def broadcast_all(mes, clients):
    print("Server type of mes:", type(mes))
    print("Server got message:", mes['payload'])
    for client in clients:
        client.send(encode(mes))
        print("Server echoed message %s to client %s" % (mes['payload'], mes['uid']))

client = connection.Client('', __PORT__, onReceive=echo)

server = connection.Server(__PORT__, onReceive=broadcast_all)

server.start()

client.start()

client.send("Hi!")

client.send(5)

client.send(['netty supports', 'pickleable data types', 5])

client.send( {'a': 'b'} )


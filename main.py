from __init__ import *


__PORT__ = 3010


def echo(mes):
    print("Client got message with time %s, uid %s, and data %s" % (mes.time, mes.uid, mes.data))

def broadcast_all(mes, clients):
    for client in clients:
        client.send(encode(mes))

client = connection.Client('', __PORT__, onReceive=echo)

server = connection.Server(__PORT__, onReceive=broadcast_all)

server.start()

client.start()

client.send("Hi!")

client.send(5)

client.send(['netty supports', 'pickleable data types', 5])

client.send( {'a': 'b'} )


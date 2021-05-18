import .netty

def echo(message):
    print(message)

def broadcast_all(mes, clients):
    for client in clients:
        client.send(mes)

client = connection.Client('', 3000, onReceive=echo)

server = connection.Server(3000, onReceive=broadcast_all)

server.start()

client.connect()

client.send("Hi!")

client.send(5)

client.send( {'a': 'b'} )


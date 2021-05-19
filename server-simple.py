import netty
import pickle

__PORT__ = 1030

def broadcast_all(mes, clients):
    print("Got packet %s" % mes)
    dump = pickle.dumps(mes)
    dumpl = str(len(dump)).encode().rjust(4, b'0')
    for c in clients:
        c.send(dumpl)
        c.send(dump)
        
server = netty.connection.Server(__PORT__, onReceive=broadcast_all, _newthread_client=False)

server.start()

import netty
import pickle
import time

__PORT__ = 34893

STATES = {}

def handle_packet(packet, clients, server, client):
    if packet['type'] == 'join':
        print('%s has joined!' % packet['uid'][:10])
        STATES[packet['uid']] = {'x': 0, 'y': 0, 'color': 'black'}
        server.send_single(client, {'type': 'welcome_sync', 'data': {'players': STATES}, 'uid': 'SERVER', 'time': time.time()})
        server.send_all({'type': 'join', 'data': packet['data'], 'uid': packet['uid'], 'time': time.time()})

    elif packet['type'] == 'update':
        STATES[packet['uid']] = packet['data']
        server.send_all({'type': 'update', 'data': packet['data'], 'uid': packet['uid'], 'time': time.time()})
        
    elif packet['type'] == 'leave':
        server.send_all({'type': 'leave', 'data': packet['data'], 'uid': packet['uid'], 'time': time.time()})
        server.remove_client(client)
        del STATES[packet['uid']]
    
    
        
server = netty.connection.Server(__PORT__, on_receive=handle_packet, _newthread_client=False)

server.start()

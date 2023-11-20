import netty
import pygame
from pygame.locals import *
import time

pygame.init()

PORT = 34893
IP = ''

class Player:
    def __init__(self, x, y, color, uid):
        self.x = x
        self.y = y
        self.color = pygame.Color(color)
        self.uid = uid


    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))
                         
    def update_color(self, color):
        self.color = color

    def get_packet_dict(self):
        return {'x': self.x, 'y': self.y, 'color': self.color}
    
    def handle_packet(self, packet): # EXTERNAL METHOD CALLED EXTERNALLY
        data = packet.data
        if not (packet.uid == self.uid): return

        self.update_position(data['x'], data['y'])
        self.update_color(data['color'])

class NetworkedPlayerManager:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = netty.connection.Client(ip, port, self.handle_packet)
        self.client.start()

        self.player_uid = self.client.uid

        self.players = {self.client.uid: Player(0, 0, 'black', self.client.uid)}

        self.client.send(['join', self.client.uid], type_='join')

    def handle_packet(self, packet):
        packet_type, packet_data = packet.type_, packet.data
        if packet_type == 'join':
            if not packet.uid in self.players:
                self.players[packet.uid] = Player(0, 0, 'black', packet.uid)
                print('Player joined')
        elif packet_type == 'leave':
            if packet.uid in self.players:
                del self.players[packet.uid]
                print('Player left')
        elif packet_type == 'update':
            if packet.uid in self.players:
                self.players[packet.uid].handle_packet(packet)

        elif packet_type == 'welcome_sync':
            player_dicts = packet_data['players']
            self.players = {}
            for uid in player_dicts:
                self.players[uid] = Player(player_dicts[uid]['x'], player_dicts[uid]['y'], player_dicts[uid]['color'], uid)
            print('Parsed welcome sync and there are %d player(s)' % len(self.players))
        else:
            print('Unknown packet type:', packet_type)

    def update(self):
        update = self.players[self.player_uid].get_packet_dict()
        self.client.send(update, type_='update')

    def leave(self):
        self.client.send(['leave', self.client.uid], type_='leave')
        self.end_connection()

    def end_connection(self):
        self.client.stop()

    def draw_players(self, screen):
        for player in self.players.values():
            player.draw(screen)

    def update_local_player(self, x_move, y_move, color_change):
        self.players[self.player_uid].x += x_move
        self.players[self.player_uid].y += y_move
        self.players[self.player_uid].update_color(color_change)

        


manager = NetworkedPlayerManager(IP, PORT)

SCREEN_W, SCREEN_H = (400, 400)
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))


clock = pygame.time.Clock()



running = True

while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            manager.update_local_player(0, -3, 'black')

        if keys[K_DOWN]:
            manager.update_local_player(0, 3, 'red')

        if keys[K_LEFT]:
            manager.update_local_player(-3, 0, 'green')

        if keys[K_RIGHT]:
            manager.update_local_player(3, 0, 'blue')


        screen.fill((255, 255, 255))

        manager.update()
        manager.draw_players(screen)

        pygame.display.update()
        clock.tick(60)
    except KeyboardInterrupt:
        manager.leave()
        running = False
        print('Exiting...')

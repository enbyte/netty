import netty
import pickle
import pygame
from pygame.locals import *

pygame.init()

SCREEN_W, SCREEN_H = (500, 500)
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

p1 = pygame.Rect(0, 0, 50, 50)
p2 = pygame.Rect(0, 0, 50, 50)

SELF = p1
OTHER = p2


PORT = 1030

def echo(mes):
    data = mes.data
    if mes.uid == SELF_UID:
        SELF.x = data['x']
        SELF.y = data['y']
    else:
        OTHER.x = data['x']
        OTHER.y = data['y']

client = netty.connection.Client('', PORT, onReceive=echo)
client.start()
clock = pygame.time.Clock()

SELF_UID = client.uid

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        SELF.y -= 3

    if keys[K_DOWN]:
        SELF.y += 3

    if keys[K_LEFT]:
        SELF.x -= 3

    if keys[K_RIGHT]:
        SELF.x += 3

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (255, 0, 0), SELF)
    pygame.draw.rect(screen, (0, 255, 0), OTHER)

    client.send({'x': SELF.x, 'y': SELF.y})

    pygame.display.update()
    clock.tick(30)

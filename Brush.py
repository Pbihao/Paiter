# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from Data import *

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
screen.fill(COLOR_WHITE)
image = pygame.image.load("images/pen.png")
screen.blit(image, (400, 300))


while True:
    clock.tick(30)
    ok = True
    image = pygame.image.load("images/eraser.png")
    screen.blit(image, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            ok = False
            break
    if not ok:
        break
    pygame.display.update()
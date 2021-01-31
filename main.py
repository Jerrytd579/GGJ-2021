from game import *
import pygame, sys


g = Game(1280,720)
while g.should_stop():
    g.update()

pygame.quit()
sys.exit()


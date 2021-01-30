from game import *
import pygame

g = Game(1280,720)
while g.should_stop():
    g.update()

pygame.quit()
quit()
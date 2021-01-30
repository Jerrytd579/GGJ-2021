import math
import menu
import pygame
import pygame.freetype
from player import Dude
from enum import Enum
from map import Level

class GameStates(Enum):
    menu = 0
    park = 1
    minigame = 2

class Game:
    instance = None
    state = GameStates.menu
    flags = {}
    sprites = {} # for map object sprites

    def __init__(self, w, h):
        pygame.init()
        pygame.freetype.init()

        self.display_size = (w,h)
        self.display = pygame.display.set_mode((w,h))
        pygame.display.set_caption('hehe game')
        self.font = pygame.freetype.Font("MeleeSans.ttf")
        
        self.sprites['sign'] = pygame.image.load("sprites/sign.png")
        
        self.running = True
        self.justPressed = False
        
        self.camera = pygame.Rect(0,0,w,h)
        self.baseCamera = pygame.Rect(0,0,1,1) #used for rendering things without worrying about the camera following in the player
        self.clock = pygame.time.Clock()
        self.player = Dude(pygame.Rect(w * 0.5, h - 64, 64,64))
        self.level = Level()

        self.level.addWall(pygame.Rect(10,10,64,64))
        self.level.addWall(pygame.Rect(100,100,64,64))
        self.level.addWall(pygame.Rect(200,200,100,64))
        
    def should_stop(self):
        return self.running

    def render(self, img, rect, angle):
        self.display.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.w,rect.h)),angle), (rect.x - self.camera.x,rect.y - self.camera.y))

    def update(self):
        if(self.state == GameStates.menu):
            if(menu.menu_state(self.display, self.font, self.clock)):
                self.state = GameStates.park
        elif(self.state == GameStates.park):
            keyDown = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  
                    keyDown = True
                    justPressed = event.key
                else:
                    if event.type == pygame.QUIT:
                        self.running = False

            if (keyDown == False):
                self.justPressed = None
            
            self.display.fill((0,0,0))

            if (self.level.reading == ""):
                self.player.update(self.level, self.camera, self.clock, self.justPressed)

            else:
                surf, rect = self.font.render(self.level.reading,fgcolor = (1,1,1),bgcolor = (0,0,0),size = 100)  

                self.render(sign, pygame.Rect(10, 10, self.display_size[0] - 20, self.display_size[1] - 20), 0, self.baseCamera)
                self.render(surf, pygame.Rect(30, 30, rect.w, rect.h) , 0, self.baseCamera)
                if (justPressed == pygame.K_e):
                    self.level.reading = ""

            
            self.render(self.level.tilemap, pygame.Rect(0, 0, 1600,1344), 0)
            
            #TODO: Add wall rendering here
            for obj in self.level.objects:
                self.render(obj.img, obj.rect, 0)


            self.render(self.player.img, self.player.rect, 0)

            self.camera.x = self.player.rect.x + self.player.rect.w/2 - self.camera.w/2
            self.camera.y = self.player.rect.y + self.player.rect.h/2 - self.camera.h/2
                
            pygame.display.update()
            self.clock.tick(120)
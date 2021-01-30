import math
import menu
import pygame
import pygame.freetype
from player import Dude
from enum import Enum
from map import Level, TulipField

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

        self.camera.x = self.player.rect.x + self.player.rect.w/2 - self.camera.w/2
        self.camera.y = self.player.rect.y + self.player.rect.h/2 - self.camera.h/2

        self.level.addWall(pygame.Rect(10,10,64,64))
        self.level.addWall(pygame.Rect(100,100,64,64))
        self.level.addWall(pygame.Rect(200,200,100,64))
        self.level.addObject(TulipField(pygame.Rect(300,300,640,256),self))
        
    def should_stop(self):
        return self.running

    @staticmethod
    def blitToSurface(surface, img, rect, angle,camera): #in case other objects want to blit to a surface
        surface.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.w,rect.h)),angle), (rect.x - camera.x,rect.y - camera.y))
    
    def render(self, img, rect, angle,camera):
        self.blitToSurface(self.display,img,rect,angle,camera)

    def update(self):
        if(self.state == GameStates.menu):
            if(menu.menu_state(self.display, self.font, self.clock)):
                self.state = GameStates.park
                
                #TODO: this could be cleaned up or moved to a function

                fade = pygame.Surface((self.display_size[0], self.display_size[1]))
                self.display.blit(fade, pygame.Rect(0, 0, self.display_size[0], self.display_size[1]))
                fade.fill((0,0,0))
                for x in range(0, 255):
                    fade.set_alpha(255-x)

                    self.render(self.level.tilemap, pygame.Rect(0, 0, 1600,1344), 0,self.camera)

                    #TODO: Add wall rendering here
                    for obj in self.level.objects:
                        if(obj.rect.y < self.player.rect.y):
                            self.render(obj.img, obj.rect, 0,self.camera)

                        self.render(self.player.img, self.player.rect, 0,self.camera)

                        if(obj.rect.y > self.player.rect.y):
                                self.render(obj.img, obj.rect, 0)

                    self.display.blit(fade, pygame.Rect(0, 0, self.display_size[0], self.display_size[1]))
                    pygame.display.flip()
                    self.clock.tick(127.5)

                
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

            
            self.render(self.level.tilemap, pygame.Rect(0, 0, 1600,1344), 0,self.camera)

            #TODO: Add wall rendering here
            for obj in self.level.objects:
                if(obj.rect.y < self.player.rect.y):
                    self.render(obj.img, obj.rect, 0,self.camera)

                self.render(self.player.img, self.player.rect, 0,self.camera)

                if(obj.rect.y > self.player.rect.y):
                    self.render(obj.img, obj.rect, 0,self.camera)

            self.camera.x = self.player.rect.x + self.player.rect.w/2 - self.camera.w/2
            self.camera.y = self.player.rect.y + self.player.rect.h/2 - self.camera.h/2
                
            pygame.display.update()
            self.clock.tick(120)
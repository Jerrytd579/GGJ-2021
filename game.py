import math
import menu
import pygame
import pygame.freetype
from player import Dude
from enum import Enum
import map

TL_SZ = 32 # TILE SIZE

class GameStates(Enum):
    menu = 0
    park = 1
    minigame = 2

class Game:
    instance = None
    state = GameStates.menu
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
        self.justClicked = False
        
        self.camera = pygame.Rect(0,0,w,h)
        self.baseCamera = pygame.Rect(0,0,1,1) #used for rendering things without worrying about the camera following in the player
        self.clock = pygame.time.Clock()
        self.player = Dude(pygame.Rect(w * 0.5, h - 64, 64,64))
        self.level = map.Level()


        self.camera.x = self.player.rect.x + self.player.rect.w/2 - self.camera.w/2
        self.camera.y = self.player.rect.y + self.player.rect.h/2 - self.camera.h/2


        WATERWALL = ((11,6),(9,10),(7,12),(6,13),(6,14),(5,16),(5,16),(5,16),(5,16),(6,15),(6,14),(6,14),(7,11),(8,9),(8,7),(9,5))
        for x,y in enumerate(range(3,19)):
            self.level.addWall(pygame.Rect(WATERWALL[x][0] * TL_SZ, y * TL_SZ, WATERWALL[x][1] * TL_SZ, TL_SZ))

        #Outer walls
        self.level.addWall(pygame.Rect(0, 0, 50 * TL_SZ, TL_SZ))
        self.level.addWall(pygame.Rect(0, 41 * TL_SZ, 51 * TL_SZ, TL_SZ))
        self.level.addWall(pygame.Rect(0, TL_SZ, TL_SZ, 40 * TL_SZ))
        self.level.addWall(pygame.Rect(49 * TL_SZ, TL_SZ, TL_SZ, 40 * TL_SZ))
        self.level.addObject(map.TulipInteractable(pygame.Rect(300,300,64,128),self))
        self.tulips = map.TulipField(pygame.Rect(0,0,w,h),self)
        #Trees
        TREES = ((4,21),(4,36),(13,31),(19,30),(12,38),(18,37))
        for tree in TREES:
            self.level.addWall(pygame.Rect(tree[0] * TL_SZ, tree[1] * TL_SZ, TL_SZ, TL_SZ))
        
    def should_stop(self):
        return self.running

    @staticmethod
    def blitToSurface(surface, img, rect, angle, camera): #in case other objects want to blit to a surface
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

                        self.render(self.player.img, pygame.Rect(self.player.rect[0] - 16, self.player.rect[1] - 40, 64, 64), 0,self.camera)

                        if(obj.rect.y > self.player.rect.y):
                                self.render(obj.img, obj.rect, 0)

                    self.display.blit(fade, pygame.Rect(0, 0, self.display_size[0], self.display_size[1]))
                    pygame.display.flip()
                    self.clock.tick(127.5)

                
        else:
            keyDown = False
            self.justClicked = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  
                    keyDown = True
                    self.justPressed = event.key
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.justClicked = True
                elif event.type == pygame.QUIT:
                        self.running = False

            if (keyDown == False):
                self.justPressed = None
            if (self.state == GameStates.park):
                self.display.fill((0,0,0,0))

                if (self.level.reading == ""):
                    self.player.update(self.level, self.camera, self.clock, self.justPressed)

                else:
                    surf, rect = self.font.render(self.level.reading,fgcolor = (1,1,1),bgcolor = (0,0,0),size = 100)  

                    self.render(sign, pygame.Rect(10, 10, self.display_size[0] - 20, self.display_size[1] - 20), 0, self.baseCamera)
                    self.render(surf, pygame.Rect(30, 30, rect.w, rect.h) , 0, self.baseCamera)
                    if (self.justPressed == pygame.K_e):
                        self.level.reading = ""

                
                self.render(self.level.tilemap, pygame.Rect(0, 0, 1600,1344), 0,self.camera)

                #TODO: Add wall rendering here
                for obj in self.level.objects:
                    if(obj.rect.y < self.player.rect.y):
                        self.render(obj.img, obj.rect, 0,self.camera)

                    self.render(self.player.img, self.player.rect, 0,self.camera)
                    if (self.justPressed == pygame.K_g):
                        obj.grayscale()
                    if (obj.rect.y > self.player.rect.y):
                        self.render(obj.img,obj.rect,0,self.camera)


                self.camera.x = self.player.rect.x + self.player.rect.w/2 - self.camera.w/2
                self.camera.y = self.player.rect.y + self.player.rect.h/2 - self.camera.h/2
            else:
                self.display.blit(self.tulips.img, pygame.Rect(0, 0, self.display_size[0], self.display_size[1]))   
                self.display.blit(self.tulips.mask, pygame.Rect(0, 0, self.display_size[0], self.display_size[1]))   
                self.tulips.update()
                self.render(self.player.img, pygame.Rect(self.player.rect[0] -16, self.player.rect[1] - 40, 64, 64), 0,self.camera)

                if(obj.rect.y > self.player.rect.y):
                    self.render(obj.img, obj.rect, 0,self.camera)

            pygame.display.update()
            self.clock.tick(120)

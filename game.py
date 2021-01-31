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
    textbox = 3

class Game:
    instance = None
    state = GameStates.menu
    entered_text = ""
    sprites = {} # for map object sprites
    colored_areas = []

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

    def draw_scene_park(self):
        self.render(self.level.tilemap, pygame.Rect(0, 0, 1600,1344), 0,self.camera)

        if(self.player.flags['color_area_1'] and (1 not in self.colored_areas)):
            self.level.reloadTilemap(2, True)
            self.colored_areas.append(1)

        for obj in self.level.objects:
            if(obj.rect.y <= self.player.rect.y):
                self.render(obj.img, obj.rect, 0,self.camera)

            self.render(self.player.img, pygame.Rect(self.player.rect[0] -16, self.player.rect[1] - 40, 64, 64), 0,self.camera)

            if(obj.rect.y > self.player.rect.y):
                self.render(obj.img, obj.rect, 0,self.camera)

        if(self.player.reading != ""):
            surf, rect = self.font.render(self.player.reading,fgcolor = (255,255,255), size = 32)  
            
            pygame.draw.rect(self.display, (0,0,0), pygame.Rect(0, 600, 1280, 120))
            pygame.draw.rect(self.display, (255,255,255), pygame.Rect(0, 590, 1280, 10))
            self.display.blit(surf, pygame.Rect(10, 610, rect.w, rect.h))

    def update(self):
        if(self.state == GameStates.menu):
            if(menu.menu_state(self.display, self.font, self.clock)):
                self.state = GameStates.park
                

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

        elif(self.state == GameStates.textbox):
            self.draw_scene_park()

            pygame.draw.rect(self.display, (255,255,255), pygame.Rect((1280 / 2) - 460, (720 / 2) - 74, 920, 148))
            pygame.draw.rect(self.display, (0,0,0), pygame.Rect((1280 / 2) - 450, (720 / 2) - 64, 900, 128))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if(event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE):
                        self.entered_text += pygame.key.name(event.key)
                    elif(event.key == pygame.K_BACKSPACE):
                        self.entered_text = self.entered_text[0:-1]
                    else:
                        print("check riddles or whatever here")
                        self.entered_text = ""
                        self.state = GameStates.park
                
            surf, rect = self.font.render(self.entered_text, fgcolor = (255,255,255), size = 32)  
            
            self.display.blit(surf, pygame.Rect((1280 / 2) - 440, (720 / 2) - 54, rect.w, rect.h))

            pygame.display.update()

        elif(self.state == GameStates.park):
            keyDown = False
            self.justClicked = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  
                    keyDown = True
                    justPressed = event.key

                    if(event.key == pygame.K_1):
                        self.state = GameStates.textbox

                    if(event.key == pygame.K_2):
                        self.player.flags['color_area_1'] = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.justClicked = True
                elif event.type == pygame.QUIT:
                        self.running = False

            if (keyDown == False):
                self.justPressed = None
            if (self.state == GameStates.park):
                self.display.fill((0,0,0,0))

            if (self.player.reading == ""):
                self.player.update(self.level, self.camera, self.clock, self.justPressed)
            
            if (pygame.K_e in pygame.key.get_pressed()):
                self.player.reading = ""

            self.draw_scene_park()
            
            self.camera.x = self.player.rect.x + self.player.rect.w/2 - self.camera.w/2
            self.camera.y = self.player.rect.y + self.player.rect.h/2 - self.camera.h/2

            pygame.display.update()
            self.clock.tick(120)

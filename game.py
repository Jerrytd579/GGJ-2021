import math
import menu
import pygame
import os.path
import pygame.freetype
from player import Dude
from enum import Enum
import map

TL_SZ = 32 # TILE SIZE
bush_img = pygame.image.load("objects/bush.png")


class GameStates(Enum):
    menu = 0
    park = 1
    minigame = 2
    textbox = 3
    finished =4

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
        pygame.display.set_caption('Simple Things')
        self.font = pygame.freetype.Font("MeleeSans.ttf")
        
        self.running = True
        self.justPressed = False
        self.justClicked = False
        
        self.camera = pygame.Rect(0,0,w,h)
        self.baseCamera = pygame.Rect(0,0,1,1) #used for rendering things without worrying about the camera following in the player
        self.clock = pygame.time.Clock()
        self.player = Dude(pygame.Rect(w * 0.5 + 16, h - 24, 32,24))
        self.level = map.Level()
        self.finishImage = pygame.image.load("sprites/njit-endscreen.png")

        if (os.path.isfile("finished.txt")):
            self.finish()

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
        self.level.addObject(map.TulipInteractable(pygame.Rect(600,300,64,128),self))
        self.level.addObject(map.Wheel(pygame.Rect(900,900,128,128)))
        self.level.addObject(map.Bench(pygame.Rect(800,0,128,128),self))
        self.tulips = map.TulipField(pygame.Rect(0,0,w,h),self)
  
        #Trees
        TREES = ((4,21),(4,36),(13,31),(19,30),(12,38),(18,37))
        for tree in TREES:
            self.level.addWall(pygame.Rect(tree[0] * TL_SZ, tree[1] * TL_SZ, TL_SZ, TL_SZ))
        #Bushes
        BUSHES = ((2,3),(21,2),(2,14),(13,21),(16,18),(19,18),(29,4),(45,6),(38,17),(28,24),(28,34),(6,30))
        for bush in BUSHES:
            self.level.addWall(pygame.Rect(bush[0] * TL_SZ + 4, bush[1] * TL_SZ + 4, 56, 56))
        self.level.addWall(pygame.Rect(42 * TL_SZ + 16, 15 * TL_SZ + 8, 44, 52))
        
    def should_stop(self):
        return self.running
    def finish(self):
        pygame.mixer_music.load('music/njit-endtheme.wav')
        pygame.mixer_music.play()
        self.state = GameStates.finished
    @staticmethod
    def blitToSurface(surface, img, rect, angle, camera): #in case other objects want to blit to a surface
        surface.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.w,rect.h)),angle), (rect.x - camera.x,rect.y - camera.y))
    
    def render(self, img, rect, angle,camera):
        self.blitToSurface(self.display,img,rect,angle,camera)

    def draw_scene_park(self):
        self.render(self.level.tilemap, pygame.Rect(0, 0, 1600,1344), 0,self.camera)

        if((2 not in self.colored_areas) and self.player.flags['color_area_1']):
            self.level.reloadTilemap(2)
            self.colored_areas.append(2)

        if((3 not in self.colored_areas) and self.player.flags['color_area_3']):
            self.level.reloadTilemap(3)
            self.colored_areas.append(3)

        if((4 not in self.colored_areas) and self.player.flags['color_area_4']):
            self.level.reloadTilemap(4)
            self.colored_areas.append(4)

        if((5 not in self.colored_areas) and self.player.flags['color_area_5']):
            self.level.reloadTilemap(5)
            self.colored_areas.append(5)

        if((6 not in self.colored_areas) and self.player.flags['color_area_6']):
            self.level.reloadTilemap(6)
            self.colored_areas.append(6)

        for obj in self.level.objects:
            if(obj.rect.y <= self.player.rect.y + self.player.rect.h):
                self.render(self.player.img, pygame.Rect(self.player.rect[0] -16, self.player.rect[1] - 40, 64, 64), 0,self.camera)
            if (obj.img != None):
                self.render(obj.img, obj.rect, 0,self.camera)

        if(self.player.reading != ""):
            surf, rect = self.font.render(self.player.reading,fgcolor = (255,255,255), size = 32)  
            
            pygame.draw.rect(self.display, (0,0,0), pygame.Rect(0, 600, 1280, 120))
            pygame.draw.rect(self.display, (255,255,255), pygame.Rect(0, 590, 1280, 10))
            self.display.blit(surf, pygame.Rect(10, 610, rect.w, rect.h))

    def update(self):
        self.justPressed = None
        self.justClicked = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  
                self.justPressed = event.key
            
                if(event.key == pygame.K_1):
                    self.state = GameStates.textbox

                if(event.key == pygame.K_2):
                    self.player.flags['color_area_1'] = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.justClicked = True
            elif event.type == pygame.QUIT:
                    self.running = False
        if(self.state == GameStates.menu):
            if(menu.menu_state(self.display, self.font, self.clock)):
                self.state = GameStates.park
                

                fade = pygame.Surface((self.display_size[0], self.display_size[1]))
                self.display.blit(fade, pygame.Rect(0, 0, self.display_size[0], self.display_size[1]))
                fade.fill((0,0,0))
                for x in range(0, 255):
                    fade.set_alpha(255-x)

                    self.render(self.level.tilemap, pygame.Rect(0, 0, 1600,1344), 0,self.camera)

                    #Don't need ordered rendering here since you arent overlapping anything at the start
                    for obj in self.level.objects:
                        if (obj.img != None):
                            self.render(obj.img, obj.rect, 0,self.camera)

                    self.render(self.player.img, pygame.Rect(self.player.rect[0] -16, self.player.rect[1] - 40, 64, 64), 0,self.camera)

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

            self.display.fill((0,0,0,0))

            if (self.player.reading == ""):
                self.player.update(self.level, self.camera, self.clock, self.justPressed)
            
            if (pygame.K_e in pygame.key.get_pressed()):
                self.player.reading = ""

            self.draw_scene_park()
            
            self.camera.x = self.player.rect.x + self.player.rect.w/2 - self.camera.w/2
            self.camera.y = self.player.rect.y + self.player.rect.h/2 - self.camera.h/2
            ##
            self.render(bush_img,pygame.Rect(200,700,64,64),0,self.camera)

            pygame.display.update()
            self.clock.tick(120)
        elif self.state == GameStates.minigame:
            self.render(self.tulips.img,pygame.Rect(0,0,self.display_size[0],self.display_size[1]),0,self.baseCamera)
            self.render(self.tulips.mask,pygame.Rect(0,0,self.display_size[0],self.display_size[1]),0,self.baseCamera)
            self.tulips.update()
            pygame.display.update()
            self.clock.tick(120)
        elif self.state == GameStates.finished:

            self.render(self.finishImage,pygame.Rect(0,0,self.display_size[0],self.display_size[1]),0,self.baseCamera)
            pygame.display.update()
            self.clock.tick(120)
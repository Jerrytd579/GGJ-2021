import pygame
import json
import random
import os.path
import random

from map_data.tile_set import tile_images as color_tiles
from map_data.tile_set_gray import tile_images as gray_tiles

def loadTilemapAsSurface(tilemap_path, use_gray_tileset=False, use_surface=None):
    map_surface = None

    if(use_surface != None):
        map_surface = use_surface
    else:
        map_surface = pygame.Surface((1600,1344))

    tilemap = open(tilemap_path, 'r')
    tiles = tilemap.read().replace('\n',',').split(',')
    tilemap.close()
    tile_imgs = None

    if(use_gray_tileset):
        tile_imgs = gray_tiles    
    else:
        tile_imgs = color_tiles

    for y in range(0, 42):
        for x in range(0,50):
            tile = int(tiles[(y * 50) + x])
            if(tile > 0 and tile < len(tile_imgs)):
                map_surface.blit(pygame.transform.scale(tile_imgs[tile], (32,32)), (x*32, y*32))

    return map_surface

def loadMapObjects(level):
    f = open('map.json') 
    map_dict = json.load(f)

    used_button_indices = []

    for string in map_dict:
        obj = map_dict[string]
        if(obj['type'].lower() == "sign"):
            interact = pygame.Rect(obj['interact_range']['x'], obj['interact_range']['y'],  obj['interact_range']['w'], obj['interact_range']['h'])
            s = Sign(obj['message'], interact, obj['sprite'])
            level.addObject(s)
    
        if(obj['type'].lower() == "button"):
            interact = pygame.Rect(obj['interact_range']['x'], obj['interact_range']['y'],  obj['interact_range']['w'], obj['interact_range']['h'])
            
            s = None
            if("sprite" not in obj):
                s = Button(obj['enable_flag'], interact, None)
            else:
                s = Button(obj['enable_flag'], interact, obj['sprite'])

            s.index = s.index = random.randint(0,4)
            while(s.index in used_button_indices):
                s.index = random.randint(0,4)

            level.addObject(s)
    
    level.objects.sort(key=lambda obj: obj.rect.y)

class Level:
    walls = []
    objects = [] #anything that can be interacted with

    def __init__(self):
        self.tilemap = loadTilemapAsSurface('map_data/map_Layer1.csv')
        loadMapObjects(self)


    def reloadTilemap(self, area_count, use_gray):
        for x in range(2, area_count+1):
            self.tilemap = loadTilemapAsSurface(f'map_data/map_Layer{x}.csv', use_gray, self.tilemap)

    def addWall(self, wall):
        self.walls.append(wall)

    def addObject(self, obj):
        self.objects.append(obj)    

class Interactable:  #parent class of anything that can be interacted with
    spritePath = None
    def __init__(self, rect, spritePath):
        self.rect = rect
        self.spritePath = spritePath
        if spritePath != None:
            self.img = pygame.image.load(spritePath)
        else:
            self.img = None
    def grayscale(self):
        if (self.spritePath != None):
            #print(self.spritePath)
            grayscale = "sprites_grey" + self.spritePath[self.spritePath.find("/"): -4] +  "_g.png"
            if (os.path.isfile(grayscale)):
                self.img = pygame.image.load(grayscale)
        #self.img = pygame.image.load()

    def interact(self,dude):
        print("Blank interact function")

class Sign(Interactable):
    def __init__(self, message, rect, spritePath):
        Interactable.__init__(self, rect, spritePath)
        self.message = message
    def interact(self,dude):
        dude.reading = self.message

class TulipInteractable(Interactable):
    def __init__(self,rect,game):
        Interactable.__init__(self,rect,"sprites/tulip.png")
        self.game = game
    def interact(self,dude):
        import game
        self.game.state = game.GameStates.minigame
        self.game.display.fill((0,0,0,0))

class Button(Interactable):
    def __init__(self, enableFlag, rect, spritePath):
        Interactable.__init__(self, rect, spritePath)
        self.enableFlag = enableFlag
        self.enabled = False
        self.index = -1
#dylan
class Sprite(Interactable):
    def __init__(self, rect, spritePath):
        Interactable.__init__(self, rect, spritePath)

    def interact(self, dude):
        if(not self.enabled):
            if(not dude.flags['trees_complete'] and dude.flags['current_index'] == self.index):
                dude.flags[f"button_{self.enableFlag}"] = True
                self.enabled = True
                dude.flags['current_index'] += 1
            else:
                for x in range(0, dude.flags['current_index']):
                    dude.flags[f"button_{x}"] = False
                    dude.flags['current_index'] = 0

            if(dude.flags['current_index'] == 4):
                dude.flags['trees_complete'] = True

class TulipField:
    curTulip = []
    curCounter = []
    dimen = 64 #width and height of each tulip
    tulipPerRow = 0
    correct = 0 #number of tulips clicked
    curTulipImg = None #alternate surface for red tulips
    wins = 0
    tulipImg = None
    startPos = None
    def __init__(self,rect, game):
        Interactable.__init__(self,rect,None)
        self.img = pygame.Surface((rect.w,rect.h))
        self.mask = pygame.Surface((rect.w,rect.h), flags = pygame.SRCALPHA  )
        self.mask.fill((0,0,0,0))
        self.tulipPerRow = 5#self.rect.w//self.dimen #number of tulips per row
        self.tulipPerCol = 5#self.rect.h//self.dimen #number of tulips per column
        self.tulipImg = pygame.image.load("objects/flower_g.png")
        self.curTulipImg = pygame.image.load("objects/flower.png")
        self.game = game
        self.startPos = (self.rect.w//self.dimen//2 - self.tulipPerRow//2,self.rect.h//self.dimen//2 - self.tulipPerCol//2)
        for i in range(self.tulipPerRow):
            for j in range(self.tulipPerCol):
                pos = ((i + self.startPos[0])*self.dimen,(j + self.startPos[1])*self.dimen)
                rect = pygame.Rect(pos[0],pos[1],self.dimen,self.dimen)

                self.game.blitToSurface(self.img,self.tulipImg,rect,0,self.game.baseCamera)
    def showBlinks(self):
        self.curCounter = []
        for i in self.curTulip:
            pos = (i[0],i[1])
            rect = pygame.Rect(pos[0],pos[1],self.dimen,self.dimen)
            #pygame.draw.rect(self.img,(0,255,255,1),rect)
            self.game.blitToSurface(self.mask,self.curTulipImg,rect,0,pygame.Rect(0,0,0,0))
            self.curCounter.append(False)
            
    def update(self):
        if (self.wins < 6):
            import game
            mousePos = pygame.mouse.get_pos()
            clicked = False
            for i in (self.curTulip):
                pos = (i[0],i[1])
                rect = pygame.Rect(pos[0],pos[1],self.dimen,self.dimen)
                if rect.collidepoint(mousePos) and self.game.justClicked:
                    if pos in self.curTulip:
                        clicked = True
                        if (pos not in self.curCounter):
                            self.game.blitToSurface(self.mask,self.curTulipImg,rect,0,pygame.Rect(0,0,0,0))
                            self.curCounter.append(pos)
            if self.game.justClicked and not clicked: #clicked a tulip that's not part of the list
                self.curCounter = []
                self.mask.fill((0,0,0,0))
                
            if len(self.curCounter) == len(self.curTulip):
            
                pos = (random.randrange(0,self.tulipPerRow),random.randrange(0,self.tulipPerCol))
                while pos in self.curTulip:
                    pos = (random.randrange(0,self.tulipPerRow),random.randrange(0,self.tulipPerCol))
                pos = ((pos[0] + self.startPos[0])*self.dimen,(pos[1] + self.startPos[1])*self.dimen)
                self.curTulip.append(pos)
                self.game.blitToSurface(self.mask,self.curTulipImg,pygame.Rect(pos[0],pos[1],self.dimen,self.dimen),0,pygame.Rect(0,0,0,0))
                self.game.display.blit(self.mask,pygame.Rect(0, 0, self.game.display_size[0], self.game.display_size[1])) 
                pygame.display.update()
                pygame.time.wait(2000) 
                self.mask.fill((0,0,0,0))
                self.curCounter = []
                self.wins += 1
        else:
            import game
            self.game.state = game.GameStates.park
def load_map_objects(level):
    f = open('map.json') 
    map_dict = json.load(f)

    for string in map_dict:
        obj = map_dict[string]
        if(obj['type'].lower() == "sign"):
            interact = pygame.Rect(obj['interact_range']['x'], obj['interact_range']['y'],  obj['interact_range']['w'], obj['interact_range']['h'])
            s = Sign(obj['message'], interact, obj['sprite'])
            
            level.addObject(s)
            
            
            

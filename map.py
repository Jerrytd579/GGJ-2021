import pygame
import json
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

    for string in map_dict:
        obj = map_dict[string]
        if(obj['type'].lower() == "sign"):
            interact = pygame.Rect(obj['interact_range']['x'], obj['interact_range']['y'],  obj['interact_range']['w'], obj['interact_range']['h'])
            s = Sign(obj['message'], interact, obj['sprite'])
            
            level.addObject(s)

class Level:
    reading = ""
    walls = []
    objects = [] #anything that can be interacted with

    def __init__(self):
        self.tilemap = loadTilemapAsSurface('map_data/map_Layer1.csv')
        loadMapObjects(self)


    def reloadTilemap(self, path, use_gray):
        self.tilemap = loadTilemapAsSurface(path, use_gray, self.tilemap)

    def addWall(self, wall):
        self.walls.append(wall)

    def addObject(self, obj):
        self.objects.append(obj)

    

class Interactable:  #parent class of anything that can be interacted with
    def __init__(self, rect, spritePath):
        self.rect = rect
        if spritePath != None:
            self.img = pygame.image.load(spritePath)
        else:
            self.img = None
    def update(self,camera):
        import main
        main.render(self.img,self.rect,0,camera)
    def interact(self,dude):
        print("Blank interact function")

class Sign(Interactable):
    def __init__(self, message, rect, spritePath):
        Interactable.__init__(self, rect, spritePath)
        self.message = message
    def interact(self,dude):
        from main import l
        l.reading = self.message

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
    
    def interact(self, dude):
        if(not self.enabled):
            dude.flags[self.enabledFlag] = True
            self.enabled = True

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
        self.tulipImg = pygame.image.load("sprites/tulip.png")
        self.curTulipImg = self.tulipImg.copy()
        self.curTulipImg.fill((200,0,0,0), special_flags=pygame.BLEND_RGB_ADD)
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
            
            
            

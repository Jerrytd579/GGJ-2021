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

class TulipField(Interactable):
    tulips = []
    curTulip = -1
    dimen = 64 #width and height of each tulip
    tulipSet = set() #set of positions where a tulip has been added
    tulipPerRow = 0
    correct = 0 #number of tulips clicked
    def __init__(self,rect):
        import main
        Interactable.__init__(self,rect,None)
        self.tulipPerRow = self.rect.w/self.dimen #number of tulips per row
        self.curTulipImg = main.tulipImg.copy()
        for i in range(20):
            key = self.randomTulip()
            while (key in self.tulipSet):
                key = self.randomTulip()
            self.tulipSet.add(key)
            pos = self.keyToPos(key)
            self.tulips.append((pos[0],pos[1]))
        self.curTulip = random.choice(tuple(self.tulipSet))
    def randomTulip(self):#returns the key of a random tulip
        x = random.randrange(0,self.tulipPerRow)
        y = random.randrange(0,self.rect.h/self.dimen)
        return y*self.tulipPerRow + x
    def keyToPos (self, key):
        return (self.rect.x + key%(self.tulipPerRow)*self.dimen,self.rect.y + key//(self.tulipPerRow)*self.dimen)
    def convertPosToKey(self, pos): #takes coordinates of a tulip and converts it to the index
        return (pos[1]-self.rect.y)/self.dimen*self.tulipPerRow + (pos[0] - self.rect.x)/self.dimen
    def update(self,camera):
        import main
        pos = self.keyToPos(self.curTulip)
        #pygame.draw.rect(main.gameDisplay,main.black,pygame.Rect(self.rect.x + pos[0] - camera.x,self.rect.y + pos[1] - camera.y,self.dimen,self.dimen))
        #while (newTulip == self.curTulip):
        #    newTulip = self.randomTulip()
        self.curTulipImg.fill((1,0,0,0), special_flags=pygame.BLEND_RGB_ADD)
        for i in self.tulips:
            if  self.convertPosToKey(i) == self.curTulip or self.correct >= 3:
                main.render(self.curTulipImg,pygame.Rect(i[0],i[1],self.dimen,self.dimen),0,camera)
            else:
                main.render(main.tulipImg,pygame.Rect(i[0],i[1],self.dimen,self.dimen),0,camera)
    def interact(self,dude):
        pos = self.keyToPos(self.curTulip)
        if dude.rect.colliderect(pygame.Rect(pos[0],pos[1],self.dimen,self.dimen)):
            self.curTulip = random.choice(tuple(self.tulipSet))
            self.correct += 1
        
def load_map_objects(level):
    f = open('map.json') 
    map_dict = json.load(f)

    for string in map_dict:
        obj = map_dict[string]
        if(obj['type'].lower() == "sign"):
            interact = pygame.Rect(obj['interact_range']['x'], obj['interact_range']['y'],  obj['interact_range']['w'], obj['interact_range']['h'])
            s = Sign(obj['message'], interact, obj['sprite'])
            
            level.addObject(s)
            
            
            
            
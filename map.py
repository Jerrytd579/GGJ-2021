import pygame
import json

def loadTilemapAsSurface(tilemap_path):
    mapSurface = pygame.Surface((1600,1344))

    tilemap = open(tilemap_path, 'r')
    tiles = tilemap.read().replace('\n',',').split(',')
    tilemap.close()
    tile_imgs = [pygame.image.load("sprites/path_right_grass.png"), pygame.image.load("sprites/path_left_grass.png"), pygame.image.load("sprites/path.png")]

    for y in range(0, 42):
        for x in range(0,50):
            tile = int(tiles[(y * 50) + x])
            if(tile != 3):
                mapSurface.blit(pygame.transform.scale(tile_imgs[tile], (32,32)), (x*32, y*32))

    return mapSurface

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
        self.tilemap = loadTilemapAsSurface('test.csv')
        loadMapObjects(self)

    def addWall(self,wall):
        self.walls.append(wall)

    def addObject(self,obj):
        self.objects.append(obj)

class Interactable:  #parent class of anything that can be interacted with
    def __init__(self,rect, spritePath):
        self.rect = rect
        self.img = pygame.image.load(spritePath)

    def interact(self):
        print("Blank interact function")

class Sign(Interactable):
    def __init__(self,message,rect,spritePath):
        Interactable.__init__(self,rect,spritePath)
        self.message = message

    def interact(self):
        from main import l
        l.reading = self.message

            
            
            
            
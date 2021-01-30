import pygame
import json

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
        self.img = pygame.image.load(spritePath)

    def interact(self):
        print("Blank interact function")

class Sign(Interactable):
    def __init__(self, message, rect, spritePath):
        Interactable.__init__(self, rect, spritePath)
        self.message = message

    def interact(self):
        from main import l
        l.reading = self.message

            
            
            
            
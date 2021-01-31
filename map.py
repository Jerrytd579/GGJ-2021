import pygame
import json
import random
import os.path
import random

from map_data.tile_set import tile_images as color_tiles
from map_data.tile_set_gray import tile_images as gray_tiles
# gray_tiles = {}
for i in color_tiles:
    # grayscale = ("sprites_grey" + color_tiles[i][color_tiles[i].find("/"): -4] +  "_g.png")
    # if os.path.isfile(grayscale):
        # gray_tiles[i] = pygame.image.load(grayscale)
    # else:
        # print(grayscale)

    color_tiles[i] = pygame.image.load(color_tiles[i])

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
                if (tile not in tile_imgs):
                    map_surface.blit(pygame.transform.scale(color_tiles[tile], (32,32)), (x*32, y*32))
                else:
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
            
            used_button_indices.append(s.index)

            s.grayscale()

            level.addObject(s)

class Level:
    walls = []
    objects = [] #anything that can be interacted with
    map_img = None
    map_layers = [pygame.image.load('sprites/color_map.png'), pygame.image.load('sprites/quad_1.png'), pygame.image.load('sprites/quad_2.png'), pygame.image.load('sprites/quad_3.png'), pygame.image.load('sprites/quad_4.png')]

    def __init__(self):
        self.map_img = pygame.Surface((1600,1344))
        for layer in self.map_layers:
            self.map_img.blit(pygame.transform.scale(layer, (1600,1344)), (0,0))
        
        loadMapObjects(self)

    def update_mapimg(self, index):
        self.map_layers.pop(index)
        for layer in self.map_layers:
            self.map_img.blit(pygame.transform.scale(layer, (1600,1344)), (0,0))

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
    def grayscale(self, setGray=True):
        if (self.spritePath != None):
            if(setGray):
                #print(self.spritePath)
                grayscale = "sprites_grey" + self.spritePath[self.spritePath.find("/"): -4] +  "_g.png"
                if (os.path.isfile(grayscale)):
                    self.img = pygame.image.load(grayscale)
            else:
                self.img = pygame.image.load(self.spritePath)
            

    def interact(self,dude):
        print("Blank interact function")

class Bench(Interactable):
    def __init__(self, rect,game):
        Interactable.__init__(self,rect,"objects/bench.png")
        self.game = game
    def interact(self, dude):
        self.game.finish()
        open("finished.txt", "x")
        

class Sign(Interactable):
    def __init__(self, message, rect, spritePath):
        Interactable.__init__(self, rect, spritePath)
        self.message = message
    def interact(self,dude):
        dude.reading = self.message

class TulipInteractable(Interactable):
    def __init__(self,rect,game):
        Interactable.__init__(self,rect,None)
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

    def interact(self, dude):
        if(not self.enabled):
            self.grayscale()
            print(f"{self.index} : {dude.flags['current_index']}")
            if(not dude.flags['trees_complete'] and dude.flags['current_index'] == self.index):
                dude.flags[f"button_{self.enableFlag}"] = True
                self.enabled = True
                dude.flags['current_index'] += 1
                self.grayscale(False)
            else:
                for x in range(0, dude.flags['current_index']):
                    dude.flags[f"button_{x}"] = False
                    dude.flags['current_index'] = 0

            if(dude.flags['current_index'] == 4):
                dude.flags['trees_complete'] = True

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

class Wheel(Interactable):
    part = 4
    def __init__(self,rect):
        Interactable.__init__(self,rect,"objects/wheel4.png")
    def interact(self,dude):
        self.part -= 1
        if (self.part >= 1):
            self.img = pygame.image.load("objects/wheel" + str(self.part)+".png")
        if (self.part == 1):
            dude.flags['color_area_4'] = not dude.flags['color_area_4']
            

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
                pos = ((pos[0] + self.startPos[0])*self.dimen,(pos[1] + self.startPos[1])*self.dimen)
                while pos in self.curTulip:
                    pos = (random.randrange(0,self.tulipPerRow),random.randrange(0,self.tulipPerCol))
                    pos = ((pos[0] + self.startPos[0])*self.dimen,(pos[1] + self.startPos[1])*self.dimen)
                #pos = ((pos[0] + self.startPos[0])*self.dimen,(pos[1] + self.startPos[1])*self.dimen)
                #print(pos)
                self.curTulip.append(pos)
                self.showBlinks()
                #self.game.blitToSurface(self.mask,self.curTulipImg,pygame.Rect(pos[0],pos[1],self.dimen,self.dimen),0,pygame.Rect(0,0,0,0))
                self.game.display.blit(self.mask,pygame.Rect(0, 0, self.game.display_size[0], self.game.display_size[1])) 
                pygame.display.update()
                pygame.time.wait(2000) 
                self.mask.fill((0,0,0,0))
                self.curCounter = []
                self.wins += 1
        else:
            import game
            self.game.state = game.GameStates.park
            self.game.level.active_stages.remove(1)
import pygame
import json
import random

###########
# You should move this code into main or another python file
from enum import Enum

class GameStates(Enum):
    menu = 0
    park = 1
    minigame = 2

class State:
    instance = None
    state = GameStates.menu
    flags = {}
    game_map = {}

    @staticmethod
    def inst():
        if(isinstance == None):
            State()

        return State.instance

    def __init__(self):
        if not State.instance:
            State.instance = self



########

    

class Interactable:  #parent class of anything that can be interacted with
    def __init__(self,rect, spritePath):
        self.rect = rect
        if spritePath != None:
            self.img = pygame.image.load(spritePath)
    def update(self,camera):
        import main
        main.render(self.img,self.rect,0,camera)
    def interact(self,dude):
        print("Blank interact function")

class Sign(Interactable):
    def __init__(self,message,rect,spritePath):
        Interactable.__init__(self,rect,spritePath)
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
            
            
            
            
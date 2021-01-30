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
    def interact(self):
        print("Blank interact function")

class Sign(Interactable):
    def __init__(self,message,rect,spritePath):
        Interactable.__init__(self,rect,spritePath)
        self.message = message
    def interact(self):
        from main import l
        l.reading = self.message

class TulipField(Interactable):
    tulips = []
    curTulip = -1
    def __init__(self,rect):
        Interactable.__init__(self,rect,None)
        for i in range(20):
            self.tulips.append((random.randint(rect.x,rect.x + rect.w),random.randint(rect.y,rect.y + rect.h)))
    def update(self,camera):
        import main
        for i in self.tulips:
            main.render(main.tulipImg,pygame.Rect(i[0],i[1],64,64),0,camera)

def load_map_objects(level):
    f = open('map.json') 
    map_dict = json.load(f)

    for string in map_dict:
        obj = map_dict[string]
        if(obj['type'].lower() == "sign"):
            interact = pygame.Rect(obj['interact_range']['x'], obj['interact_range']['y'],  obj['interact_range']['w'], obj['interact_range']['h'])
            s = Sign(obj['message'], interact, obj['sprite'])
            
            level.addObject(s)
            
            
            
            
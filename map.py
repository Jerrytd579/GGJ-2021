import pygame
import json

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

def load_map_objects(level):
    map_dict = json.loads('map.json')

    for obj in map_dict:
        if(obj['type'].lower() == "sign"):
            interact = pygame.Rect(obj['interact_range']['x'], obj['interact_range']['y'], obj['interact_range']['x'], obj['interact_range']['w'], obj['interact_range']['h'])
            s = Sign(obj['message'], interact, obj['sprite'])
            
            level.addObject(s)
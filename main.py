import pygame
import esper
import math

pygame.init()
#

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')

black = (0,0,0)
white = (255,255,255) 

clock = pygame.time.Clock()
crashed = False

class Rect:
    def __init__(self,x,y,z,a):
        self.x = x
        self.y = y
        self.z = z;
        self.a = a

class MoveComponent:
    def __init__(self,rect):
        self.rect = rect
        self.speed = pygame.Vector2(0,0)
        self.velocity = 1
        self.accel = pygame.Vector2(0,0)
        self.angle = 90
        
class MoveProcessor(esper.Processor):
    def process(self):
        keys = pygame.key.get_pressed();
        for ent,rec in self.world.get_component(MoveComponent):
            if (keys[pygame.K_SPACE]):
                rec.speed[1] += rec.velocity*(math.sin(rec.angle/180*math.pi))
                rec.speed[0] += rec.velocity*(math.cos(rec.angle/180*math.pi))
            if (keys[pygame.K_RIGHT]):
                rec.angle -= 1
            elif keys[pygame.K_LEFT]:
                rec.angle += 1
            rec.angle = max(0,min(rec.angle, 180))
            rec.speed[1] -= .1
            rec.rect.y -= rec.speed[1]
            rec.rect.x += rec.speed[0]
            render(ent.img,rec.rect,rec.angle)
        

class Rocket:
    def __init__(self):
        global world
        self.img = pygame.image.load('sprites/blastRocket.png')
        world.add_component(self,MoveComponent(Rect(display_width*.5,display_height - 64, 64,64)))
def render(img,rect,angle):
    gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.z,rect.a)),angle), (rect.x,rect.y))

world = esper.World()
move = MoveProcessor()
world.add_processor(move)
r = Rocket()
camera = Rect(0,0,display_width,display_height)
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    rect = world.component_for_entity(r,MoveComponent).rect
    camera.x = rect.x + rect.z/2 - camera.z/2
    camera.y = rect.y + rect.a/2 - camera.a/2
        
    world.process()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
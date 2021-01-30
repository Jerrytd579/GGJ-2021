import pygame
import math

pygame.init()
#

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Title here')

mapSurface = pygame.Surface((1538,1280))

black = (0,0,0)
white = (255,255,255) 

clock = pygame.time.Clock()
closed = False      

class Level:
    walls = []
    def addWall(self,wall):
        self.walls.append(wall)
    def update(self,camera):
        for i in self.walls:
            pygame.draw.rect(gameDisplay,black,i.move(-1*camera.x,-1*camera.y))

class Dude:
    def __init__(self, rect):
        self.rect = rect
        self.img = pygame.image.load('sprites/blastRocket.png')
    def update(self,level):
        keys = pygame.key.get_pressed();
        velocity = .25
        velocity *= clock.get_time()
        speeds = pygame.Vector2(0,0)
        if (keys[pygame.K_RIGHT]):
            speeds[0] += velocity
        elif keys[pygame.K_LEFT]:
            speeds[0] -= velocity
        if keys[pygame.K_UP]:
            speeds[1] -= velocity
        elif keys[pygame.K_DOWN]:
            speeds[1] += velocity
        render(self.img,self.rect,0)
        horizRect = self.rect.move(speeds[0],0)
        vertRect = self.rect.move(0,speeds[1])
        collidedHoriz = True
        collidedVert = True
        for i in level.walls:
            if i.colliderect(horizRect):
                collidedHoriz = False
            if i.colliderect(vertRect):
                collidedVert = False;
        if collidedHoriz:
            self.rect.x = horizRect.x
        if collidedVert:
            self.rect.y = vertRect.y
                
def render(img,rect,angle):
    gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.w,rect.h)),angle), (rect.x - camera.x,rect.y - camera.y))

def render2(img,rect,angle):
    mapSurface.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.w,rect.h)),angle), (rect.x - camera.x,rect.y - camera.y))

r = Dude(pygame.Rect(0,0, 64,64))
l = Level()
##l.addWall(pygame.Rect(10,10,64,64))
##l.addWall(pygame.Rect(100,100,64,64))
##l.addWall(pygame.Rect(200,200,100,64))
camera = pygame.Rect(0,0,display_width,display_height)
clock = pygame.time.Clock()

#gameDisplay.blit
pygame.draw.rect(gameDisplay, black, (300,300, 32, 32))
render(pygame.image.load("sprites/path_left_grass.png"),pygame.Rect(300,300,32,32),0)

for x in range(0, 1537, 128):
    for y in range(0, 1281, 32):
        render2(pygame.image.load("sprites/path_left_grass.png"),pygame.Rect(300 - x,300 - y,32,32),0)
        render2(pygame.image.load("sprites/path.png"),pygame.Rect(332 - x,300 - y,32,32),0)
        render2(pygame.image.load("sprites/path.png"),pygame.Rect(364 - x,300 - y,32,32),0)
        render2(pygame.image.load("sprites/path_right_grass.png"),pygame.Rect(396 - x,300 - y,32,32),0)




while not closed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

    gameDisplay.fill(white)
##    for y in range(0, 1281, 32):
##        
##        render(pygame.image.load("sprites/path_left_grass.png"),pygame.Rect(300,300 - y,32,32),0)
##        render(pygame.image.load("sprites/path.png"),pygame.Rect(332,300 - y,32,32),0)
##        render(pygame.image.load("sprites/path.png"),pygame.Rect(364,300 - y,32,32),0)
##        render(pygame.image.load("sprites/path_right_grass.png"),pygame.Rect(396,300 - y,32,32),0)

    render(mapSurface, pygame.Rect(0,0,1538,1280),0)
    
    r.update(l)
      
    camera.x = r.rect.x + r.rect.w/2 - camera.w/2
    camera.y = r.rect.y + r.rect.h/2 - camera.h/2
    
    l.update(camera)

        
    pygame.display.update()
    clock.tick(120)

pygame.quit()
quit()

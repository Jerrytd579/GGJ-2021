import pygame
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

class Level:
    walls = []
    def addWall(self,wall):
        self.walls.append(wall)
    def update(self):
        for i in self.walls:
            pygame.draw.rect(gameDisplay,black,i)

class Dude:
    def __init__(self, rect):
        self.rect = rect
        self.img = pygame.image.load('sprites/blastRocket.png')
    def update(self,level):
        keys = pygame.key.get_pressed();
        velocity = .25
        if (keys[pygame.K_LSHIFT]):
            velocity = .5
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
    gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.w,rect.h)),angle), (rect.x,rect.y))

r = Dude(pygame.Rect(display_width*.5,display_height - 64, 64,64))
l = Level()
l.addWall(pygame.Rect(10,10,64,64))
l.addWall(pygame.Rect(100,100,64,64))
l.addWall(pygame.Rect(200,200,100,64))
camera = pygame.Rect(0,0,display_width,display_height)
clock = pygame.time.Clock()
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    r.update(l)
    l.update()
    camera.x = r.rect.x + r.rect.w/2 - camera.w/2
    camera.y = r.rect.y + r.rect.h/2 - camera.h/2
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
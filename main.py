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

class Rect:
    def __init__(self,x,y,z,a):
        self.x = x
        self.y = y
        self.z = z;
        self.a = a
       

        

class Dude:
    def __init__(self, rect):
        self.rect = rect
        self.speed = pygame.Vector2(0,0)
        self.velocity = 1
        self.accel = pygame.Vector2(0,0)
        self.angle = 90
        self.img = pygame.image.load('sprites/blastRocket.png')
    def update(self):
        keys = pygame.key.get_pressed();
        velocity = 1
        if (keys[pygame.K_SPACE]):
            velocity = 10
        #velocity *= pygame.time.Clock.get_time()
        if (keys[pygame.K_RIGHT]):
            self.rect.x += velocity
        elif keys[pygame.K_LEFT]:
            self.rect.x -= velocity
        if keys[pygame.K_UP]:
            self.rect.y -= velocity
        elif keys[pygame.K_DOWN]:
            self.rect.y += velocity
        render(self.img,self.rect,self.angle)
def render(img,rect,angle):
    gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.z,rect.a)),angle), (rect.x,rect.y))

r = Dude(Rect(display_width*.5,display_height - 64, 64,64))
camera = Rect(0,0,display_width,display_height)
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    r.update()
    camera.x = r.rect.x + r.rect.z/2 - camera.z/2
    camera.y = r.rect.y + r.rect.a/2 - camera.a/2
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
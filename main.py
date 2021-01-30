import pygame
import math
import pygame.freetype

pygame.init()
pygame.freetype.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')

meleeSans =  pygame.freetype.Font("MeleeSans.ttf")
sign = pygame.image.load("sprites/sign.png")

black = (0,0,0)
white = (255,255,255) 

clock = pygame.time.Clock()
crashed = False      

class Level:
    reading = ""
    walls = []
    objects = [] #anything that can be interacted with
    def addWall(self,wall):
        self.walls.append(wall)
    def addObject(self,obj):
        self.objects.append(obj)
    def update(self,camera):
        for i in self.walls:
            pygame.draw.rect(gameDisplay,black,i.move(-1*camera.x,-1*camera.y))
            

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
        l.reading = self.message
    

class Dude:
    def __init__(self, rect):
        self.rect = rect
        self.img = pygame.image.load('sprites/blastRocket.png')
    def update(self,level,camera):
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
        render(self.img,self.rect,0,camera)
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
        for i in level.objects:
            if i.rect.colliderect(self.rect):
                i.interact()
                
def render(img,rect,angle,camera):
    gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(img,(rect.w,rect.h)),angle), (rect.x - camera.x,rect.y - camera.y))

r = Dude(pygame.Rect(display_width*.5,display_height - 64, 64,64))
l = Level()
l.addWall(pygame.Rect(10,10,64,64))
l.addWall(pygame.Rect(100,100,64,64))
l.addWall(pygame.Rect(200,200,100,64))
#l.addObject(Sign("Hello world",pygame.Rect(500,500,100,100),"sprites/signIcon.png"))
camera = pygame.Rect(0,0,display_width,display_height)
baseCamera = pygame.Rect(0,0,1,1) #used for rendering things without worrying about the camera following in the player
clock = pygame.time.Clock()
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    if (l.reading == ""):
        r.update(l,camera)

    else:
        surf,rect = meleeSans.render(l.reading,fgcolor = white,bgcolor = black,size = 100)  

        render(surf,pygame.Rect(10,10,rect.w,rect.h),0,baseCamera)
        #render(sign,pygame.Rect(10,10,display_width - 20, display_height - 20),0,baseCamera)
        if (pygame.key.get_pressed()[pygame.K_e]):
            l.reading = ""
      
    camera.x = r.rect.x + r.rect.w/2 - camera.w/2
    camera.y = r.rect.y + r.rect.h/2 - camera.h/2
    
    l.update(camera)

        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
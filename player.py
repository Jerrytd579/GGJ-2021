import pygame

class Dude:
    def __init__(self, rect):
        self.rect = rect
        self.front_imgs = (pygame.image.load('sprites/player_front1.png'), pygame.image.load('sprites/player_front2.png'), pygame.image.load('sprites/player_front1.png'), pygame.image.load('sprites/player_front3.png'))
        self.back_imgs = (pygame.image.load('sprites/player_back1.png'), pygame.image.load('sprites/player_back2.png'), pygame.image.load('sprites/player_back1.png'), pygame.image.load('sprites/player_back3.png'))
        self.side_imgs = (pygame.image.load('sprites/player_side1.png'), pygame.image.load('sprites/player_side2.png'))

        self.img = self.front_imgs[0]
        self.frame = 0
        self.frame_cooldown = 10


    def update(self, level, camera, clock, pressed):
        justPressed = pressed
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

        if(self.frame_cooldown == 0):
            if(speeds[0] > 0):
                self.img = pygame.transform.flip(self.side_imgs[self.frame], True, False)
            elif(speeds[0] < 0):
                self.img = self.side_imgs[self.frame]
            
            if(speeds[1] > 0):
                self.img = self.front_imgs[self.frame]
            if(speeds[1] < 0):
                self.img = self.back_imgs[self.frame]

            self.frame = (self.frame + 1) % len(self.side_imgs)
            self.frame_cooldown = 10
        else:
            self.frame_cooldown -= 1

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
            if i.rect.colliderect(self.rect) and justPressed == pygame.K_e:
                i.interact()
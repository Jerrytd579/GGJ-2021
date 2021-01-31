import pygame

class Dude:
    def __init__(self, rect):
        self.rect = rect
        self.img = pygame.image.load('sprites/blastRocket.png')

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
            if i.rect.colliderect(self.rect) and pressed == pygame.K_e:
                i.interact(self)
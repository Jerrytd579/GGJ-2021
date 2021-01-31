import pygame, sys

def menu_state(screen, font, clock):
    pygame.mixer_music.load('music/njit-title.wav')
    pygame.mixer_music.play()

    BLACK = (0, 0, 0)
    NOT_HELD = (23, 4, 30)
    WHITE = (255, 255, 255)
    HOVER_COLOR = (50, 70, 90)
    text1 = font.render("Play", fgcolor=(0xff, 0xff, 0xff), size=32)[0]
    text2 = font.render("Quit", fgcolor=(0xff, 0xff, 0xff), size=32)[0]
    text3 = font.render("Simple Things", fgcolor=(0xff, 0xff, 0xff), size=32)[0]
    rect3 = pygame.Rect(440, 100, 400, 100)
    rect1 = pygame.Rect(540,300,200,60)
    rect2 = pygame.Rect(540,400,200,60)
    buttons = [
        [text1, rect1, NOT_HELD],
        [text2, rect2, NOT_HELD],
    ]
    print(text1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button[1].collidepoint(event.pos):
                        # Set the button's color to the hover color.
                        button[2] = HOVER_COLOR
                    else:
                        # Otherwise reset the color to NOT_HELD.
                        button[2] = NOT_HELD
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if rect2.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
                elif rect1.collidepoint(pos):
                    pygame.mixer.music.stop()

                    fade = pygame.Surface((1280,720))
                    fade.fill((0,0,0))

                    for x in range(0, 255):
                        fade.set_alpha(x)
                        screen.blit(fade, pygame.Rect(0, 0, 1280, 720))
                        pygame.display.flip()
                        clock.tick(127.5)

                    return True

        screen.fill((255, 251, 219))
        for text, rect, color in buttons:
            pygame.draw.rect(screen, color, rect)
            screen.blit(text, [610, rect[1] + 16])
        pygame.draw.rect(screen, BLACK, rect3)
        screen.blit(text3, [rect3[0] + rect3[2] // 2 - 90, rect3[1] + 36])

        pygame.display.flip()
        clock.tick(15)

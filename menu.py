import pygame

def menu_state(screen, font, clock):
    BLACK = (0, 0, 0)
    NOT_HELD = (23, 4, 30)
    WHITE = (255, 255, 255)
    HOVER_COLOR = (50, 70, 90)
    text1 = font.render("Play", fgcolor=(0xff, 00, 00), size=32)[0]
    text2 = font.render("Quit", fgcolor=(0xff, 00, 00), size=32)[0]
    text3 = font.render("Insert Title Here", fgcolor=(0xff, 00, 00), size=32)[0]
    rect3 = pygame.Rect(500, 100, 400, 100)
    rect1 = pygame.Rect(600,300,205,60)
    rect2 = pygame.Rect(600,400,205,60)
    buttons = [
        [text1, rect1, NOT_HELD],
        [text2, rect2, NOT_HELD],
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
                elif rect1.collidepoint(pos):
                    return True

        screen.fill((255, 251, 219))
        for text, rect, color in buttons:
            pygame.draw.rect(screen, color, rect)
            screen.blit(text, rect)
        pygame.draw.rect(screen, BLACK, rect3)
        screen.blit(text3, rect3)

        pygame.display.flip()
        clock.tick(15)
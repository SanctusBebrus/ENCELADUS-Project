import pygame

from settings import WINDOW_SIZE, CAPTION
from field import Field

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(CAPTION)

field = Field()

while True:
    screen.fill((0, 0, 0))
    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()

    field.update(screen, events)

    pygame.display.update()

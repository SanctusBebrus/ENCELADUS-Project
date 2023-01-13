import pygame
from level import default_field, y_player, g_player, r_player, b_player

from settings import WINDOW_SIZE, CAPTION
from field import Field, Cell
from ui import start_screen, ButtonsController, pause

pygame.init()

if __name__ == '__main__':
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(CAPTION)

    start_screen(screen)

    field = Field([y_player, g_player, r_player, b_player], default_field)
    buttons_controller = ButtonsController(screen, field)

    while True:
        screen.fill((0, 0, 0))
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pause(screen)

        field.update(screen, events)
        buttons_controller.update(events)

        pygame.display.update()

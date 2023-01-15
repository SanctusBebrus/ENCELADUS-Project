import pygame
from level import default_field, y_player, g_player, r_player, b_player

from settings import WINDOW_SIZE, CAPTION
from field import Field, Cell
from itertools import cycle
from ui import start_screen, ButtonsController, pause
import sound

sound = sound.Sound()

pygame.init()

if __name__ == '__main__':
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(CAPTION)

    start_screen(screen)

    field = Field([y_player, g_player, r_player, b_player], default_field)
    buttons_controller = ButtonsController(screen, field)
    playlist = sound.stage_one_playlist
    wind = sound.wind.play(-1)
    wind.set_volume(0.8)
    pygame.mixer.music.load(playlist.pop())  # Get the first track from the playlist
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.queue(playlist.pop())  # Queue the 2nd song
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Se tup the end track event
    pygame.mixer.music.play()

    while True:
        screen.fill((0, 0, 0))
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pause(screen)

            elif e.type == pygame.USEREVENT:  # A track has ended
                if len(playlist) > 0:  # If there are more tracks in the queue...
                    pygame.mixer.music.queue(sound.stage_one_playlist.pop())

        field.update(screen, events)
        buttons_controller.update(events)

        pygame.display.update()

from typing import List

import pygame

from settings import WINDOW_SIZE, CAPTION


class Field:
    default_field = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    def __init__(self, field: list[list[int]] = default_field, rect_size: int = 50,
                 scroll_speed=3):
        self.field = field
        self.coords = (0, 0)
        self.rect_size = rect_size
        self.scroll_speed = scroll_speed
        self.can_get_rel = False

        self.max_rect_size = 100
        self.min_rect_size = 25

        self.surface = pygame.surface.Surface((len(field[0]) * self.max_rect_size,
                                              len(field) * self.max_rect_size))

    def update(self, surface, events) -> None:
        self.event_control(events)
        self.draw()

        surface.blit(field.surface, field.coords)

    def event_control(self, events) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoom(self.scroll_speed)
                elif event.button == 5:
                    self.zoom(-self.scroll_speed)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    print(self.get_coords(pygame.mouse.get_pos()))

            if e.type == pygame.MOUSEMOTION:
                rel = pygame.mouse.get_rel()
                if pygame.mouse.get_pressed()[2] and self.can_get_rel:
                    self.coords = (rel[0] + field.coords[0],
                                   rel[1] + field.coords[1])
                else:
                    self.can_get_rel = True

            if e.type == pygame.MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[2]:
                    self.can_get_rel = False

    def zoom(self, px: int) -> None:
        if self.min_rect_size < self.rect_size + px < self.max_rect_size:
            self.rect_size += px

    def draw(self) -> None:
        self.surface.fill((0, 0, 0))

        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                color = 'black'
                match self.field[y][x]:
                    case 0:
                        color = 'white'
                    case 1:
                        color = 'red'
                    case 2:
                        color = 'yellow'

                rect = pygame.Rect(x * self.rect_size, y * self.rect_size, self.rect_size, self.rect_size)
                pygame.draw.rect(self.surface, color, rect, width=1)

    def get_coords(self, coords: tuple[int, int]) -> tuple[int, int] or str:
        coords = ((coords[0] - self.coords[0]) // self.rect_size,
                  (coords[1] - self.coords[1]) // self.rect_size)

        if not (0 <= coords[1] < len(self.field) and 0 <= coords[0] < len(self.field[0])):
            return 'out of field'

        return coords


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

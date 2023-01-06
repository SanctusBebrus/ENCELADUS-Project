import pygame

import settings
import units

snow_image_path = 'sprites/cell/snow.png'
stone_image_path = 'sprites/cell/stone.png'
grass_image_path = 'sprites/cell/grass.png'

unit1 = units.Rover(1)
unit2 = units.Hunter(1)


class Cell:
    size = 50

    def __init__(self, image_path: str = snow_image_path, team: 'Team' = None, unit: units.Unit or None = None):
        self.image = pygame.image.load(image_path)

        self.alpha_surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)
        self.surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)

        self.team = team
        self.unit = unit
        self.defence_level = 0

    def draw(self, surface: pygame.surface.Surface, pos: tuple[int, int], alpha=70) -> None:
        self.alpha_surface = pygame.surface.Surface((settings.cell_size, settings.cell_size), pygame.SRCALPHA)
        self.surface = pygame.surface.Surface((settings.cell_size, settings.cell_size), pygame.SRCALPHA)
        self.alpha_surface.fill((255, 0, 0, alpha))

        self.surface.blit(pygame.transform.scale(self.image, (settings.cell_size - 2, settings.cell_size - 2)), (0, 0))
        self.surface.blit(self.alpha_surface, (0, 0))

        if self.unit:
            self.unit.draw_unit(self.surface, (0, 0))

        surface.blit(self.surface, pos)

    def set_image(self, image_path: str) -> None:
        self.image = pygame.image.load(image_path)

    def set_unit(self, unit: 'Unit') -> None:
        self.unit = unit

    def set_team(self, team: 'Team') -> None:
        self.team = team


class Field:
    default_field = list(map(lambda y: list(map(lambda x: Cell(), range(10))), range(10)))
    default_field[0][0].set_unit(unit1)
    default_field[7][5].set_unit(unit2)

    def __init__(self, field: list[list[Cell]] = default_field,
                 scroll_speed=4):
        self.current_cell = None

        self.field = field
        self.coords = self.x, self.y = (0, 0)
        self.scroll_speed = scroll_speed
        self.can_get_rel = False

        self.max_rect_size = 100
        self.min_rect_size = 25

        self.surface = pygame.surface.Surface((len(field[0]) * self.max_rect_size,
                                               len(field) * self.max_rect_size))

    def update(self, surface: pygame.surface.Surface, events) -> None:
        self.event_control(events)
        self.draw()

        surface.blit(self.surface, self.coords)

    def event_control(self, events) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoom(self.scroll_speed)
                elif event.button == 5:
                    self.zoom(-self.scroll_speed)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.on_click()

            if event.type == pygame.MOUSEMOTION:
                rel = pygame.mouse.get_rel()
                if pygame.mouse.get_pressed()[2] and self.can_get_rel:
                    self.coords = self.x, self.y = (rel[0] + self.coords[0],
                                                    rel[1] + self.coords[1])
                else:
                    self.can_get_rel = True

            if event.type == pygame.MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[2]:
                    self.can_get_rel = False

    def zoom(self, px: int) -> None:
        if self.min_rect_size < settings.cell_size + px < self.max_rect_size:
            settings.cell_size += px

            self.x -= len(self.field[0]) * px // 2
            self.y -= len(self.field) * px // 2

            self.coords = self.x, self.y

    def get_where_can_move(self):
        where_can_move = list()
        current_unit = self.get_cell(self.current_cell).unit
        for x in range(self.current_cell[0] - current_unit.distance,
                       self.current_cell[0] + current_unit.distance + 1):
            for y in range(self.current_cell[1] - current_unit.distance,
                           self.current_cell[1] + current_unit.distance + 1):
                if x < 0 or x >= len(self.field[0]) or y < 0 or x >= len(self.field):
                    continue
                if x == self.current_cell[0] or y == self.current_cell[1]:
                    where_can_move.append((x, y))

        return where_can_move

    def draw(self) -> None:
        self.surface.fill((0, 0, 0))

        where_can_move = list()
        if self.current_cell:
            where_can_move = self.get_where_can_move()

        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                rect = pygame.Rect(x * settings.cell_size, y * settings.cell_size, settings.cell_size,
                                   settings.cell_size)

                self.field[y][x].draw(self.surface, (rect.x, rect.y), alpha=30 if (x, y) in where_can_move else 70)

    def move_unit(self, pos, pos1):
        self.get_cell(pos1).unit = self.get_cell(pos).unit
        self.get_cell(pos).unit = None

    def get_cell(self, pos):
        return self.field[pos[1]][pos[0]]

    def on_click(self):
        mouse_pos = self.get_coords(pygame.mouse.get_pos())

        if self.current_cell and mouse_pos in self.get_where_can_move():
            self.move_unit(self.current_cell, mouse_pos)
            self.current_cell = None
            return

        if mouse_pos != -1 and self.get_cell(mouse_pos).unit is not None:
            self.current_cell = mouse_pos
        else:
            self.current_cell = None

        print(mouse_pos)

    def get_coords(self, coords: tuple[int, int]) -> tuple[int, int] or str:
        coords = ((coords[0] - self.x) // settings.cell_size,
                  (coords[1] - self.y) // settings.cell_size)

        if not (0 <= coords[1] < len(self.field) and 0 <= coords[0] < len(self.field[0])):
            return -1

        return coords

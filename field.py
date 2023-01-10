import sys

import pygame

import random
import settings
import units
import player

snow_image_path = 'sprites/cell/snow.png'
stone_image_path = 'sprites/cell/stone.png'
grass_image_path = 'sprites/cell/grass.png'

team_1 = player.Team((255, 0, 0))
team_2 = player.Team((0, 0, 255))

player_1 = player.Player(team_1)
player_2 = player.Player(team_2)

unit1 = units.Rover(team_1)
unit2 = units.Hunter(team_2)


class Cell:
    size = 50

    def __init__(self, team: player.Team = None, image_path: str = snow_image_path, unit: units.Unit or None = None):
        self.image = pygame.image.load(image_path)

        self.alpha_surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)
        self.surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)

        self.team = team
        self.unit = unit
        self.defence_level = 0

    def draw(self, surface: pygame.surface.Surface, pos: tuple[int, int], alpha=20) -> None:
        self.alpha_surface = pygame.surface.Surface((settings.cell_size, settings.cell_size), pygame.SRCALPHA)
        self.surface = pygame.surface.Surface((settings.cell_size, settings.cell_size), pygame.SRCALPHA)
        self.alpha_surface.fill((*self.team.color, alpha))

        self.surface.blit(pygame.transform.scale(self.image, (settings.cell_size - 2, settings.cell_size - 2)), (0, 0))
        self.surface.blit(self.alpha_surface, (0, 0))

        if self.unit:
            self.unit.draw_unit(self.surface, (0, 0))

        surface.blit(self.surface, pos)

    def set_image(self, image_path: str) -> None:
        self.image = pygame.image.load(image_path)

    def set_unit(self, unit: units.Unit or None) -> None:
        self.unit = unit

        if unit is not None:
            self.team = self.get_unit().get_team()

    def set_team(self, team: player.Team) -> None:
        self.team = team

    def get_unit(self) -> units.Unit:
        return self.unit

    def get_team(self) -> player.Team:
        return self.team


class Field:
    default_field = list(
        map(lambda y: list(map(lambda x: Cell(random.choice([team_1, team_2])), range(15))), range(25)))
    default_field[0][0].set_unit(unit1)
    default_field[7][5].set_unit(unit2)

    def __init__(self, field: list[list[Cell]] = default_field,
                 scroll_speed=4):
        self.current_cell_coords = None

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

        current_cell = self.get_cell(self.current_cell_coords)

        distance = (current_cell.get_unit().distance - 1) // 2

        x_range = list(range(self.current_cell_coords[0] - distance, self.current_cell_coords[0] + distance + 1))
        y_range = list(range(self.current_cell_coords[1] - distance, self.current_cell_coords[1] + distance + 1))

        def get_need_cells(x, y):
            for x1, y1 in ([x - 1, y], [x, y - 1], [x + 1, y], [x, y + 1]):
                if current_cell.get_team() is self.get_cell((x1, y1)).get_team():
                    if (x1, y1) not in where_can_move:
                        if not (x1 in x_range and y1 in y_range):
                            return

                        where_can_move.append((x1, y1))
                        get_need_cells(x1, y1)

        get_need_cells(self.current_cell_coords[0], self.current_cell_coords[1])

        return where_can_move

    def draw(self) -> None:
        self.surface.fill((0, 0, 0))

        where_can_move = list()
        if self.current_cell_coords:
            where_can_move = self.get_where_can_move()

        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                rect = pygame.Rect(x * settings.cell_size, y * settings.cell_size, settings.cell_size,
                                   settings.cell_size)

                self.field[y][x].draw(self.surface, (rect.x, rect.y), alpha=100 if (x, y) in where_can_move else 15)

    def move_unit(self, pos: tuple[int, int], pos1: tuple[int, int]):
        if pos != pos1:
            self.get_cell(pos1).set_unit(self.get_cell(pos).get_unit())

            self.get_cell(pos).set_unit(None)

    def get_cell(self, pos: tuple[int, int]) -> Cell or None:
        if self.is_pos_in_field(pos):
            cell = self.field[pos[1]][pos[0]]
            return cell
        return Cell()

    def is_pos_in_field(self, pos: tuple[int, int]) -> Cell or bool:
        if 0 <= pos[0] <= len(self.field[0]) - 1 \
                and 0 <= pos[1] <= len(self.field) - 1:
            return True
        return False

    def on_click(self) -> None:
        mouse_pos = self.get_coords(pygame.mouse.get_pos())

        if self.current_cell_coords and mouse_pos in self.get_where_can_move():
            self.move_unit(self.current_cell_coords, mouse_pos)
            self.current_cell_coords = None
            return

        if mouse_pos != -1 and self.get_cell(mouse_pos).unit is not None:
            self.current_cell_coords = mouse_pos
            print('Current cell coords are ', mouse_pos)
        else:
            self.current_cell_coords = None
            print('Current cell coords are None')

        print(mouse_pos)

    def get_coords(self, coords: tuple[int, int]) -> tuple[int, int] or str:
        coords = ((coords[0] - self.x) // settings.cell_size,
                  (coords[1] - self.y) // settings.cell_size)

        if not (0 <= coords[1] < len(self.field) and 0 <= coords[0] < len(self.field[0])):
            return -1

        return coords

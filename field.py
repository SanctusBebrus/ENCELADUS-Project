import pygame
import random
import settings
import sound
import units
import player
from itertools import product

snow_image_path = 'sprites/cell/snow.png'
ice_image_path = 'sprites/cell/ice_rock.png'
hole_image_path = 'sprites/cell/hole.png'

team_1 = player.Team((255, 0, 0))
LENGTH = WIDTH = random.randint(10, 16)

pygame.font.init()


class Cell:
    size = 50
    font = pygame.font.SysFont('Arial', settings.cell_size)

    def __init__(self, team: player.Team = None, image_path: str = snow_image_path, unit: units.Unit or None = None):
        self.image = pygame.image.load(image_path)

        self.alpha_surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)
        self.surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)

        self.team = team
        self.unit = unit
        self.profit = 1
        self.defence_level = 0

    def draw(self, surface: pygame.surface.Surface, pos: tuple[int, int], alpha=20) -> None:
        self.alpha_surface = pygame.surface.Surface((settings.cell_size, settings.cell_size), pygame.SRCALPHA)
        self.surface = pygame.surface.Surface((settings.cell_size, settings.cell_size), pygame.SRCALPHA)
        self.alpha_surface.fill((*self.team.color, alpha))

        self.surface.blit(pygame.transform.scale(self.image, (settings.cell_size - 2, settings.cell_size - 2)), (0, 0))
        self.surface.blit(self.alpha_surface, (0, 0))

        if self.unit:
            self.unit.draw_unit(self.surface, (0, 0))

        if self.defence_level not in [0, 500]:
            self.surface.blit(Cell.font.render(str(self.defence_level), True, True), (0, 0))

        surface.blit(self.surface, pos)

    def set_image(self, image_path: str) -> None:
        self.image = pygame.image.load(image_path)

    def set_unit(self, unit: units.Unit or None) -> None:
        self.unit = unit

        if unit is not None:
            self.team = self.get_unit().get_team()

    def set_team(self, team: player.Team) -> None:
        self.team = team

    def set_defence_level(self, level):
        self.defence_level = level

    def get_unit(self) -> units.Unit:
        return self.unit

    def get_team(self) -> player.Team:
        return self.team

    def get_defence_level(self):
        return self.defence_level


class IceCell(Cell):
    size = 50

    def __init__(self, team: player.Team = None, image_path: str = ice_image_path, unit: units.Unit or None = None):
        super().__init__(team, image_path, unit)
        self.image = pygame.image.load(image_path)

        self.alpha_surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)
        self.surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)

        self.team = team
        self.unit = unit
        self.profit = 0
        self.defence_level = 500


class HoleCell(Cell):
    size = 50

    def __init__(self, team: player.Team = None, image_path: str = hole_image_path, unit: units.Unit or None = None):
        super().__init__(team, image_path, unit)
        self.image = pygame.image.load(image_path)

        self.alpha_surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)
        self.surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)

        self.team = team
        self.unit = unit
        self.profit = 0
        self.defence_level = 500


class Field:
    default_field = list(
        map(lambda y: list(map(lambda x: Cell(random.choice([team_1])), range(LENGTH))), range(WIDTH)))

    for row, col in product(range(LENGTH + 3, LENGTH - 3), range(LENGTH + 3, LENGTH - 3)):
        default_field[row][col] = IceCell(team_1)

    def __init__(self, player_list: list[player.Player], field: list[list[Cell]] = default_field,
                 scroll_speed=4):
        self.current_cell_coords = None
        self.field = field
        self.coords = self.x, self.y = (0, 0)
        self.scroll_speed = scroll_speed
        self.can_get_rel = False
        self.player_list = player_list
        self.current_player = 0
        self.live_units = []

        self.max_rect_size = 100
        self.min_rect_size = 45

        self.surface = pygame.surface.Surface((len(field[0]) * self.max_rect_size,
                                               len(field) * self.max_rect_size))

    def update(self, surface: pygame.surface.Surface, events) -> None:
        self.event_control(events)

        Cell.font = pygame.font.SysFont('Arial', int(0.15 * settings.cell_size))
        self.calculate_defence()

        self.draw()

        surface.blit(self.surface, self.coords)

    def calculate_defence(self):
        for row in self.field:
            for cell in row:
                if not any(map(lambda x: True if isinstance(cell, x) else False, [IceCell, HoleCell])):
                    cell.set_defence_level(0)

        for y, x in product(range(len(self.field)), range(len(self.field[0]))):
            if not self.get_cell((x, y)).get_unit():
                continue

            for x1, y1 in product(range(-1, 2), repeat=2):
                if self.is_pos_in_field((x + x1, y + y1)):

                    if self.get_cell((x + x1, y + y1)).get_team() is not self.get_cell((x, y)).get_team():
                        continue

                    if self.get_cell((x, y)).unit.default_defence > self.get_cell(
                            (x + x1, y + y1)).get_defence_level():
                        self.get_cell((x + x1, y + y1)).set_defence_level(
                            self.get_cell((x, y)).unit.default_defence)

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.make_new_turn()
                    self.check_units()
                    self.check_base_status()
                    self.count_money()
                    self.check_players()
                    self.check_encircled()
                    self.current_player += 1
                    self.current_player %= len(self.player_list)
                    self.find_base()

    def find_base(self):
        x_min = 100
        x_max = 0
        y_min = 100
        y_max = 0

        for y, x in product(range(len(self.field)), range(len(self.field[0]))):
            if self.get_cell((x, y)).get_team() is self.player_list[self.current_player].get_team():
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y)
                y_max = max(y_max, y)

        self.coords = self.x, self.y = settings.WINDOW_WIDTH // 2 - (
                x_min + x_max) // 2 * settings.cell_size, settings.WINDOW_HEIGHT // 2 - (
                                               y_min + y_max) // 2 * settings.cell_size

    def find_mines(self):
        mines = 0
        for row in self.field:
            for col in row:
                if isinstance(col.get_unit(), units.Mine) and col.get_unit().get_team() == \
                        self.player_list[self.current_player].get_team():
                    mines += 1
        return mines

    def buy_unit(self, unit, unit_cost):
        if self.player_list[self.current_player].base_is_alive:
            try:
                mouse_pos = self.get_coords(pygame.mouse.get_pos())
                if self.get_cell(mouse_pos).get_team() != self.player_list[self.current_player].get_team() \
                        and self.get_cell(mouse_pos).get_unit():
                    return
                if not self.get_cell(mouse_pos).get_unit() and self.get_cell(mouse_pos).get_team() == \
                        self.player_list[self.current_player].get_team() \
                        and self.player_list[self.current_player].money >= unit_cost:
                    self.get_cell(mouse_pos).set_unit(
                        unit(
                            self.player_list[self.current_player].get_team()
                        )
                    )
                    sound.Sound().building.play()
                    self.player_list[self.current_player].money -= unit_cost
            except Exception:
                pass

    def check_players(self):
        if not self.player_list[self.current_player].base_is_alive and self.player_list[self.current_player].money < 0:
            self.player_list.remove(self.player_list[self.current_player])

    def check_units(self):
        self.live_units = []
        for row in self.field:
            for col in row:
                if col.get_unit() and col.get_unit().get_team() == self.player_list[self.current_player].get_team() \
                        and not col.get_unit().is_building:
                    self.live_units.append(col.get_unit())

    def check_base_status(self):
        for row in self.field:
            for col in row:
                if not (col.get_unit()
                        and col.get_unit().get_team() == self.player_list[self.current_player].get_team()
                        and col.get_unit().is_building and col.get_unit().is_base):
                    continue
                else:
                    self.player_list[self.current_player].base_is_alive = True
                    return
        self.player_list[self.current_player].base_is_alive = False
        return

    def kill_all(self):
        for row in self.field:
            for col in row:
                if (col.get_unit()
                        and col.get_unit().get_team() == self.player_list[self.current_player].get_team()
                        and not col.get_unit().is_building
                        and self.player_list[self.current_player].money < 0):
                    col.set_unit(None)
                    self.live_units = []

    def count_money(self):
        total_profit = 0
        if self.live_units:
            for unit in self.live_units:
                total_profit -= unit.maintenance

        for row in self.field:
            for col in row:
                if not col.get_unit() and col.get_team() == self.player_list[self.current_player].get_team() \
                        and self.player_list[self.current_player].base_is_alive:
                    total_profit += col.profit
                elif col.get_unit() and col.get_team() == self.player_list[self.current_player].get_team() \
                        and self.player_list[self.current_player].base_is_alive:
                    total_profit += col.get_unit().profit
        self.player_list[self.current_player].money += total_profit
        self.player_list[self.current_player].player_profit = total_profit
        self.kill_all()

    def make_new_turn(self):
        for row in self.field:
            for col in row:
                if col.get_unit() and col.get_unit().already_moved and not col.get_unit().is_building:
                    col.get_unit().already_moved = False

    def zoom(self, px: int) -> None:
        if self.min_rect_size < settings.cell_size + px < self.max_rect_size:
            settings.cell_size += px

            pos = self.get_coords(pygame.mouse.get_pos())

            if px < 0 or pos == -1:
                pos = self.get_coords((settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2))
            try:
                self.x -= pos[0] * px
                self.y -= pos[1] * px

                self.coords = self.x, self.y
            except TypeError:
                pass

    def check_encircled(self):
        for row in self.field:
            for col in row:
                neighbours = 0
                pos = self.field.index(row), row.index(col)
                try:
                    for x, y in product(range(-1, 2), range(-1, 2)):
                        if pos == (pos[0] + x, pos[1] + y) or \
                                not self.is_pos_in_field((pos[0] + x, pos[1] + y)):
                            continue
                        if self.field[pos[0]][pos[1]].get_team() == \
                                self.field[pos[0] + x][pos[1] + y].get_team() and \
                                self.is_pos_in_field((pos[0] + x, pos[1] + y)):
                            neighbours += 1
                        else:
                            continue
                except Exception:
                    continue
                if neighbours == 0:
                    self.field[pos[0]][pos[1]].set_unit(None)

    def get_where_can_move(self):
        where_can_move = list()

        current_cell = self.get_cell(self.current_cell_coords)

        distance = (current_cell.get_unit().distance - 1)

        x_range = list(range(self.current_cell_coords[0] - distance, self.current_cell_coords[0] + distance + 1))
        y_range = list(range(self.current_cell_coords[1] - distance, self.current_cell_coords[1] + distance + 1))

        def get_need_cells(x, y):
            for x1, y1 in ([x - 1, y], [x, y - 1], [x + 1, y], [x, y + 1]):
                if current_cell.get_team() is self.get_cell((x1, y1)).get_team():
                    if (x1, y1) not in where_can_move and x1 in x_range and y1 in y_range:
                        where_can_move.append((x1, y1))
                        get_need_cells(x1, y1)
                elif x1 in x_range and y1 in y_range:
                    where_can_move.append((x1, y1))

        get_need_cells(self.current_cell_coords[0], self.current_cell_coords[1])
        return where_can_move

    def draw(self) -> None:
        self.surface.fill((0, 0, 0))

        where_can_move = list()
        if self.current_cell_coords:
            where_can_move = self.get_where_can_move()

        for y, x in product(range(len(self.field)), range(len(self.field[0]))):
            rect = pygame.Rect(x * settings.cell_size, y * settings.cell_size, settings.cell_size,
                               settings.cell_size)
            if (x, y) in where_can_move or self.get_cell(
                    (x, y)).unit and self.get_cell(
                (x, y)).get_team() is self.player_list[self.current_player].get_team() and \
                    not self.get_cell((x, y)).unit.already_moved:
                alpha = 100
            else:
                alpha = 30

            self.field[y][x].draw(self.surface, (rect.x, rect.y), alpha=alpha)

    def move_unit(self, pos: tuple[int, int], pos1: tuple[int, int]):
        start_cell = self.get_cell(pos)
        end_cell = self.get_cell(pos1)

        if start_cell.get_team() is end_cell.get_team():
            if end_cell.get_unit():
                return
        else:
            if start_cell.get_defence_level() <= end_cell.get_defence_level():
                if start_cell.get_unit().default_defence != 4:
                    return

        if end_cell.defence_level > 5:
            return

        if start_cell.get_unit().already_moved:
            return

        start_cell.get_unit().get_sound()
        start_cell.get_unit().sound_effect.set_volume(0.3)
        start_cell.get_unit().sound_effect.play()
        start_cell.get_unit().sound.set_volume(0.4)
        start_cell.get_unit().sound.play()
        end_cell.set_unit(self.get_cell(pos).get_unit())
        end_cell.get_unit().already_moved = True
        start_cell.set_unit(None)

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
            print(self.move_unit(self.current_cell_coords, mouse_pos))
            self.current_cell_coords = None
            return

        if mouse_pos != -1 and self.get_cell(mouse_pos).unit is not None:
            if self.player_list[self.current_player].get_team() is self.get_cell(mouse_pos).get_team():
                self.current_cell_coords = mouse_pos
        else:
            self.current_cell_coords = None

    def get_coords(self, coords: tuple[int, int]) -> tuple[int, int] or str:
        coords = ((coords[0] - self.x) // settings.cell_size,
                  (coords[1] - self.y) // settings.cell_size)

        if not (0 <= coords[1] < len(self.field) and 0 <= coords[0] < len(self.field[0])):
            return -1

        return coords

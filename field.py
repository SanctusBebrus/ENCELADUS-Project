import pygame

snow_image_path = 'sprites/cell/snow.png'
stone_image_path = 'sprites/cell/stone.png'
grass_image_path = 'sprites/cell/grass.png'


class Cell:
    size = 50
    alpha_color = 70

    def __init__(self, image_path: str = snow_image_path, team: 'Team' = None):
        self.image = pygame.image.load(image_path)

        self.team = team
        self.defence_level = 0

        self.unit = None

    def draw(self, surface: pygame.surface.Surface, pos: tuple[int, int]) -> None:
        surface.blit(pygame.transform.scale(self.image, (Cell.size - 2, Cell.size - 2)), pos)

    def update(self, surface: pygame.surface.Surface, pos: tuple[int, int]) -> None:
        self.draw(surface, pos)

    def set_image(self, image_path: str) -> None:
        self.image = pygame.image.load(image_path)

    def set_unit(self, unit: 'Unit') -> None:
        self.unit = unit

    def set_team(self, team: 'Team') -> None:
        self.team = team


class Field:
    default_field = list(map(lambda y: list(map(lambda x: Cell(), range(10))), range(10)))

    def __init__(self, field: list[list[Cell]] = default_field,
                 scroll_speed=3):
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
                    print(self.get_coords(pygame.mouse.get_pos()))

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
        if self.min_rect_size < Cell.size + px < self.max_rect_size:
            Cell.size += px

    def draw(self) -> None:
        self.surface.fill((0, 0, 0))

        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                surface = pygame.surface.Surface((Cell.size, Cell.size), pygame.SRCALPHA)
                surface.fill((255, 0, 0, Cell.alpha_color) if x > 5 and y > 5 else (0, 0, 255, Cell.alpha_color))

                rect = pygame.Rect(x * Cell.size, y * Cell.size, Cell.size, Cell.size)

                self.field[y][x].draw(self.surface, (rect.x, rect.y))
                self.surface.blit(surface, (rect.x, rect.y))

    def get_coords(self, coords: tuple[int, int]) -> tuple[int, int] or str:
        coords = ((coords[0] - self.x) // Cell.size,
                  (coords[1] - self.y) // Cell.size)

        if not (0 <= coords[1] < len(self.field) and 0 <= coords[0] < len(self.field[0])):
            return 'out of field'

        return coords

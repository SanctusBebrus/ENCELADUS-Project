import pygame


class Unit:
    def __init__(self, team):
        self.image = None
        self.team = team
        self.cost = 0
        self.maintenance = 0
        self.default_defence = 0
        self.defence = 0
        self.distance = 0
        self.is_dead = True
        self.diagonal_distance = self.distance - 2

    def get_team(self):
        return self.team

    def get_status(self):
        return self.is_dead

    def get_cost(self) -> int:
        return self.cost

    def get_defence(self) -> int:
        return self.defence

    def get_distance(self) -> int:
        return self.distance

    def get_maintenance(self) -> int:
        return self.maintenance

    def set_image(self, image_path: str):
        self.image = pygame.image.load(image_path)

    def set_defence(self, value: int):
        self.defence = value

    def resize(self):
        return pygame.transform.scale(self.image, (Cell.size, Cell.size))

    def draw_unit(self, surface: pygame.surface.Surface, pos: tuple[int, int]):
        self.resize()
        surface.blit(self.resize(), pos)


class Mine(Unit):
    def __init__(self, team):
        super(Mine, self).__init__(team)
        self.image = pygame.image.load('images/mine_sprite.png')
        self.cost = 60
        self.maintenance = 0
        self.default_defence = 0
        self.distance = 0
        self.life_period = 0
        self.profit = 25
        self.is_dead = False

    def set_money(self):
        return self.profit

    def resize(self):
        return pygame.transform.scale(self.image, (Cell.size + 186, Cell.size + 120))


class Base(Unit):
    def __init__(self, team):
        super(Base, self).__init__(team)
        self.image = pygame.image.load('images/base_sprt.png')
        self.default_defence = 2
        self.is_dead = False

    def resize(self):
        return pygame.transform.scale(self.image, (Cell.size + 50, Cell.size + 20))


class Tower(Unit):
    def __init__(self, team):
        super(Tower, self).__init__(team)
        self.image = pygame.image.load('images/tower_sprt.png')
        self.cost = 25
        self.maintenance = 10
        self.default_defence = 2
        self.is_dead = False

    def resize(self):
        return pygame.transform.scale(self.image, (Cell.size - 10, Cell.size - 10))


class Rover(Unit):
    def __init__(self, team):
        super(Rover, self).__init__(team)
        self.image = pygame.image.load('images/rover_sprt.png')
        self.cost = 15
        self.maintenance = 5
        self.default_defence = 1
        self.is_dead = False
        self.distance = 5

    def resize(self):
        return pygame.transform.scale(self.image, (Cell.size - 22, Cell.size - 22))


class Rhino(Unit):
    def __init__(self, team):
        super(Rhino, self).__init__(team)
        self.image = pygame.image.load('images/rhino_sprite.png')
        self.cost = 25
        self.maintenance = 10
        self.default_defence = 2
        self.is_dead = False
        self.distance = 4

    def resize(self):
        return pygame.transform.scale(self.image, (Cell.size - 20, Cell.size - 30))


class Hunter(Unit):
    def __init__(self, team):
        super(Hunter, self).__init__(team)
        self.image = pygame.image.load('images/hunter.png')
        self.cost = 35
        self.maintenance = 15
        self.default_defence = 3
        self.is_dead = False
        self.distance = 6

    def resize(self):
        return pygame.transform.scale(self.image, (Cell.size - 10, Cell.size - 10))


class Devastator(Unit):
    def __init__(self, team):
        super(Devastator, self).__init__(team)
        self.image = pygame.image.load('images/devastator.png')
        self.cost = 45
        self.maintenance = 20
        self.default_defence = 4
        self.is_dead = False
        self.distance = 4

    def resize(self):
        return pygame.transform.scale(self.image, (Cell.size + 20, Cell.size + 10))

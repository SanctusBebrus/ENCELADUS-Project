import pygame
import settings
import random

from sound import *

path = 'sprites/units/'
sound = Sound()


class Unit:
    def __init__(self, team):
        self.sound = sound.default
        self.sound_effect = sound.default
        self.image = None
        self.profit = 0
        self.team = team
        self.is_building = True
        self.is_base = False
        self.cost = 0
        self.maintenance = 0
        self.default_defence = 0
        self.defence = 0
        self.distance = 0
        self.is_dead = True
        self.diagonal_distance = self.distance - 2
        self.already_moved = True

    def get_sound(self):
        pass

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
        return pygame.transform.scale(self.image, (settings.cell_size, settings.cell_size))

    def draw_unit(self, surface: pygame.surface.Surface, pos: tuple[int, int]):
        image = self.resize()
        surface.blit(image, (
            pos[0] + (settings.cell_size - image.get_width()) // 2,
            pos[1] + (settings.cell_size - image.get_height()) // 2
        ))


class Mine(Unit):
    def __init__(self, team):
        super(Mine, self).__init__(team)
        self.image = pygame.image.load(path + 'mine_sprite.png')
        self.cost = 60
        self.is_building = True
        self.maintenance = 0
        self.default_defence = 0
        self.distance = 0
        self.life_period = 0
        self.profit = 15
        self.is_dead = False

    def get_money(self):
        return self.profit

    def resize(self):
        return pygame.transform.scale(self.image, (settings.cell_size + settings.cell_size * 0.75,
                                                   settings.cell_size + settings.cell_size * 0.4))


class Base(Unit):
    def __init__(self, team):
        super(Base, self).__init__(team)
        self.image = pygame.image.load(path + 'base_sprt.png')
        self.default_defence = 2
        self.profit = 8
        self.is_base = True
        self.is_building = True
        self.is_dead = False

    def resize(self):
        return pygame.transform.scale(self.image, (settings.cell_size + 10, settings.cell_size))


class Tower(Unit):
    def __init__(self, team):
        super(Tower, self).__init__(team)
        self.image = pygame.image.load(path + 'tower_sprt.png')
        self.cost = 35
        self.is_building = True
        self.maintenance = 20
        self.default_defence = 2
        self.is_dead = False

    def resize(self):
        return pygame.transform.scale(self.image, (settings.cell_size - 10, settings.cell_size - 10))


class Rover(Unit):
    def __init__(self, team):
        super(Rover, self).__init__(team)
        self.sound_list = [sound.rover_1, sound.rover_2,
                           sound.rover_3, sound.rover_4,
                           sound.rover_5]
        self.sound = random.choice(self.sound_list)
        self.sound_effect = sound.rover_
        self.sound_effect.set_volume(0.2)
        self.image = pygame.image.load(path + 'rover_sprt.png')
        self.cost = 15
        self.is_building = False
        self.maintenance = 10
        self.default_defence = 1
        self.is_dead = False
        self.distance = 4
        self.already_moved = False

    def get_sound(self):
        self.sound = random.choice(self.sound_list)

    def resize(self):
        return pygame.transform.scale(self.image, (settings.cell_size - 22, settings.cell_size - 22))


class Rhino(Unit):
    def __init__(self, team):
        super(Rhino, self).__init__(team)
        self.sound_list = [sound.rhino_1, sound.rhino_2,
                           sound.rhino_3, sound.rhino_4,
                           sound.rhino_5]
        self.sound_effect = sound.rhino_
        self.sound_effect.set_volume(0.2)
        self.image = pygame.image.load(path + 'rhino_sprite.png')
        self.cost = 25
        self.is_building = False
        self.maintenance = 20
        self.default_defence = 2
        self.is_dead = False
        self.distance = 3
        self.already_moved = False

    def get_sound(self):
        self.sound = random.choice(self.sound_list)

    def resize(self):
        return pygame.transform.scale(self.image, (settings.cell_size - 20, settings.cell_size - 30))


class Hunter(Unit):
    def __init__(self, team):
        super(Hunter, self).__init__(team)
        self.sound_list = [sound.hunter_1, sound.hunter_2,
                           sound.hunter_3, sound.hunter_4,
                           sound.hunter_5]
        self.sound_effect = sound.hunter_
        self.sound_effect.set_volume(0.2)
        self.image = pygame.image.load(path + 'hunter.png')
        self.cost = 35
        self.is_building = False
        self.maintenance = 25
        self.default_defence = 3
        self.is_dead = False
        self.distance = 4
        self.already_moved = False

    def get_sound(self):
        self.sound = random.choice(self.sound_list)

    def resize(self):
        return pygame.transform.scale(self.image, (settings.cell_size - 10, settings.cell_size - 10))


class Devastator(Unit):
    def __init__(self, team):
        super(Devastator, self).__init__(team)
        self.sound_list = [sound.devast_1, sound.devast_2,
                           sound.devast_3, sound.devast_4,
                           sound.devast_5]
        self.sound_effect = sound.devast_
        self.sound_effect.set_volume(0.2)
        self.image = pygame.image.load(path + 'devastator.png')
        self.cost = 45
        self.is_building = False
        self.maintenance = 35
        self.default_defence = 4
        self.is_dead = False
        self.distance = 3
        self.already_moved = False

    def get_sound(self):
        self.sound = random.choice(self.sound_list)

    def resize(self):
        return pygame.transform.scale(self.image, (settings.cell_size + 20, settings.cell_size + 10))

import sys

import pygame
from settings import WINDOW_SIZE
from sound import path

WIDTH, HEIGHT = WINDOW_SIZE


def load_image(name):
    fullname = name
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    main_theme = pygame.mixer.music.load(path + 'main_theme.mp3')
    pygame.mixer.music.play(-1)
    intro_text = ["НАЖМИТЕ   ENTER   ЧТОБЫ   НАЧАТЬ"]

    fon = pygame.transform.scale(load_image('sprites/backgrounds/ENCELADUS.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 20)
    text_coord = HEIGHT // 2 + HEIGHT // 4
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WIDTH // 2 - 90
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()
                return  # начинаем игру
        pygame.display.flip()


def pause(screen):
    main_theme = pygame.mixer.music.load(path + 'main_theme.mp3')
    pygame.mixer.music.play(-1)
    intro_text = ["НАЖМИТЕ   ESC   ЧТОБЫ   ПРОДОЛЖИТЬ"]
    fon = pygame.transform.scale(load_image('sprites/backgrounds/ENCELADUS.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 20)
    text_coord = HEIGHT // 2 + HEIGHT // 4
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WIDTH // 2 - 90
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return
        pygame.display.update()


class Button:
    def __init__(self, screen, text: str, pos: tuple, width: int, height: int, font=20):
        self.text = text
        self.pos = pos
        self.screen = screen
        self.width, self.height = width, height
        self.font = pygame.font.Font(None, font)
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (width, height))

    def draw(self):
        pygame.draw.rect(self.screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(self.screen, 'dark gray', [self.pos[0], self.pos[1], self.width, self.height], 5, 5)
        text2 = self.font.render(self.text, True, 'black')
        self.screen.blit(text2, (self.pos[0] + 7, self.pos[1] + 7))

    def check_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.collidepoint(pygame.mouse.get_pos()):
                    return True
                else:
                    return False


class ButtonWithCost(Button):
    def __init__(self, screen, text: str, pos: tuple, width: int, height: int, font=20):
        super(ButtonWithCost, self).__init__(screen, text, pos, width, height)

    def draw(self, cost=None):
        pygame.draw.rect(self.screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(self.screen, 'dark gray', [self.pos[0], self.pos[1], self.width, self.height], 5, 5)
        text2 = self.font.render(self.text, True, 'black')
        self.screen.blit(text2, (self.pos[0] + 7, self.pos[1] + 7))
        if cost:
            self.screen.blit(pygame.font.Font(None, 20).render(f'cost: {cost}', True, 'black'),
                             (self.pos[0] + 7, self.pos[1] + 20))


class InfoLabel(Button):
    def __init__(self, screen, text: str, pos: tuple, width: int, height: int, font=20):
        super(InfoLabel, self).__init__(screen, text, pos, width, height)

    def draw(self, parameter=None):
        pygame.draw.rect(self.screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(self.screen, 'dark gray', [self.pos[0], self.pos[1], self.width, self.height], 5, 5)
        text2 = self.font.render(self.text, True, 'black')
        self.screen.blit(text2, (self.pos[0] + 7, self.pos[1] + 7))
        if parameter != None:
            self.screen.blit(pygame.font.Font(None, 20).render(f'{parameter}', True, 'black'),
                             (self.pos[0] + 7, self.pos[1] + 20))


# тут магазин юнитов
class UnitsShop(Button):
    def __init__(self, screen, text: str, pos: tuple, width: int, height: int, font=20):
        super(UnitsShop, self).__init__(screen, text, pos, width, height)

    def open_shop(self, events):
        btn_rover = ButtonWithCost(self.screen, 'Rover', (self.pos[0] + self.width, self.pos[1]), self.width,
                                   self.height)
        btn_rhino = ButtonWithCost(self.screen, 'Rhino', (self.pos[0] + self.width * 2, self.pos[1]), self.width,
                                   self.height)
        btn_hunter = ButtonWithCost(self.screen, 'Hunter', (self.pos[0] + self.width * 3, self.pos[1]), self.width,
                                    self.height)
        btn_devastator = ButtonWithCost(self.screen, 'Devastator', (self.pos[0] + self.width * 4, self.pos[1]),
                                        self.width, self.height, font=17)

        btn_rover.draw(cost=100)
        btn_rhino.draw(cost=100)
        btn_hunter.draw(cost=100)
        btn_devastator.draw(cost=100)

        # место для функции покупки юнита Rover
        if btn_rover.check_clicked(events):
            pass

        # место для функции покупки юнита Rhino
        if btn_rhino.check_clicked(events):
            pass

        # место для функции покупки юнита Hunter
        if btn_hunter.check_clicked(events):
            pass

        # место для функции покупки юнита Devastator
        if btn_devastator.check_clicked(events):
            pass


# тут магазин зданий
class TowersShop(Button):
    def __init__(self, screen, text: str, pos: tuple, width: int, height: int, font=20):
        super(TowersShop, self).__init__(screen, text, pos, width, height)

    def open_shop(self, events):
        btn_tower = ButtonWithCost(self.screen, 'Tower', (self.pos[0] + self.width, self.pos[1]), self.width,
                                   self.height)
        btn_mine = ButtonWithCost(self.screen, 'Mine', (self.pos[0] + self.width * 2, self.pos[1]), self.width,
                                  self.height)

        # место для функции покупки здания Tower
        if btn_tower.check_clicked(events):
            pass

        # место для функции покупки здания Mine
        if btn_mine.check_clicked(events):
            pass

        btn_tower.draw(cost=100)
        btn_mine.draw(cost=100)


# Контроллер кнопок
class ButtonsController:
    def __init__(self, screen, field):
        self.field = field
        self.screen = screen

        self.units_shop_opened = False
        self.building_shop_opened = False

        self.btn_units = UnitsShop(self.screen, 'Units', (0, int(HEIGHT * 0.75)), WIDTH // 10, WIDTH // 10)
        self.btn_buildings = TowersShop(self.screen, 'Buildings', (0, int(HEIGHT * 0.88)), WIDTH // 10,
                                        WIDTH // 10, font=10)

        self.resources_info = InfoLabel(self.screen, 'Money', (0, 0), WIDTH // 9, WIDTH // 14)
        self.current_player_info = InfoLabel(self.screen, 'Player', (WIDTH // 9, 0), WIDTH // 9, WIDTH // 14)

        self.next_turn_btn = Button(self.screen, 'Next turn', (WIDTH // 9 + WIDTH // 9, 0), WIDTH // 9, WIDTH // 14)
        self.pause_btn = Button(self.screen, 'Pause', (WIDTH // 9 + WIDTH // 9 * 2, 0), WIDTH // 9, WIDTH // 14)

    def update(self, events):
        self.btn_units.draw()
        self.btn_buildings.draw()

        self.resources_info.draw(parameter=self.field.player_list[self.field.current_player].money)
        self.current_player_info.draw(parameter=self.field.current_player + 1)

        self.next_turn_btn.draw()
        self.pause_btn.draw()

        if self.btn_units.check_clicked(events):
            if not self.units_shop_opened:
                self.units_shop_opened = True
            else:
                self.units_shop_opened = False

        elif self.btn_buildings.check_clicked(events):
            if not self.building_shop_opened:
                self.building_shop_opened = True
            else:
                self.building_shop_opened = False

        if self.next_turn_btn.check_clicked(events):
            self.field.current_player += 1
            self.field.current_player %= len(self.field.player_list)

        if self.pause_btn.check_clicked(events):
            pause(self.screen)

        if self.units_shop_opened:
            self.btn_units.open_shop(events)

        if self.building_shop_opened:
            self.btn_buildings.open_shop(events)

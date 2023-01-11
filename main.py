import pygame
import player
import units

from settings import WINDOW_SIZE, CAPTION
from field import Field, Cell

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(CAPTION)

team_1 = player.Team((25, 245, 37))
team_2 = player.Team((235, 25, 75))

cell_field = list(
    map(lambda y: list(map(lambda x: Cell(), range(20))), range(20)))

for y in range(len(cell_field)):
    for x in range(len(cell_field[0])):
        if y > 10:
            cell_field[y][x].set_team(team_1)
        else:
            cell_field[y][x].set_team(team_2)

field = Field(cell_field)
cell_field[15][15].set_unit(units.Rover(team_1))

while True:
    screen.fill((0, 0, 0))
    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()

    field.update(screen, events)

    pygame.display.update()

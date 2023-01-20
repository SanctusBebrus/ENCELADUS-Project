from field import Cell, IceCell, HoleCell, LENGTH, WIDTH
import units
import player
from itertools import product
import random

# Teams
default_team = player.Team((255, 255, 255))

YELLOW = player.Team((255, 215, 0))
GREEN = player.Team((0, 128, 0))
RED = player.Team((255, 0, 0))
BLUE = player.Team((0, 0, 255))

default_field = list(
    map(lambda y: list(map(lambda x: Cell(default_team), range(LENGTH))), range(WIDTH)))

for i in range(random.randint(6, 9)):
    x1 = random.randint(2, LENGTH - 3)
    y1 = random.randint(0, LENGTH - 3)
    default_field[x1][y1] = IceCell(default_team)

for i in range(random.randint(4, 7)):
    x1 = random.randint(2, LENGTH - 3)
    y1 = random.randint(0, LENGTH - 3)
    default_field[x1][y1] = HoleCell(default_team)

# Players
y_player = player.Player(YELLOW)
g_player = player.Player(GREEN)
r_player = player.Player(RED)
b_player = player.Player(BLUE)

# Units
rover = units.Rover
hunter = units.Hunter
rhino = units.Rhino
devast = units.Devastator

# Buildings
tower = units.Tower
base = units.Base
mine = units.Mine

# YELLOW Team
for i, j in product(range(2), range(LENGTH - 2, LENGTH)):
    default_field[i][j].set_team(YELLOW)

default_field[0][LENGTH - 1].set_unit(base(YELLOW))
default_field[1][LENGTH - 2].set_unit(rover(YELLOW))

# GREEN Team
for i, j in product(range(2), range(2)):
    default_field[i][j].set_team(GREEN)

default_field[0][0].set_unit(base(GREEN))
default_field[1][1].set_unit(rover(GREEN))

# BLUE Team
for i, j in product(range(LENGTH - 2, LENGTH), range(LENGTH - 2, LENGTH)):
    default_field[i][j].set_team(BLUE)

default_field[LENGTH - 1][LENGTH - 1].set_unit(base(BLUE))
default_field[LENGTH - 2][LENGTH - 2].set_unit(rover(BLUE))

# RED Team
for i, j in product(range(LENGTH - 2, LENGTH), range(2)):
    default_field[i][j].set_team(RED)

default_field[LENGTH - 1][0].set_unit(base(RED))
default_field[LENGTH - 2][1].set_unit(rover(RED))

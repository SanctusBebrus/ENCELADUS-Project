from field import Cell
import units
import player

# Teams
default_team = player.Team((255, 255, 255))
YELLOW = player.Team((255, 215, 0))
GREEN = player.Team((0, 128, 0))
RED = player.Team((255, 0, 0))
BLUE = player.Team((0, 0, 255))

default_field = list(
    map(lambda y: list(map(lambda x: Cell(default_team), range(15))), range(25)))

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
for i in range(4):
    for j in range(11, 15):
        default_field[i][j].set_team(YELLOW)

default_field[0][14].set_unit(base(YELLOW))
default_field[0][13].set_unit(mine(YELLOW))
default_field[0][12].set_unit(tower(YELLOW))

default_field[0][11].set_unit(rover(YELLOW))
default_field[1][11].set_unit(hunter(YELLOW))
default_field[2][11].set_unit(rhino(YELLOW))
default_field[3][11].set_unit(devast(YELLOW))

# GREEN Team
for i in range(21, 25):
    for j in range(11, 15):
        default_field[i][j].set_team(GREEN)

default_field[24][14].set_unit(base(GREEN))
default_field[24][13].set_unit(mine(GREEN))
default_field[24][12].set_unit(tower(GREEN))

default_field[24][11].set_unit(rover(GREEN))
default_field[23][11].set_unit(hunter(GREEN))
default_field[22][11].set_unit(rhino(GREEN))
default_field[21][11].set_unit(devast(GREEN))

# BLUE Team
for i in range(4):
    for j in range(4):
        default_field[i][j].set_team(BLUE)

default_field[0][0].set_unit(base(BLUE))
default_field[0][1].set_unit(mine(BLUE))
default_field[0][2].set_unit(tower(BLUE))

default_field[0][3].set_unit(rover(BLUE))
default_field[1][3].set_unit(hunter(BLUE))
default_field[2][3].set_unit(rhino(BLUE))
default_field[3][3].set_unit(devast(BLUE))

# RED Team
for i in range(21, 25):
    for j in range(4):
        default_field[i][j].set_team(RED)

default_field[24][0].set_unit(base(RED))
default_field[24][1].set_unit(mine(RED))
default_field[24][2].set_unit(tower(RED))

default_field[24][3].set_unit(rover(RED))
default_field[23][3].set_unit(hunter(RED))
default_field[22][3].set_unit(rhino(RED))
default_field[21][3].set_unit(devast(RED))

import pygame

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1400, 780
CAPTION = 'ENCELADUS PROJECT'

cell_size = 80

background_image = pygame.image.load('sprites/backgrounds/background.png')
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

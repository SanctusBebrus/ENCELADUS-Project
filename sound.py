import pygame

path = 'resources/'


class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.default = pygame.mixer.Sound(path + 'default.mp3')

        self.hunter_ = pygame.mixer.Sound(path + 'hunt_.wav')
        self.hunter_1 = pygame.mixer.Sound(path + 'hunter_1.wav')
        self.hunter_2 = pygame.mixer.Sound(path + 'hunter_2.wav')
        self.hunter_3 = pygame.mixer.Sound(path + 'hunter_3.wav')
        self.hunter_4 = pygame.mixer.Sound(path + 'hunter_4.wav')
        self.hunter_5 = pygame.mixer.Sound(path + 'hunter_5.wav')

        self.rhino_ = pygame.mixer.Sound(path + 'rhino_.wav')
        self.rhino_1 = pygame.mixer.Sound(path + 'rhino_1.wav')
        self.rhino_2 = pygame.mixer.Sound(path + 'rhino_2.wav')
        self.rhino_3 = pygame.mixer.Sound(path + 'rhino_3.wav')
        self.rhino_4 = pygame.mixer.Sound(path + 'rhino_4.wav')
        self.rhino_5 = pygame.mixer.Sound(path + 'rhino_5.wav')

        self.devast_ = pygame.mixer.Sound(path + 'devast_.wav')
        self.devast_1 = pygame.mixer.Sound(path + 'devast_1.wav')
        self.devast_2 = pygame.mixer.Sound(path + 'devast_2.wav')
        self.devast_3 = pygame.mixer.Sound(path + 'devast_3.wav')
        self.devast_4 = pygame.mixer.Sound(path + 'devast_4.wav')
        self.devast_5 = pygame.mixer.Sound(path + 'devast_5.wav')

        self.rover_ = pygame.mixer.Sound(path + 'rover_.wav')
        self.rover_1 = pygame.mixer.Sound(path + 'rover_1.wav')
        self.rover_2 = pygame.mixer.Sound(path + 'rover_2.wav')
        self.rover_3 = pygame.mixer.Sound(path + 'rover_3.wav')
        self.rover_4 = pygame.mixer.Sound(path + 'rover_4.wav')
        self.rover_5 = pygame.mixer.Sound(path + 'rover_5.wav')

        self.stage_one_playlist = list()
        self.stage_one_playlist.append(path + 'playlist/battle_11.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_10.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_9.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_8.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_7.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_6.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_5.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_4.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_3.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_2.mp3')
        self.stage_one_playlist.append(path + 'playlist/battle_1.mp3')

import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Ninja game")
        self.screen = pygame.display.set_mode((640, 480))
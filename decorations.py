import pygame


class Barrel(pygame.sprite.Sprite):
    def __init__(self, pos, scale):
        super().__init__()

        self.image = pygame.image.load('sprites/Decorations/barrel.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect(center=pos)
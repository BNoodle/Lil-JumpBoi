import pygame
import constants

class Platform:

    def __init__(self, screen, x, y):
        self.screen = screen
        self.image = pygame.Surface(constants.PLATFORM_SIZE).convert()
        self.image.fill(constants.REGULAR_PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.groupkill = False
        self.type = 'regular'

    def update(self):
        if self.rect.top > constants.SCREEN_SIZE[1]:
            self.groupkill = True
        self.screen.blit(self.image, self.rect)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

    def collidepoint(self, point):
        return self.rect.collidepoint(point)


class JumpBoostPlatform(Platform):
    
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image.fill(constants.JUMP_BOOST_PLATFORM_COLOR)
        self.type = 'jump boost'


class DeathPlatform(Platform):
    
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image.fill(constants.DEATH_PLATFORM_COLOR)
        self.type = 'death'


class NonePlatform(Platform):

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image.set_colorkey(constants.REGULAR_PLATFORM_COLOR)
        self.type = None
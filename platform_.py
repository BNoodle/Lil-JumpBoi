import pygame
import constants

class Platform:

    def __init__(self, screen, x, y):
        self.screen = screen
        self.image = pygame.image.load('Images/regular_platform.png', ).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()*constants.PLATFORM_SCALE, self.image.get_height()*constants.PLATFORM_SCALE))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.groupkill = False
        self.type = 'regular'

    def update(self):
        if self.rect.top > constants.SCREEN_SIZE[1]:
            self.groupkill = True
        self.screen.blit(self.image, self.rect)

    def collidefall(self, a, b):
        return a < self.rect.bottom and b >= a

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

    def collidepoint(self, point):
        return self.rect.collidepoint(point)


class JumpBoostPlatform(Platform):
    
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image = pygame.image.load('Images/jump_boost_platform.png', ).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()*constants.PLATFORM_SCALE, self.image.get_height()*constants.PLATFORM_SCALE))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.type = 'jump boost'


class DeathPlatform(Platform):
    
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image.fill(constants.DEATH_PLATFORM_COLOR)
        self.type = 'death'


class NonePlatform(Platform):

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image.set_colorkey((255, 255, 255))
        self.image.fill((255, 255, 255))
        self.type = None


class DisappearPlatform(Platform):

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image.fill(constants.DISAPPEAR_PLATFORM_COLOR)
        self.image.set_alpha(constants.DISAPPEAR_PLATFORM_ALPHA)
        self.type = 'disappear'
        self.do_collision = True

    def collidepoint(self, point):
        if self.do_collision:
            return super().collidepoint(point)
        else: return False

    def colliderect(self, rect):
        if self.do_collision:
            return super().colliderect(rect)
        else: return False

    def collidefall(self, a, b):
        if self.do_collision:
            return super().collidefall(a, b)
        else:
            return False

    def hit(self):
        self.do_collision = False

    def update(self):
        if not self.do_collision:
            alpha = self.image.get_alpha()-constants.DISAPPEAR_PLATFORM_ALPHA_DECREASE
            if alpha >= 0:
                self.image.set_alpha(alpha)
            else:
                self.groupkill = True
        return super().update()

import pygame
import constants

class Background:

    def __init__(self, screen):
        self.screen = screen

        self.image = pygame.image.load('Images/background.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*constants.BG_SCALE, self.image.get_height()*constants.BG_SCALE)).convert()

        self.y = 0

    def movey(self, num):
        self.y += num*constants.BG_MOVE

    def update(self):
        if self.y >= self.image.get_height():
            self.y -= self.image.get_height()

        self.screen.blit(self.image, (0, self.y))
        self.screen.blit(self.image, (0, self.y-self.image.get_height()))
        self.screen.blit(self.image, (0, self.y+self.image.get_height()))

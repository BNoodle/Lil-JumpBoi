import platform_
import random
import constants
from math import ceil

class SpriteGroup:

    def __init__(self):
        self.group = []

    def add(self, sprite):
        self.group.append(sprite)

    def clear(self):
        self.group = []

    def colliderect(self, rect):
        for sprite in self.group:
            if sprite.colliderect(rect):
                return True, sprite
        return False, None

    def collidepoint(self, point):
        for sprite in self.group:
            if sprite.collidepoint(point):
                return True, sprite
        return False, None

    def update(self):
        sprites_to_remove = []
        for i, sprite in enumerate(self.group):
            sprite.update()
            if sprite.groupkill:
                sprites_to_remove.insert(0, i)
        for i in sprites_to_remove:
            del self.group[i]


class PlatformGroup(SpriteGroup):
    
    def __init__(self, screen, menu):
        super().__init__()
        my_platform = platform_.Platform(screen, self.random_x(under_player=False), constants.SCREEN_SIZE[1]-constants.PLATFORM_SPAWN_DISTANCE)
        self.group.append(my_platform)
        self.screen = screen
        self.menu = menu
        self.safe_counter = 0
        self.jump_boost_chance = constants.JUMP_BOOST_PLATFORM_START_CHANCE
        self.death_chance = constants.DEATH_PLATFORM_START_CHANCE
        self.disappear_chance = constants.DISAPPEAR_PLATFORM_START_CHANCE
        self.no_platform_chance = constants.NO_PLATFORM_START_CHANCE
        self.moving_chance = constants.MOVING_PLATFORM_START_CHANCE
        self.score_counter = 0
        self.score_store = self.menu.score
        self.update()

    def movey(self, distance):
        for platform in self.group:
            platform.rect.y += distance

    def random_x(self, under_player=True):
        num = random.randint(0, constants.SCREEN_SIZE[0]-constants.PLATFORM_SIZE[0])
        if not under_player:
            start = (constants.SCREEN_SIZE[0]//2)-(constants.PLAYER_SIZE[0]//2)-(constants.PLATFORM_SIZE[0])
            end = (constants.SCREEN_SIZE[0]//2)+(constants.PLAYER_SIZE[0]//2)
            while num >= start and num <= end:
                num = random.randint(0, constants.SCREEN_SIZE[0]-constants.PLATFORM_SIZE[0])
        return num

    def spawn(self, x, y):
        self.safe_counter += 1
        n = random.randint(1, 100)
        platform_type = self.platform_chance(n)
        if platform_type == 'regular':
            self.group.append(platform_.Platform(self.screen, x, y))
        elif platform_type == 'jump boost':
            self.group.append(platform_.JumpBoostPlatform(self.screen, x, y))
        elif platform_type == 'death':
            self.group.append(platform_.DeathPlatform(self.screen, x, y))
        elif platform_type == 'disappear':
            self.group.append(platform_.DisappearPlatform(self.screen, x, y))
        elif platform_type == 'moving':
            self.group.append(platform_.MovingPlatform(self.screen, x, y))
        elif platform_type == None:
            self.group.append(platform_.NonePlatform(self.screen, x, y))

    def platform_chance(self, n):
        # safe spawning
        if self.safe_counter == 3:
            self.safe_counter = 0
            if n <= self.jump_boost_chance:
                return 'jump boost'
            elif n <= self.jump_boost_chance+self.disappear_chance:
                return 'disappear'
            elif n <= self.jump_boost_chance+self.disappear_chance+self.moving_chance:
                return 'moving'
            else:
                return 'regular'
        # regular spawning
        else:
            if n <= self.jump_boost_chance:
                return 'jump boost'
            elif n <= self.jump_boost_chance+self.death_chance:
                return 'death'
            elif n <= self.jump_boost_chance+self.death_chance+self.no_platform_chance:
                return None
            elif n <= self.jump_boost_chance+self.death_chance+self.no_platform_chance+self.disappear_chance:
                return 'disappear'
            elif n <= self.jump_boost_chance+self.death_chance+self.no_platform_chance+self.disappear_chance+self.moving_chance:
                return 'moving'
            else:
                return 'regular'

    def add_chance(self):
        self.jump_boost_chance += constants.JUMP_BOOST_PLATFORM_CHANCE_INCREASE
        self.death_chance += constants.DEATH_PLATFORM_CHANCE_INCREASE
        self.no_platform_chance += constants.NO_PLATFORM_CHANCE_INCREASE
        self.disappear_chance += constants.DISAPPEAR_PLATFORM_CHANCE_INCREASE
        self.moving_chance += constants.MOVING_PLATFORM_CHANCE_INCREASE
        if self.jump_boost_chance+self.death_chance+self.no_platform_chance > 100:
            self.jump_boost_chance -= constants.JUMP_BOOST_PLATFORM_CHANCE_INCREASE
            self.death_chance -= constants.DEATH_PLATFORM_CHANCE_INCREASE
            self.no_platform_chance -= constants.NO_PLATFORM_CHANCE_INCREASE
            self.disappear_chance -= constants.DISAPPEAR_PLATFORM_CHANCE_INCREASE
            self.moving_chance -= constants.MOVING_PLATFORM_CHANCE_INCREASE

    def update(self):
        super().update()
        max = 100000
        for platform in self.group:
            if platform.rect.top < max:
                max = platform.rect.top
        for i in range(1, ceil((max+1000)/constants.PLATFORM_SPAWN_DISTANCE)):
            if max-(i*constants.PLATFORM_SPAWN_DISTANCE) > constants.SCREEN_SIZE[1]*0.75:
                x = self.random_x(under_player=False)
            else:
                x = self.random_x()
            self.spawn(x, max-(i*constants.PLATFORM_SPAWN_DISTANCE))
        self.score_counter += self.menu.score-self.score_store
        self.score_store = self.menu.score
        if self.score_counter > constants.SCORE_CHANCE_INCREASE:
            self.score_counter -= constants.SCORE_CHANCE_INCREASE
            self.add_chance()
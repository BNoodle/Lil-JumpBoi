import pygame
import constants
import random

class Player:

    def __init__(self, screen, menu, platforms, x, y):
        self.screen = screen
        self.menu = menu
        self.platforms = platforms

        self.image_jump = pygame.image.load('Images/player_jump.png')
        self.image_jump = pygame.transform.smoothscale(self.image_jump, (self.image_jump.get_width()*constants.PLAYER_SCALE, self.image_jump.get_height()*constants.PLAYER_SCALE)).convert_alpha()
        self.image_stand = pygame.image.load('Images/player_stand.png')
        self.image_stand = pygame.transform.smoothscale(self.image_stand, (self.image_stand.get_width()*constants.PLAYER_SCALE, self.image_stand.get_height()*constants.PLAYER_SCALE)).convert_alpha()
        self.image_death = pygame.image.load('Images/player_death.png')
        self.image_death = pygame.transform.smoothscale(self.image_death, (self.image_death.get_width()*constants.PLAYER_SCALE, self.image_death.get_height()*constants.PLAYER_SCALE)).convert_alpha()
        self.image = self.image_jump

        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.velocity = [0, 0]
        self.acceleration = [0, 0]

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.stored_y = self.rect.bottom
        self.jump_on_floor = True
        self.dead = False

        self.flip = False

        # things the player is allowed to do
        self.do = {
            'gravity': True,
            'move': True,
            'jump': True,
            'camera': True,
            'wraparound': True,
            'die': True,
            'animate': True
        }
        
    def die(self):
        self.dead = True
        self.image = self.image_death
        self.update_rect()
        self.menu.game_over()
        self.do['jump'] = False
        self.do['move'] = False
        self.do['die'] = False
        self.do['wraparound'] = False
        self.do['camera'] = False
        self.do['animate'] = False

    def update_rect(self):
        coord = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = coord

    def update(self):

        # key pressesd
        keys = pygame.key.get_pressed()
        # left and right
        key_left = (keys[pygame.K_a] or keys[pygame.K_LEFT])
        key_right = (keys[pygame.K_d] or keys[pygame.K_RIGHT])
        if (not (key_left and key_right)) and (key_left or key_right):
            if key_left: move_direction = -1
            elif key_right: move_direction = 1
        else: move_direction = 0


        # movement and collision
        self.acceleration = [0, 0]
        # get the initial y
        self.stored_y = self.rect.bottom

        if self.do['gravity']:
            self.acceleration[1] = constants.PLAYER_ACCELERATION[1]
        
        if self.do['move']:        
            target_speed = move_direction*constants.PLAYER_MAX_VELOCITY[0]
            speed_diff = target_speed-self.velocity[0]
            self.acceleration[0] = speed_diff*constants.PLAYER_ACCELERATION[0]

        # add acceleration to velocity
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        # cap at max velocity and make velocity 0 if its low enough
        if abs(self.velocity[0]) > constants.PLAYER_MAX_VELOCITY[0]:
            self.velocity[0] = constants.PLAYER_MAX_VELOCITY[0]*(self.velocity[0]/abs(self.velocity[0]))
        if abs(self.velocity[0]) < 0.5:
            self.velocity[0] = 0
        if abs(self.velocity[1]) > constants.PLAYER_MAX_VELOCITY[1]:
            self.velocity[1] = constants.PLAYER_MAX_VELOCITY[1]
        if abs(self.velocity[1]) < 0.5:
            self.velocity[1] = 0
        # create copies for collisions
        test_rectx = self.rect.copy()
        test_recty = self.rect.copy()
        test_rectx.x += self.velocity[0]
        test_recty.y += self.velocity[1]
        

        # collisions

        # flags for collision detection
        move_rectx = True
        move_recty = True

        # platform collision
        if self.velocity[1] > 0:
            collision, platform = self.platforms.colliderect(test_recty)
            if collision and (platform.collidefall(self.stored_y, self.rect.bottom)):
                if platform.type == 'regular':
                    if self.do['jump']:
                        self.velocity[1] = constants.PLAYER_JUMP_VELOCITY
                        move_recty = False
                        if self.stored_y < platform.rect.top:
                            self.rect.bottom = platform.rect.top
                        platform.hit()
                elif platform.type == 'jump boost':
                    if self.do['jump']:
                        self.velocity[1] = constants.JUMP_BOOST_VELOCITY
                        move_recty = False
                        if self.stored_y < platform.rect.top:
                            self.rect.bottom = platform.rect.top
                        platform.hit()
                elif platform.type == 'death':
                    if self.do['die']:
                        self.die()
                        self.velocity[0] = random.randint(-10, 10)
                        self.velocity[1] = constants.DEATH_PLATFORM_VELOCITY
                        platform.hit()
                elif platform.type == 'disappear':
                    if self.do['jump']:
                        self.velocity[1] = constants.PLAYER_JUMP_VELOCITY
                        move_recty = False
                        if self.stored_y < platform.rect.top:
                            self.rect.bottom = platform.rect.top
                        platform.hit()
        # bottom screen collision
        if test_recty.bottom > self.screen_height:
            if self.jump_on_floor:
                if self.do['jump']:
                    move_recty = False
                    self.velocity[1] = constants.PLAYER_JUMP_VELOCITY
                    self.rect.bottom = self.screen_height
            else:
                if self.do['die']:
                    self.die()
        # side screen collision
        if self.do['wraparound']:
            if test_rectx.right < 0:
                self.rect.left = self.screen_width
            elif test_rectx.left > self.screen_width:
                self.rect.right = 0
        # move rectangle if indicated
        if move_rectx:
            self.rect.x += self.velocity[0]
        if move_recty:
            # move the platforms instead of moving the player if the player is more than halfway
            if self.do['camera']:
                if self.rect.centery + self.velocity[1] < self.screen_height//2 and self.velocity[1] <= -1:
                    diff = self.screen_height//2-(self.rect.centery+self.velocity[1])+1
                    self.rect.centery = self.screen_height//2
                    self.platforms.movey(diff)
                    self.jump_on_floor = False
                    self.menu.score += diff*constants.SCORE_PER_PIXEL
                else:
                    self.rect.y += self.velocity[1]
            else:
                self.rect.y += self.velocity[1]
        
        # animations
        if self.do['animate']:
            if self.velocity[1] >= -1:
                self.image = self.image_jump
            elif self.velocity[1] < -1:
                self.image = self.image_stand
            if self.velocity[0] > 0:
                self.flip = True
            elif self.velocity[0] < 0:
                self.flip = False
            self.image = pygame.transform.flip(self.image, self.flip, False)
            self.update_rect()


        self.screen.blit(self.image, self.rect)

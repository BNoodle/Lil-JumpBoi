import pygame
import constants

class Platform:

    def __init__(self, screen, x, y):
        self.screen = screen
        self.image = pygame.image.load('Images/regular_platform.png', )
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()*constants.PLATFORM_SCALE, self.image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.shadow_image = pygame.image.load('Images/regular_platform_shadow.png', )
        self.shadow_image = pygame.transform.smoothscale(self.shadow_image, (self.shadow_image.get_width()*constants.PLATFORM_SCALE, self.shadow_image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.display_diff = [0, 0]
        self.groupkill = False
        self.type = 'regular'

        self.velocity = [0, 0]
        self.acceleration = [0, 0]

    def hit(self):
        self.velocity[1] = constants.PLATFORM_ANIMATION_VELOCITY

    def update(self):
        if self.rect.top > constants.SCREEN_SIZE[1]:
            self.groupkill = True

        y = self.rect.top+self.display_diff[1]
        target_velocity = (self.rect.top-y)*constants.PLATFORM_ANIMATION_ACCURACY
        speed_diff = target_velocity-self.velocity[1]
        self.acceleration[1] = speed_diff*constants.PLATFORM_ACCELERATION
        if abs(self.velocity[1]) < 0.5:
            self.velocity[1] = 0

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.display_diff[0] += self.velocity[0]
        self.display_diff[1] += self.velocity[1]
        
        rect_to_display = self.rect.copy()
        rect_to_display.x += self.display_diff[0]
        rect_to_display.y += self.display_diff[1]
        shadow_rect = rect_to_display.copy()
        shadow_rect.x += constants.PLATFORM_SHADOW_OFFSET[0]
        shadow_rect.y += constants.PLATFORM_SHADOW_OFFSET[1]
        self.screen.blit(self.shadow_image, shadow_rect)
        self.screen.blit(self.image, rect_to_display)

    def collidefall(self, a, b):
        return a < self.rect.bottom and b >= a

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

    def collidepoint(self, point):
        return self.rect.collidepoint(point)


class JumpBoostPlatform(Platform):
    
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image = pygame.image.load('Images/jump_boost_platform.png', )
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()*constants.PLATFORM_SCALE, self.image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.shadow_image = pygame.image.load('Images/jump_boost_platform_shadow.png', )
        self.shadow_image = pygame.transform.smoothscale(self.shadow_image, (self.shadow_image.get_width()*constants.PLATFORM_SCALE, self.shadow_image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.type = 'jump boost'


class DeathPlatform(Platform):
    
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image = pygame.image.load('Images/death_platform.png')
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()*constants.PLATFORM_SCALE, self.image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.shadow_image = pygame.image.load('Images/death_platform_shadow.png', )
        self.shadow_image = pygame.transform.smoothscale(self.shadow_image, (self.shadow_image.get_width()*constants.PLATFORM_SCALE, self.shadow_image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.rect = pygame.Rect((x, y-constants.DEATH_PLATFORM_SPIKE_HEIGHT), (self.image.get_width(), constants.DEATH_PLATFORM_SPIKE_HEIGHT))
        self.type = 'death'

    def hit(self):    
        self.velocity[1] = -constants.PLATFORM_ANIMATION_VELOCITY


class NonePlatform(Platform):

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image.set_colorkey((255, 255, 255))
        self.image.fill((255, 255, 255))
        self.shadow_image.set_colorkey((255, 255, 255))
        self.shadow_image.fill((255, 255, 255))
        self.type = None


class DisappearPlatform(Platform):

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image = pygame.image.load('Images/disappear_platform.png')
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()*constants.PLATFORM_SCALE, self.image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.shadow_image = pygame.image.load('Images/disappear_platform_shadow.png', )
        self.shadow_image = pygame.transform.smoothscale(self.shadow_image, (self.shadow_image.get_width()*constants.PLATFORM_SCALE, self.shadow_image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.image.set_alpha(constants.DISAPPEAR_PLATFORM_ALPHA)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height()-(100*constants.PLATFORM_SCALE))
        self.type = 'disappear'
        self.do_collision = True
        self.target_velocity = 0

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
        super().hit()
        self.do_collision = False
        self.target_velocity = constants.DISAPPEAR_PLATFORM_FALL_VELOCITY

    def update(self):
        if not self.do_collision:
            alpha = self.image.get_alpha()-constants.DISAPPEAR_PLATFORM_ALPHA_DECREASE
            if alpha >= 0:
                self.image.set_alpha(alpha)
                self.shadow_image.set_alpha(alpha)
            else:
                self.groupkill = True
                
        y = self.rect.top+self.display_diff[1]
        speed_diff = self.target_velocity-self.velocity[1]
        self.acceleration[1] = speed_diff*constants.PLATFORM_ACCELERATION
        if abs(self.velocity[1]) < 0.5:
            self.velocity[1] = 0

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.display_diff[0] += self.velocity[0]
        self.display_diff[1] += self.velocity[1]
        
        rect_to_display = self.rect.copy()
        rect_to_display.x += self.display_diff[0]
        rect_to_display.y += self.display_diff[1]
        shadow_rect = rect_to_display.copy()
        shadow_rect.x += constants.PLATFORM_SHADOW_OFFSET[0]
        shadow_rect.y += constants.PLATFORM_SHADOW_OFFSET[1]
        self.screen.blit(self.shadow_image, shadow_rect)
        self.screen.blit(self.image, rect_to_display)


class MovingPlatform(Platform):

    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.image1 = pygame.image.load('Images/moving_platform1.png')
        self.image1 = pygame.transform.smoothscale(self.image1, (self.image1.get_width()*constants.PLATFORM_SCALE, self.image1.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.image2 = pygame.image.load('Images/moving_platform2.png')
        self.image2 = pygame.transform.smoothscale(self.image2, (self.image2.get_width()*constants.PLATFORM_SCALE, self.image2.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.image3 = pygame.image.load('Images/moving_platform3.png')
        self.image3 = pygame.transform.smoothscale(self.image3, (self.image3.get_width()*constants.PLATFORM_SCALE, self.image3.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.image4 = pygame.image.load('Images/moving_platform4.png')
        self.image4 = pygame.transform.smoothscale(self.image4, (self.image4.get_width()*constants.PLATFORM_SCALE, self.image4.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.image5 = pygame.image.load('Images/moving_platform5.png')
        self.image5 = pygame.transform.smoothscale(self.image5, (self.image5.get_width()*constants.PLATFORM_SCALE, self.image5.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.image6 = pygame.image.load('Images/moving_platform6.png')
        self.image6 = pygame.transform.smoothscale(self.image6, (self.image6.get_width()*constants.PLATFORM_SCALE, self.image6.get_height()*constants.PLATFORM_SCALE)).convert_alpha()
        self.shadow_image = pygame.image.load('Images/moving_platform_shadow.png', )
        self.shadow_image = pygame.transform.smoothscale(self.shadow_image, (self.shadow_image.get_width()*constants.PLATFORM_SCALE, self.shadow_image.get_height()*constants.PLATFORM_SCALE)).convert_alpha()

        self.image_list = [self.image1, self.image2, self.image3, self.image4, self.image5, self.image6, self.image5, self.image4, self.image3, self.image2]
        self.animation_length = len(self.image_list)-1
        self.current_image = 0
        self.image = self.image_list[self.current_image]

        self.animation_timer = 0

        self.rect = pygame.Rect((x, y), (self.image.get_width(), self.image.get_height()-constants.MOVING_PLATFORM_JET_HEIGHT))
        self.current_direction = constants.MOVING_PLATFORM_SPEED
        self.type = 'moving'

    def update(self):
        self.rect.x += self.current_direction
        if self.rect.right > constants.SCREEN_SIZE[0] or self.rect.left < 0:
            self.current_direction *= -1
            self.rect.x += self.current_direction*2

        self.animation_timer += 1
        if self.animation_timer >= constants.MOVING_PLATFORM_ANIMATION_SPEED:
            self.animation_timer = 0
            self.current_image += 1
            if self.current_image > self.animation_length:
                self.current_image = 0
            self.image = self.image_list[self.current_image]

        super().update()

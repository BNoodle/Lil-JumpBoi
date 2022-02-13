import pygame
import constants

class Menu:

    def __init__(self, screen, save_file):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.save_file = save_file

        self.mode = 'title'

        self.score_font = pygame.font.Font(None, constants.SCORE_SIZE)

        self.score = 0
        self.highscore = self.save_file.data['highscore']

        self.fade_cover = pygame.Surface((screen.get_width(), screen.get_height())).convert()
        self.fade_cover.fill((0, 0, 0))
        self.fade_amount = constants.MAX_FADE_AMOUNT
        self.fade_cover.set_alpha(self.fade_amount)
        
        self.game_over_image = pygame.image.load('Images/game_over.png').convert_alpha()
        self.game_over_image = pygame.transform.smoothscale(self.game_over_image, (self.game_over_image.get_width()*constants.GAME_OVER_SCALE, self.game_over_image.get_height()*constants.GAME_OVER_SCALE))
        self.game_over_pos = ((constants.SCREEN_SIZE[0]//2)-(self.game_over_image.get_width()//2), (constants.SCREEN_SIZE[1]//2)-(self.game_over_image.get_height()//2))

        self.restart_font = pygame.font.Font(None, constants.RESTART_SIZE)
        self.restart_text = self.restart_font.render(constants.RESTART_TEXT, True, constants.RESTART_COLOR)
        self.restart_pos = ((self.screen_width//2)-(self.restart_text.get_width()//2), (self.screen_height-self.restart_text.get_height()-10))

        self.title_image = pygame.image.load('Images/title.png').convert_alpha()
        self.title_image = pygame.transform.smoothscale(self.title_image, (self.title_image.get_width()*constants.TITLE_SCALE, self.title_image.get_height()*constants.TITLE_SCALE))
        self.title_pos = ((self.screen_width//2)-(self.title_image.get_width()//2), (self.screen_height//2-self.title_image.get_height()//2))

        self.credits_font = pygame.font.Font(None, constants.CREDITS_SIZE)
        self.credits_text = self.credits_font.render(constants.CREDITS_TEXT, True, constants.CREDITS_COLOR)
        self.credits_pos = ((self.screen_width//2)-(self.credits_text.get_width()//2), self.title_pos[1]+self.title_image.get_height()+10)

        self.start_font = pygame.font.Font(None, constants.START_SIZE)
        self.start_text = self.start_font.render(constants.START_TEXT, True, constants.START_COLOR)
        self.start_pos = ((self.screen_width//2)-(self.start_text.get_width()//2), (self.screen_height-self.start_text.get_height()-10))

    def game_over(self):
        self.mode = 'game over'

    def exit_title(self):
        self.mode = 'restart'

    def get_mode(self):
        return self.mode

    def show_title(self):
        self.screen.blit(self.start_text, self.start_pos)
        self.screen.blit(self.title_image, self.title_pos)
        self.screen.blit(self.credits_text, self.credits_pos)

    def show_score(self):
        score_text = self.score_font.render(f'Score: {int(self.score)}', True, constants.SCORE_COLOR)
        self.screen.blit(score_text, (10, 10))

    def show_highscore(self):
        highscore_text = self.score_font.render(f'Highscore: {self.highscore}', True, constants.HIGHSCORE_COLOR)
        self.screen.blit(highscore_text, (self.screen_width-10-highscore_text.get_width(), 10))

    def show_game_over(self):
        self.screen.blit(self.game_over_image, self.game_over_pos)
        self.screen.blit(self.restart_text, self.restart_pos)

    def fade_out(self):
        if not self.fade_amount >= constants.MAX_FADE_AMOUNT:
            self.fade_amount += constants.FADE_SPEED
            self.fade_cover.set_alpha(self.fade_amount)
        self.screen.blit(self.fade_cover, (0, 0))

    def fade_in(self):
        if not self.fade_amount <= 0:
            self.fade_amount -= constants.FADE_SPEED
            self.fade_cover.set_alpha(self.fade_amount)
        self.screen.blit(self.fade_cover, (0, 0))

    def update(self):
        if self.mode == 'title':
            self.fade_out()
            self.show_title()
        elif self.mode == 'play':
            self.fade_in()
            if self.score > self.highscore: self.highscore = int(self.score)
            self.show_score()
            self.show_highscore()
        elif self.mode == 'game over':
            self.fade_out()
            self.show_score()
            self.show_highscore()
            self.show_game_over()
            self.save_file.data['highscore'] = self.highscore
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.mode = 'restart'
        elif self.mode == 'restart':
            self.score = 0
            self.mode = 'play'

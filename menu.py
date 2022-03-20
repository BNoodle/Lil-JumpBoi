import pygame
import constants

class Menu:

    def __init__(self, screen, save_file):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.save_file = save_file

        self.mode = 'title'

        self.score_font = pygame.font.Font('Fonts/Roboto.ttf', constants.SCORE_SIZE)

        self.score = 0
        self.highscore = self.save_file.data['highscore']

        self.fade_cover = pygame.Surface((screen.get_width(), screen.get_height())).convert()
        self.fade_cover.fill((0, 0, 0))
        self.fade_amount = constants.MAX_FADE_AMOUNT
        self.fade_cover.set_alpha(self.fade_amount)
        
        self.game_over_image = pygame.image.load('Images/game_over.png')
        self.game_over_image = pygame.transform.smoothscale(self.game_over_image, (self.game_over_image.get_width()*constants.GAME_OVER_SCALE, self.game_over_image.get_height()*constants.GAME_OVER_SCALE)).convert_alpha()
        self.game_over_pos = (0, 0)

        self.title_image = pygame.image.load('Images/title.png')
        self.title_image = pygame.transform.smoothscale(self.title_image, (self.title_image.get_width()*constants.TITLE_SCALE, self.title_image.get_height()*constants.TITLE_SCALE)).convert_alpha()
        self.title_pos = (0, 0)

        self.play_fade = pygame.image.load('Images/play.png')
        self.play_fade = pygame.transform.smoothscale(self.play_fade, (self.play_fade.get_width()*constants.PLAY_SCALE, self.play_fade.get_height()*constants.PLAY_SCALE)).convert_alpha()
        self.play_fade_pos = (0, 0)

    def add_score(self, num):
        self.score += num

    def game_over(self):
        self.mode = 'game over'

    def restart(self):
        self.mode = 'restart'

    def exit_title(self):
        self.mode = 'restart'

    def get_mode(self):
        return self.mode

    def show_title(self):
        self.screen.blit(self.title_image, self.title_pos)

    def show_score(self):
        score_text = self.score_font.render(f'Score: {int(self.score)}', True, constants.SCORE_COLOR)
        self.screen.blit(score_text, (10, 10))

    def show_highscore(self):
        highscore_text = self.score_font.render(f'Highscore: {self.highscore}', True, constants.HIGHSCORE_COLOR)
        self.screen.blit(highscore_text, (self.screen_width-10-highscore_text.get_width(), 10))

    def show_game_over(self):
        self.screen.blit(self.game_over_image, self.game_over_pos)

    def show_play_fade(self):
        self.screen.blit(self.play_fade, self.play_fade_pos)

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

    def fade_hold(self):
        self.screen.blit(self.fade_cover, (0, 0))

    def update(self):
        if self.mode == 'title':
            self.show_play_fade()
            self.fade_out()
            self.show_title()
        elif self.mode == 'play':
            self.fade_in()
            if self.score > self.highscore: self.highscore = int(self.score)
            self.show_play_fade()
            self.show_score()
            self.show_highscore()
        elif self.mode == 'game over':
            self.show_play_fade()
            self.fade_out()
            self.show_score()
            self.show_highscore()
            self.show_game_over()
            self.save_file.data['highscore'] = self.highscore
        elif self.mode == 'restart':
            self.fade_hold()
            self.score = 0
            self.mode = 'play'

import pygame
import constants

class Menu:

    def __init__(self, screen, save_file):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.save_file = save_file

        self.mode = 'play'

        self.score_font = pygame.font.Font(None, constants.SCORE_SIZE)

        self.score = 0
        self.highscore = self.save_file.data['highscore']

        self.fade_cover = pygame.Surface((screen.get_width(), screen.get_height())).convert()
        self.fade_cover.fill((0, 0, 0))
        self.fade_amount = 0
        self.fade_cover.set_alpha(self.fade_amount)
        
        self.game_over_font = pygame.font.Font(None, constants.GAME_OVER_SIZE)
        self.game = self.game_over_font.render('Game', True, constants.GAME_OVER_COLOR)
        self.game_pos = ((self.screen_width/2)-(self.game.get_width()/2), ((self.screen_height//2)-(self.game.get_height())))
        self.over = self.game_over_font.render('Over', True, constants.GAME_OVER_COLOR)
        self.over_pos = ((self.screen_width/2)-(self.over.get_width()/2), self.screen_height//2)

        self.restart_font = pygame.font.Font(None, constants.RESTART_SIZE)
        self.restart_text = self.restart_font.render('Press SPACE to restart', True, constants.RESTART_COLOR)

    def game_over(self):
        self.mode = 'game over'

    def get_mode(self):
        return self.mode

    def show_score(self):
        score_text = self.score_font.render(f'Score: {int(self.score)}', True, constants.SCORE_COLOR)
        self.screen.blit(score_text, (10, 10))

    def show_highscore(self):
        highscore_text = self.score_font.render(f'Highscore: {self.highscore}', True, constants.HIGHSCORE_COLOR)
        self.screen.blit(highscore_text, (self.screen_width-10-highscore_text.get_width(), 10))

    def show_game_over(self):
        self.screen.blit(self.game, self.game_pos)
        self.screen.blit(self.over, self.over_pos)
        self.screen.blit(self.restart_text, ((self.screen_width//2)-(self.restart_text.get_width()//2), (self.screen_height-self.restart_text.get_height()-10)))

    def update(self):
        if self.mode == 'play':
            if self.score > self.highscore: self.highscore = int(self.score)
            self.show_score()
            self.show_highscore()
        elif self.mode == 'game over':
            if not self.fade_amount >= constants.GAME_OVER_FADE_AMOUNT:
                self.fade_amount += constants.GAME_OVER_FADE_SPEED
                self.fade_cover.set_alpha(self.fade_amount)
            self.screen.blit(self.fade_cover, (0, 0))
            self.show_score()
            self.show_highscore()
            self.show_game_over()
            self.save_file.data['highscore'] = self.highscore
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.mode = 'restart'
        elif self.mode == 'restart':
            self.score = 0
            self.fade_amount = 0
            self.mode = 'play'

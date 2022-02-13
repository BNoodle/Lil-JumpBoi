import pygame
from os import path
import constants
import player
import group
import menu
import save_managing

pygame.init()

SCREEN_DIMENSIONS = WIDTH, HEIGHT = constants.SCREEN_SIZE
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
FPS = 60
clock = pygame.time.Clock()

# save file
default_data = {
    'highscore': 0
}
save_file = save_managing.SaveFile(path.join(path.dirname(__file__), 'save'), default_data)

my_menu = menu.Menu(screen, save_file)
platforms = group.PlatformGroup(screen, my_menu)
my_player = player.Player(screen, my_menu, platforms, WIDTH//2-(0.5*constants.PLAYER_SIZE[0]), HEIGHT*0.75)
my_player.do['move'] = False
my_player.do['jump'] = False
my_player.do['gravity'] = False

running = True
while running:  
    screen.fill(constants.BG_COLOR)
    
    menu_mode = my_menu.get_mode()
    if menu_mode == 'title':
        platforms.update()
        platforms.movey(1)
        my_menu.update()
        my_player.update()
    elif menu_mode == 'play':
        platforms.update()
        my_player.update()
        my_menu.update()
    elif menu_mode == 'game over':
        platforms.update()
        my_player.update()
        my_menu.update()
    elif menu_mode == 'restart':
        platforms = group.PlatformGroup(screen, my_menu)
        my_player = player.Player(screen, my_menu, platforms, WIDTH//2-(0.5*constants.PLAYER_SIZE[0]), HEIGHT*0.75)
        my_menu.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if my_menu.get_mode() == 'title':
                my_menu.exit_title()
        if event.type == pygame.QUIT:
            running = False
            save_file.save()
    pygame.display.flip()
    clock.tick(FPS)
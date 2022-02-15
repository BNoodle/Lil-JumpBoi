import pygame
import os
import constants
import player
import group
import menu
import save_managing

os.chdir(os.path.dirname(__file__))
pygame.init()

SCREEN_DIMENSIONS = WIDTH, HEIGHT = constants.SCREEN_SIZE
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
FPS = 60
clock = pygame.time.Clock()

background_image = pygame.image.load('Images/background.png')
background_image = pygame.transform.scale(background_image, (background_image.get_width()*constants.BG_SCALE, background_image.get_height()*constants.BG_SCALE)).convert()

# save file
default_data = {
    'highscore': 0
}
save_file = save_managing.SaveFile(os.path.join(os.path.dirname(__file__), 'save'), default_data)

my_menu = menu.Menu(screen, save_file)
platforms = group.PlatformGroup(screen, my_menu)
my_player = player.Player(screen, my_menu, platforms, WIDTH//2-(0.5*constants.PLAYER_SIZE[0]), HEIGHT*0.75)
my_player.do['move'] = False
my_player.do['jump'] = False
my_player.do['gravity'] = False

running = True
while running:  
    screen.blit(background_image, (0, 0))
    
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
            elif my_menu.get_mode() == 'game over':
                if event.key == pygame.K_SPACE:
                    my_menu.restart()
        if event.type == pygame.QUIT:
            running = False
            save_file.save()
    pygame.display.flip()
    clock.tick(FPS)
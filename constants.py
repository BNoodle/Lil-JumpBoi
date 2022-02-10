# screen vars
SCREEN_SIZE = 650, 1000
BG_COLOR = (30, 30, 30)
SCORE_COLOR = (255, 255, 255)
SCORE_SIZE = 30
SCORE_PER_PIXEL = 0.5
HIGHSCORE_COLOR = (255, 255, 255)
GAME_OVER_FADE_AMOUNT = 175
GAME_OVER_FADE_SPEED = 5
GAME_OVER_SIZE = 150
GAME_OVER_COLOR = (255, 0, 0)
RESTART_SIZE = 25
RESTART_COLOR = (255, 255, 255)

# player vars
PLAYER_SIZE = 50
PLAYER_COLOR = (255, 255, 255)
PLAYER_ACCELERATION = (0.15, 0.5)
PLAYER_MAX_VELOCITY = [10, 100]
PLAYER_JUMP_VELOCITY = -15

# platform looks
PLATFORM_SCALE = 0.1
PLATFORM_SIZE = [1120*PLATFORM_SCALE, 220*PLATFORM_SCALE]
PLATFORM_SPAWN_DISTANCE = 75
REGULAR_PLATFORM_COLOR = (0, 200, 0)
JUMP_BOOST_PLATFORM_COLOR = (255, 255, 0)
JUMP_BOOST_VELOCITY = -30
DEATH_PLATFORM_COLOR = (215, 0, 0)
DEATH_PLATFORM_VELOCITY = 50
DISAPPEAR_PLATFORM_COLOR = (255, 255, 255)
DISAPPEAR_PLATFORM_ALPHA = 150
DISAPPEAR_PLATFORM_ALPHA_DECREASE = 5
SCORE_CHANCE_INCREASE = 2000

# platform chances
JUMP_BOOST_PLATFORM_START_CHANCE = 5
JUMP_BOOST_PLATFORM_CHANCE_INCREASE = 0
DEATH_PLATFORM_START_CHANCE = 5
DEATH_PLATFORM_CHANCE_INCREASE = 1
DISAPPEAR_PLATFORM_START_CHANCE = 3
DISAPPEAR_PLATFORM_CHANCE_INCREASE = 1.1
NO_PLATFORM_START_CHANCE = 5
NO_PLATFORM_CHANCE_INCREASE = 1.5
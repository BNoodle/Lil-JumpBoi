# screen vars
RESIZE_SCREEN_SCALE = 0.75
SCREEN_SIZE = 750, 1100
BG_COLOR = (30, 30, 30)
BG_SCALE = 0.1
BG_MOVE = 0.25
SCORE_COLOR = (255, 255, 255)
SCORE_SIZE = 25
SCORE_PER_PIXEL = 0.5
HIGHSCORE_COLOR = (255, 255, 255)
MAX_FADE_AMOUNT = 100
FADE_SPEED = 5
GAME_OVER_SCALE = 0.1
TITLE_SCALE = 0.1
TITLE_PLATFORM_MOVE = 1
PLAY_SCALE = 0.1

# player vars
PLAYER_SCALE = 0.1
PLAYER_SIZE = [600*PLAYER_SCALE, 1050*PLAYER_SCALE]
PLAYER_ACCELERATION = (0.15, 0.5)
PLAYER_MAX_VELOCITY = [12, 100]
PLAYER_JUMP_VELOCITY = -15

# platform looks
PLATFORM_SHADOW_OFFSET = [7, 7]
PLATFORM_ANIMATION_VELOCITY = 10
PLATFORM_ANIMATION_ACCURACY = 0.2
PLATFORM_ACCELERATION = 0.3
PLATFORM_SCALE = 0.1
PLATFORM_SIZE = [1100*PLATFORM_SCALE, 300*PLATFORM_SCALE]
PLATFORM_SPAWN_DISTANCE = 75
JUMP_BOOST_VELOCITY = -30
DEATH_PLATFORM_VELOCITY = -5
DEATH_PLATFORM_SPIKE_HEIGHT = 191*PLATFORM_SCALE # 491 - 300
DISAPPEAR_PLATFORM_ALPHA = 255
DISAPPEAR_PLATFORM_ALPHA_DECREASE = 20
DISAPPEAR_PLATFORM_FALL_VELOCITY = 3
MOVING_PLATFORM_JET_HEIGHT = 219*PLATFORM_SCALE # 519 - 300
MOVING_PLATFORM_SPEED = 1
MOVING_PLATFORM_ANIMATION_SPEED = 3
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
MOVING_PLATFORM_START_CHANCE = 2
MOVING_PLATFORM_CHANCE_INCREASE = 1.4

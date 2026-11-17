WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black background
PLAYER_COLOR = (60, 140, 255)  # Blue player
PLAYER_COLOR2 = (255, 140, 60)  # Orange player
PLAYER_SPEED = 6  # Speed of the player movement

OBSTACLES_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

SPAWN_OBSTACLE_DELAY = 500 #milliseconds

MIN_PLAYER_SPEED = 2  # Lowest speed of player 1
MAX_PLAYER_SPEED = 12  # Highest speed of player 1
MIN_SPAWN_DELAY = 150  # The spawn delay can never be lower than this

INITIAL_LIVES = 3  # Challenge 10: lives of each player
INVULNERABLE_TIME = 2000  # Challenge 10: milliseconds of invulnerability after a hit

POWERUP_SIZE = 30  # Challenge 11: size of a power-up
POWERUP_SPAWN_DELAY = 8000  # Challenge 11: milliseconds between power-ups
POWERUP_LIFETIME = 6000  # Challenge 11: milliseconds a power-up stays on screen
SPEED_BOOST_BONUS = 4  # Challenge 11: extra speed while the boost is active
SPEED_BOOST_DURATION = 5000  # Challenge 11: milliseconds the boost lasts

SCORES_FILE = "scores.txt"  # Challenge 12: file where the scores are saved
MAX_NAME_LENGTH = 10  # Challenge 12: maximum letters in the name
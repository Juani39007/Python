import pygame
from config import *
from player import Player
from obstacle import Obstacle


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Player Game")
clock = pygame.time.Clock()

# Create a player object
player = Player(375, 530)
player2 = Player(100, 100, PLAYER_COLOR2,2)  # Create a second player object

obstacles = [] # List to store obstacles

last_obstacle_spawn_time = pygame.time.get_ticks()  # Track the last time an obstacle was spawned

score = 0  # Initialize the score
game_over = False  # Initialize the game over state
paused = False  # True while the game is paused
high_score = 0  # Best score of this run
survival_time = 0  # Milliseconds survived
last_tick = pygame.time.get_ticks()  # Time of the previous frame

font = pygame.font.Font(None, 36)  

def get_spawn_delay(current_score):
    """Every 10 points the delay is 50 ms shorter, never below the minimum"""
    delay = SPAWN_OBSTACLE_DELAY - (current_score // 10) * 50
    return max(delay, MIN_SPAWN_DELAY)


def reset_game():
    """Start a new game (the high score is kept)"""
    global player, player2, obstacles, score, game_over, survival_time

    player = Player(375, 530)
    player2 = Player(100, 100, PLAYER_COLOR2, 2)
    obstacles = []
    score = 0
    survival_time = 0
    game_over = False 

# GAME LOOP
running = True  
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not game_over:
                paused = not paused  # Pause / continue
            if event.key == pygame.K_r and game_over:
                reset_game()  # Restart after Game Over
            if event.key == pygame.K_PLUS:
                player.change_speed(1)  # Speed up player 1
            if event.key == pygame.K_MINUS:
                player.change_speed(-1)  # Slow down player 1

    # The survival time only grows while the game is running
    now = pygame.time.get_ticks()
    if not game_over and not paused:  
        survival_time += now - last_tick
    last_tick = now
         

    if not game_over and not paused:
        #OBSTACLES spawning logic
        current_time = pygame.time.get_ticks()
        if current_time - last_obstacle_spawn_time > get_spawn_delay(score):  
            obstacles.append(Obstacle())
            last_obstacle_spawn_time = current_time

        # Update the position of each obstacle
        for obstacle in obstacles:
            obstacle.move()
            if player.rect.colliderect(obstacle.rect) or player2.rect.colliderect(obstacle.rect):  
                game_over = True


        # Remove obstacles that are off the screen
        visible_obstacles = []
        for obstacle in obstacles:
            if not obstacle.is_off_screen():
                visible_obstacles.append(obstacle)
            else :
                score += 1  # Increment the score for each obstacle that goes off screen
        obstacles = visible_obstacles
        if score > high_score:
            high_score = score  # Remember the best score


        # Update the player's position
        player.moveArrows()
        player2.moveWASD()  # Update the second player's position

    screen.fill(BACKGROUND_COLOR)  # Blue background
    player.draw(screen)  # Draw the player rectangle
    player2.draw(screen)  # Draw the second player rectangle
    
    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw each obstacle

    # Display the score
    
    score_text = font.render(f"Score: {score}   Best: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    time_text = font.render(f"Time: {survival_time // 1000}", True, (255, 255, 255))
    screen.blit(time_text, (10, 40))

    if paused:
        pause_text = font.render("PAUSE", True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

    # Display the game over message if the game is over
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
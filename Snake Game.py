import pygame
import sys
import time
import random

# Difficulty settings
difficulty = 22  # Change this to increase/decrease speed

# Window size
frame_size_x = 720
frame_size_y = 480

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Initialize game window
pygame.display.set_caption('3D Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
yellow = pygame.Color(255, 255, 0)
dark_green = pygame.Color(0, 200, 0)  # Darker green for shading
shadow = pygame.Color(50, 50, 50)  # Shadow effect
cyan = pygame.Color(0, 255, 255)  # Cyan for food

# FPS controller
fps_controller = pygame.time.Clock()

# High Score Management
def get_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

def save_high_score(new_score):
    high_score = get_high_score()
    if new_score > high_score:
        with open("highscore.txt", "w") as file:
            file.write(str(new_score))

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0
high_score = get_high_score()

# Function to display score and high score
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    
    # High Score first
    high_score_surface = score_font.render('High Score: {}'.format(high_score), True, color)
    score_surface = score_font.render('Score: {}'.format(score), True, color)
    
    high_score_rect = high_score_surface.get_rect(topleft=(10, 10))
    score_rect = score_surface.get_rect(topleft=(10, 35))
    
    game_window.blit(high_score_surface, high_score_rect)
    game_window.blit(score_surface, score_rect)


# Game Over function
def game_over():
    global high_score
    save_high_score(score)
    high_score = get_high_score()
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('YOU DIED', True, red, None)
    game_over_rect = game_over_surface.get_rect(midtop=(frame_size_x/2, frame_size_y/4))
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Function to draw the snake in 3D style
def draw_snake():
    for index, pos in enumerate(snake_body):
        # Color logic: Head has more highlights
        if index == 0:  
            body_color = green if is_prime(score) else yellow
            shadow_color = dark_green if is_prime(score) else pygame.Color(180, 180, 0)  # Darker yellow
        else:
            body_color = dark_green if is_prime(score) else pygame.Color(180, 180, 0)  # Body slightly darker
            shadow_color = shadow  # Gray shadow for depth

        # Create 3D shadow effect
        pygame.draw.rect(game_window, shadow_color, pygame.Rect(pos[0] + 2, pos[1] + 2, 10, 10))
        
        # Create main body
        pygame.draw.rect(game_window, body_color, pygame.Rect(pos[0], pos[1], 10, 10))
        
        # Add a highlight for 3D effect
        pygame.draw.rect(game_window, white, pygame.Rect(pos[0] + 2, pos[1] + 2, 4, 4))

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake in the chosen direction
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Wrap around screen edges (instead of game over)
    if snake_pos[0] < 0:
        snake_pos[0] = frame_size_x - 10
    if snake_pos[0] >= frame_size_x:
        snake_pos[0] = 0
    if snake_pos[1] < 0:
        snake_pos[1] = frame_size_y - 10
    if snake_pos[1] >= frame_size_y:
        snake_pos[1] = 0

    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    game_window.fill(black)

    # Draw snake in 3D style
    draw_snake()

    # Draw food (Changed to Cyan)
    pygame.draw.rect(game_window, cyan, pygame.Rect(food_pos[0], food_pos[1], 10, 10))  # Cyan food

    # Check collision with itself (Game Over)
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()



    show_score(white, 'consolas', 20)
    pygame.display.update()
    fps_controller.tick(difficulty)

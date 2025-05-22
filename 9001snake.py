import pygame
import random
import sys

# --- Constants ---
# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20  # Size of each grid cell, snake and food are based on this
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Snake color
RED = (255, 0, 0)    # Food color
DARK_GREEN = (0, 150, 0) # Snake head color
GRAY = (100, 100, 100) # Grid line color (optional)
BUTTON_COLOR = (50, 150, 50) # Button color
BUTTON_TEXT_COLOR = WHITE
BUTTON_HOVER_COLOR = (70, 180, 70) # Button hover color
PAUSE_OVERLAY_COLOR = (0, 0, 0, 150) # Semi-transparent black for pause overlay

# Snake movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 7  # Game FPS, controls snake speed

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
# Use different font sizes for different texts
font = pygame.font.Font(None, 36) # For displaying score and game over messages
title_font = pygame.font.Font(None, 72) # For game title and pause message
button_font = pygame.font.Font(None, 48) # For button text
small_font = pygame.font.Font(None, 28) # For smaller instructions

# --- Helper Functions ---
def draw_grid():
    """Draw grid lines (optional)"""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

def draw_snake(snake_body):
    """Draw the snake"""
    for i, segment in enumerate(snake_body):
        rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        if i == 0: # Snake head uses dark green
            pygame.draw.rect(screen, DARK_GREEN, rect)
            pygame.draw.rect(screen, WHITE, rect, 1) # Border
        else:
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, WHITE, rect, 1) # Border


def draw_food(food_pos):
    """Draw the food"""
    rect = pygame.Rect(food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, WHITE, rect, 1) # Border

def spawn_food(snake_body):
    """Randomly generate food position, ensure it's not on the snake"""
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake_body:
            return food_pos

def display_score(score):
    """Display the score"""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# --- Screen State Functions ---
def start_screen():
    """Display start screen and start game button"""
    button_width = 200
    button_height = 60
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 2 + 30
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    title_text_surface = title_font.render("Snake Game", True, GREEN)
    title_text_rect = title_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    button_text_surface = button_font.render("Start Game", True, BUTTON_TEXT_COLOR)
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)

    instructions_text_surface = font.render("Press Q to Quit", True, GRAY)
    instructions_text_rect = instructions_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))

    waiting_for_start = True
    while waiting_for_start:
        mouse_pos = pygame.mouse.get_pos()
        current_button_color = BUTTON_COLOR

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # Allow quitting from start screen by pressing Q
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    if button_rect.collidepoint(mouse_pos):
                        waiting_for_start = False # Click button, start game
            
        # Button hover effect
        if button_rect.collidepoint(mouse_pos):
            current_button_color = BUTTON_HOVER_COLOR

        screen.fill(BLACK)
        screen.blit(title_text_surface, title_text_rect)

        pygame.draw.rect(screen, current_button_color, button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 3) # Button border
        screen.blit(button_text_surface, button_text_rect)
        screen.blit(instructions_text_surface, instructions_text_rect)

        pygame.display.flip()
        clock.tick(15) # Start screen doesn't need high FPS

def game_over_screen(score):
    """Display game over message and restart prompt"""
    screen.fill(BLACK) # Clear screen
    game_over_text = title_font.render("Game Over!", True, RED) # Using large font
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart, Q to Quit", True, WHITE)

    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3 + 20))

    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(restart_text, restart_text_rect)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting_for_input = False # Break loop, will trigger re-invocation of main_game()
        clock.tick(5) # Game over screen doesn't need high FPS

def display_pause_message():
    """Displays a 'Paused' message on the screen."""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(PAUSE_OVERLAY_COLOR)
    screen.blit(overlay, (0,0))

    pause_text_surface = title_font.render("PAUSED", True, WHITE)
    pause_text_rect = pause_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(pause_text_surface, pause_text_rect)

    resume_text_surface = small_font.render("Press P to Resume", True, WHITE)
    resume_text_rect = resume_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(resume_text_surface, resume_text_rect)

# --- Main Game Logic ---
def main_game():
    global FPS # Allow modification of global FPS variable

    # Snake's initial state
    snake_body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),  # Snake head
                  (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                  (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
    current_direction = RIGHT  # Initially to the right

    # Food initial position
    food_pos = spawn_food(snake_body)

    score = 0
    game_over = False
    paused = False # <--- New: Pause state variable
    current_fps = FPS # Initial speed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # <--- New: Pause/Resume functionality
                    paused = not paused
                if not paused: # Only process game input if not paused
                    if event.key == pygame.K_UP and current_direction != DOWN:
                        current_direction = UP
                    elif event.key == pygame.K_DOWN and current_direction != UP:
                        current_direction = DOWN
                    elif event.key == pygame.K_LEFT and current_direction != RIGHT:
                        current_direction = LEFT
                    elif event.key == pygame.K_RIGHT and current_direction != LEFT:
                        current_direction = RIGHT
                # Allow quitting even when paused or game over (within this loop)
                if event.key == pygame.K_q:
                     pygame.quit()
                     sys.exit()


        if not game_over:
            if not paused: # <--- New: Only update game logic if not paused
                # --- Move snake ---
                snake_head = snake_body[0]
                new_head = (snake_head[0] + current_direction[0], snake_head[1] + current_direction[1])

                # Insert new snake head
                snake_body.insert(0, new_head)

                # --- Collision detection ---
                # 1. Hit wall
                if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                    game_over = True
                # 2. Hit self
                if new_head in snake_body[1:]:
                    game_over = True

                # 3. Ate food
                if new_head == food_pos:
                    score += 1
                    food_pos = spawn_food(snake_body)
                    # Simply increase speed (optional)
                    if score % 5 == 0 and current_fps < 25 : # Increase speed slightly every 5 points, max 25
                        current_fps += 1
                else:
                    # If food not eaten, remove snake tail, keep length constant
                    snake_body.pop()

            # --- Drawing --- (Always happens, even when paused)
            screen.fill(BLACK) # Clear screen
            # draw_grid() # If grid lines are needed, uncomment this line

            draw_snake(snake_body)
            draw_food(food_pos)
            display_score(score)

            if paused: # <--- New: Display pause message if paused
                display_pause_message()

            if game_over:
                running = False # End current game loop, enter game_over_screen

        pygame.display.flip() # Update the entire screen
        clock.tick(current_fps) # Control game speed

    return score # Return score to game over screen

# --- Main Game Loop ---
if __name__ == "__main__":
    start_screen() # Call start screen before game starts

    while True:
        final_score = main_game() # Start a game session
        game_over_screen(final_score) # Display game over screen and wait for user action
        # If user chooses to restart (R), game_over_screen will return, loop continues, main_game() is called again
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
DOLPHIN_SIZE = 80  # Changed to uppercase for consistency
PADDLE_SPEED = 5
DOLPHIN_SPEED = 7  # Changed to uppercase for consistency
ROSE_HEIGHT = 60 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dolphin Pong")
clock = pygame.time.Clock()

# Create game objects
player = pygame.Rect(50, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(WINDOW_WIDTH - 50 - PADDLE_WIDTH, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
dolphin_x = WINDOW_WIDTH//2
dolphin_y = WINDOW_HEIGHT//2
dolphin_speed_x = DOLPHIN_SPEED
dolphin_speed_y = DOLPHIN_SPEED

try:
    # Load and scale dolphin image
    dolphin_image = pygame.image.load("dolphin.png")
    dolphin_image = pygame.transform.scale(dolphin_image, (DOLPHIN_SIZE, DOLPHIN_SIZE))
    # Load and scale rose image for paddles
    # Load rose image
    rose_image = pygame.image.load("rose.png")
    # Get original dimensions
    original_width = rose_image.get_width()
    original_height = rose_image.get_height()
    # Calculate new width to maintain aspect ratio based on desired height
    aspect_ratio = original_width / original_height
    new_width = int(ROSE_HEIGHT * aspect_ratio)
    # Scale rose while maintaining aspect ratio
    rose_image = pygame.transform.scale(rose_image, (new_width, ROSE_HEIGHT))
    
    # Update paddle width based on rose width
    PADDLE_WIDTH = new_width
    # Recreate the paddle rectangles with new width
    player = pygame.Rect(50, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    opponent = pygame.Rect(WINDOW_WIDTH - 50 - PADDLE_WIDTH, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

except pygame.error:
    print("Couldn't load images. Make sure dolphin.png and rose.png are in the same directory.")
    pygame.quit()
    sys.exit()

dolphin_rect = dolphin_image.get_rect()

# Then in the main game loop, replace these lines:
# pygame.draw.rect(screen, WHITE, player)
# pygame.draw.rect(screen, WHITE, opponent)

# With these lines:
for i in range(3):  # This will draw 3 roses vertically for each paddle
    screen.blit(rose_image, (player.x, player.y + (i * PADDLE_HEIGHT//3)))
    screen.blit(rose_image, (opponent.x, opponent.y + (i * PADDLE_HEIGHT//3)))

dolphin_rect = dolphin_image.get_rect()

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

def move_paddle(paddle, up=True):
    if up and paddle.top > 0:
        paddle.y -= PADDLE_SPEED
    if not up and paddle.bottom < WINDOW_HEIGHT:
        paddle.y += PADDLE_SPEED

def move_dolphin():
    global dolphin_x, dolphin_y, dolphin_speed_x, dolphin_speed_y, player_score, opponent_score
    
    dolphin_x += dolphin_speed_x
    dolphin_y += dolphin_speed_y
    
    # Wall collisions
    if dolphin_y <= 0 or dolphin_y >= WINDOW_HEIGHT - DOLPHIN_SIZE:
        dolphin_speed_y *= -1
    
    # Scoring
    if dolphin_x <= 0:
        opponent_score += 1
        reset_dolphin()
    elif dolphin_x >= WINDOW_WIDTH - DOLPHIN_SIZE:
        player_score += 1
        reset_dolphin()
    
    # Paddle collisions
    dolphin_rect.x = dolphin_x
    dolphin_rect.y = dolphin_y
    
    if dolphin_rect.colliderect(player) or dolphin_rect.colliderect(opponent):
        dolphin_speed_x *= -1.1  # Increase speed slightly on paddle hits

def reset_dolphin():
    global dolphin_x, dolphin_y, dolphin_speed_x, dolphin_speed_y
    dolphin_x = WINDOW_WIDTH//2
    dolphin_y = WINDOW_HEIGHT//2
    dolphin_speed_x = DOLPHIN_SPEED * random.choice((1, -1))
    dolphin_speed_y = DOLPHIN_SPEED * random.choice((1, -1))

def simple_ai():
    if opponent.centery < dolphin_y:
        move_paddle(opponent, False)
    if opponent.centery > dolphin_y:
        move_paddle(opponent, True)

# Game loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            move_paddle(player, True)
        if keys[pygame.K_DOWN]:
            move_paddle(player, False)
        
        # Move dolphin and AI
        move_dolphin()
        simple_ai()
        
        # Drawing
        screen.fill(BLACK)
        
        # Draw roses instead of rectangles for paddles
        for i in range(3):
            screen.blit(rose_image, (player.x, player.y + (i * PADDLE_HEIGHT//3)))
            screen.blit(rose_image, (opponent.x, opponent.y + (i * PADDLE_HEIGHT//3)))
        
        # Draw dolphin
        screen.blit(dolphin_image, (dolphin_x, dolphin_y))
        
        # Draw scores
        player_text = font.render(str(player_score), True, WHITE)
        opponent_text = font.render(str(opponent_score), True, WHITE)
        screen.blit(player_text, (WINDOW_WIDTH//4, 20))
        screen.blit(opponent_text, (3*WINDOW_WIDTH//4, 20))
        
        # Draw center line
        pygame.draw.aaline(screen, WHITE, (WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2, WINDOW_HEIGHT))
        
        pygame.display.flip()
        clock.tick(60)
if __name__ == "__main__":
    main()
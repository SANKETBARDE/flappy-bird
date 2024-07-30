import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 1534
SCREEN_HEIGHT = 830
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
try:
    bird_img = pygame.image.load("bird.png")
    bg_img = pygame.image.load("background.png")
    pipe_img = pygame.image.load("pipe.png")
    bird_img = pygame.transform.scale(bird_img, (100, 100))  # Scale bird image to 100x100
    pipe_img = pygame.transform.scale(pipe_img, (50, 350))  # Scale pipe image to 50x350
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale background image to fit screen
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Game variables
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_y_change = 0
gravity = 0.8  # Increased gravity for a steeper fall
flap_strength = -15  # Increased flap strength for more lift
bg_x = 0
bg_speed = 5
pipe_width = 50  # Adjusted pipe width
pipe_height = 350  # Increased pipe height
bird_height = bird_img.get_height()
pipe_gap = 3 * bird_height  # Reduced initial gap to make it harder
pipe_speed = 8  # Increased pipe speed for a faster challenge
pipe_frequency = 1200  # Reduced frequency for more frequent pipes
pipe_x = SCREEN_WIDTH  # Initial position of the pipe
pipes = []  # List to hold multiple pipes
game_started = False
last_pipe_creation_time = pygame.time.get_ticks()

score = 0
font = pygame.font.SysFont(None, 36)

def check_collision(bird_rect):
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    for top_pipe, bottom_pipe in pipes:
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True
    return False

def update_pipe_gap(score):
    # Decrease the gap more aggressively as the score increases
    if score >= 100:
        return 1.5 * bird_height
    elif score >= 75:
        return 2 * bird_height
    elif score >= 50:
        return 2.5 * bird_height
    elif score >= 25:
        return 3 * bird_height
    else:
        return 4 * bird_height

# Create initial pipes
def create_pipe():
    global last_pipe_creation_time, pipe_gap
    current_time = pygame.time.get_ticks()
    if current_time - last_pipe_creation_time > pipe_frequency:
        last_pipe_creation_time = current_time
        top_pipe_height = random.randint(150, SCREEN_HEIGHT - pipe_gap - 150)
        top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, top_pipe_height)
        
        bottom_pipe_y = top_pipe_height + pipe_gap
        bottom_pipe = pygame.Rect(SCREEN_WIDTH, bottom_pipe_y, pipe_width, SCREEN_HEIGHT - bottom_pipe_y)
        
        pipes.append((top_pipe, bottom_pipe))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_change = flap_strength
                game_started = True
                print("Spacebar pressed, game started")

    if game_started:
        bird_y_change += gravity
        bird_y += bird_y_change

        # Update background position
        bg_x -= bg_speed
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0

        # Move pipes
        for i in range(len(pipes)):
            top_pipe, bottom_pipe = pipes[i]
            top_pipe.x -= pipe_speed
            bottom_pipe.x -= pipe_speed

        # Remove pipes that are off-screen
        pipes = [(top_pipe, bottom_pipe) for top_pipe, bottom_pipe in pipes if top_pipe.x + pipe_width > 0]

        # Create new pipes
        create_pipe()

        # Increment score if the bird has passed a pipe
        for top_pipe, bottom_pipe in pipes:
            if top_pipe.x + pipe_width < bird_x and not top_pipe.x + pipe_width < bird_x - pipe_speed:
                score += 1

        # Update pipe gap based on score
        pipe_gap = update_pipe_gap(score)

    # Draw everything
    # Draw the background
    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + SCREEN_WIDTH, 0))
    
    # Draw pipes
    for top_pipe, bottom_pipe in pipes:
        screen.blit(pipe_img, top_pipe)
        screen.blit(pygame.transform.flip(pipe_img, False, True), bottom_pipe)

    # Draw the bird
    screen.blit(bird_img, (bird_x, bird_y))

    # Draw the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    bird_rect = bird_img.get_rect(topleft=(bird_x, bird_y))

    # Check for collisions
    if game_started and check_collision(bird_rect):
        running = False
        print("Game Over!")

    pygame.display.update()
    pygame.time.Clock().tick(60)

    # Debug information
    print(f"Bird position: ({bird_x}, {bird_y}), Bird change: {bird_y_change}, Background position: ({bg_x})")
     
pygame.quit()
print("Game has ended.")
    
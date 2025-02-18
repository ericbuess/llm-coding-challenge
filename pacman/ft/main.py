import pygame
from . import constants  # Import from the same directory

pygame.init()

# Screen setup
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Basic Pacman")

# Pacman initial position and direction
pacman_x = constants.SCREEN_WIDTH // 2
pacman_y = constants.SCREEN_HEIGHT // 2
pacman_direction_x = 0
pacman_direction_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_direction_x = -1
                pacman_direction_y = 0
            elif event.key == pygame.K_RIGHT:
                pacman_direction_x = 1
                pacman_direction_y = 0
            elif event.key == pygame.K_UP:
                pacman_direction_y = -1
                pacman_direction_x = 0
            elif event.key == pygame.K_DOWN:
                pacman_direction_y = 1
                pacman_direction_x = 0

    # Update Pacman position
    pacman_x += pacman_direction_x * constants.PACMAN_SPEED
    pacman_y += pacman_direction_y * constants.PACMAN_SPEED

    # Keep Pacman within screen bounds
    pacman_x = max(constants.PACMAN_RADIUS, min(pacman_x, constants.SCREEN_WIDTH - constants.PACMAN_RADIUS))
    pacman_y = max(constants.PACMAN_RADIUS, min(pacman_y, constants.SCREEN_HEIGHT - constants.PACMAN_RADIUS))


    # Drawing
    screen.fill(constants.BLACK) # Clear the screen to black
    pygame.draw.circle(screen, constants.YELLOW, (pacman_x, pacman_y), constants.PACMAN_RADIUS) # Draw Pacman

    pygame.display.flip() # Update the display

pygame.quit() 
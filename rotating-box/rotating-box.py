import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball")

# Colors
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Ball properties
ball_radius = 20
ball_x = width // 4
ball_y = height // 2
ball_dx = 5
ball_dy = 5

# Square properties
square_size = 500
square_center = (width // 2, height // 2)
square_rotation = 0
square_speed = 1

clock = pygame.time.Clock()

running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce off window borders
    if ball_x <= 0 or ball_x >= width - ball_radius:
        ball_dx *= -1
    if ball_y <= 0 or ball_y >= height - ball_radius:
        ball_dy *= -1

    # Rotate the square
    square_rotation += square_speed
    square_center = (width // 2, height // 2)

    # Create rotated square surface
    square_surface = pygame.Surface((square_size, square_size))
    square_surface.fill(WHITE)
    
    # Rotate the square
    rotated_square = pygame.transform.rotate(square_surface, square_rotation)
    rotated_rect = rotated_square.get_rect(center=square_center)

    # Check ball collision with square
    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius,
                           2 * ball_radius, 2 * ball_radius)
    
    if not ball_rect.colliderect(rotated_rect):
        # Bounce the ball
        dx = ball_dx
        dy = ball_dy
        
        # Calculate distance from square edges in rotated coordinates
        point = (ball_x - rotated_rect.x, ball_y - rotated_rect.y)
        angle = math.radians(square_rotation)
        
        # Rotate point to square's coordinate system
        rotated_point_x = (point[0] * math.cos(angle) + point[1] * math.sin(angle))
        rotated_point_y = (-point[0] * math.sin(angle) + point[1] * math.cos(angle))
        
        if rotated_point_x < -ball_radius:
            ball_dx *= -1
        elif rotated_point_x > square_size + ball_radius:
            ball_dx *= -1
        if rotated_point_y < -ball_radius:
            ball_dy *= -1
        elif rotated_point_y > square_size + ball_radius:
            ball_dy *= -1

    # Clear screen
    window.fill((0, 0, 0))

    # Draw the rotating square
    window.blit(rotated_square, rotated_rect)

    # Draw the ball
    pygame.draw.circle(window, YELLOW, (int(ball_x), int(ball_y)), ball_radius)

    # Update display
    pygame.display.flip()

    # Set frame rate
    clock.tick(60)

pygame.quit()


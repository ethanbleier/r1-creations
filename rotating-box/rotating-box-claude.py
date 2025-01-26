import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 800
FPS = 60
SQUARE_SIZE = 400
BALL_RADIUS = 15
ROTATION_SPEED = 0.5  # degrees per frame
BALL_SPEED = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Square")
clock = pygame.time.Clock()

# Ball properties
ball_pos = np.array([WIDTH/2, HEIGHT/2], dtype=float)
ball_vel = np.array([BALL_SPEED, BALL_SPEED], dtype=float)

# Square properties
square_angle = 0
square_center = np.array([WIDTH/2, HEIGHT/2])

def rotate_point(point, center, angle):
    """Rotate a point around a center by given angle in degrees"""
    angle_rad = math.radians(angle)
    translated = point - center
    rotated = np.array([
        translated[0] * math.cos(angle_rad) - translated[1] * math.sin(angle_rad),
        translated[0] * math.sin(angle_rad) + translated[1] * math.cos(angle_rad)
    ])
    return rotated + center

def get_square_vertices():
    """Get the four vertices of the rotated square"""
    half_size = SQUARE_SIZE / 2
    vertices = [
        np.array([-half_size, -half_size]),
        np.array([half_size, -half_size]),
        np.array([half_size, half_size]),
        np.array([-half_size, half_size])
    ]
    return [rotate_point(square_center + v, square_center, square_angle) for v in vertices]

def get_square_lines():
    """Get the four lines of the square as (start_point, end_point, normal)"""
    vertices = get_square_vertices()
    lines = []
    for i in range(4):
        start = vertices[i]
        end = vertices[(i + 1) % 4]
        # Calculate normalized normal vector (perpendicular to the line, pointing inward)
        line_vec = end - start
        normal = np.array([-line_vec[1], line_vec[0]])
        normal = normal / np.linalg.norm(normal)
        if i in (1, 2):  # Flip normal for right and bottom edges
            normal = -normal
        lines.append((start, end, normal))
    return lines

def check_collision():
    """Check for collision between ball and square sides"""
    lines = get_square_lines()
    for start, end, normal in lines:
        # Vector from line start to ball center
        to_ball = ball_pos - start
        # Vector of the line
        line_vec = end - start
        # Project ball's position onto the line
        line_length = np.linalg.norm(line_vec)
        line_normalized = line_vec / line_length
        projection_length = np.dot(to_ball, line_normalized)
        
        # Check if ball is near the line segment
        if 0 <= projection_length <= line_length:
            # Distance from line to ball center
            distance = abs(np.dot(to_ball, normal))
            if distance < BALL_RADIUS:
                # Reflect velocity about the normal
                ball_vel[:] = ball_vel - 2 * np.dot(ball_vel, normal) * normal
                # Move ball out of collision
                ball_pos[:] = ball_pos + (BALL_RADIUS - distance) * normal

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Update
    square_angle += ROTATION_SPEED
    ball_pos += ball_vel
    check_collision()

    # Draw
    screen.fill(BLACK)
    
    # Draw square
    vertices = get_square_vertices()
    pygame.draw.polygon(screen, WHITE, vertices, 2)
    
    # Draw ball
    pygame.draw.circle(screen, YELLOW, ball_pos.astype(int), BALL_RADIUS)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

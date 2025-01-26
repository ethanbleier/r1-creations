import pygame as pg
from math import sin, cos, radians

# Initialize
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

# Square properties
side_length = min(800, 600) - 40  # Make room for ball
square_center = (400, 300)
square_rotation = 0

# Ball properties
ball_pos = [350, 270]
ball_radius = 10
dx, dy = 1, 1  # Velocity components

while True:
    screen.fill("black")

    # Update rotation and position
    square_rotation += 1  # Slowly rotate the square
    angle = radians(square_rotation)
    
    # Get rotated ball position for collision detection
    x, y = ball_pos
    rotated_x = (x - square_center[0]) * cos(angle) - (y - square_center[1]) * sin(angle) + square_center[0]
    rotated_y = (x - square_center[0]) * sin(angle) + (y - square_center[1]) * cos(angle) + square_center[1]

    # Update ball position
    ball_pos[0] += dx
    ball_pos[1] += dy

    # Check collisions with square edges using rotated coordinates
    if (rotated_x < 40 or rotated_x > side_length - 40):
        dx *= -1
    if (rotated_y < 40 or rotated_y > side_length - 40):
        dy *= -1

    # Draw objects
    color = "yellow"
    pg.draw.rect(screen, color, (square_center[0] - side_length//2 + square_rotation,
                                 square_center[1] - side_length//2,
                                 side_length, side_length))
    pg.draw.circle(screen, "white", [int(x) for x in ball_pos], ball_radius)

    # Handle window close
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    clock.tick(60)
    pg.display.flip()


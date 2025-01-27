import pygame as pg
from math import sin, cos, radians

# Initialize
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

# Square properties
side_length = 500  # Reduced size for better visibility
square_center = (400, 300)
square_rotation = 0
square_surface = pg.Surface((side_length, side_length), pg.SRCALPHA)

# Ball properties
ball_pos = [400 + side_length//4, 300]  # Start inside the square
ball_radius = 10
dx, dy = 3, 2  # Reduced initial velocity

while True:
    screen.fill("black")

    # Update rotation
    square_rotation += 1
    angle = radians(square_rotation)
    
    # Rotate square surface
    rotated_square = pg.transform.rotate(square_surface, square_rotation)
    rect = rotated_square.get_rect(center=square_center)
    
    # Draw white outlined square
    square_surface.fill((0, 0, 0, 0))  # Clear with transparency
    pg.draw.rect(square_surface, "white", (0, 0, side_length, side_length), width=2)
    screen.blit(rotated_square, rect.topleft)

    # Update ball position with collision detection
    ball_pos[0] += dx
    ball_pos[1] += dy

    # Transform ball coordinates to square's rotated system
    x, y = ball_pos[0] - square_center[0], ball_pos[1] - square_center[1]
    rotated_x = x * cos(-angle) - y * sin(-angle)
    rotated_y = x * sin(-angle) + y * cos(-angle)
    
    # Check collisions with square boundaries (accounting for rotation)
    if abs(rotated_x) > (side_length//2 - ball_radius * 2):
        dx *= -1
    if abs(rotated_y) > (side_length//2 - ball_radius * 2):
        dy *= -1

    # Draw yellow ball
    pg.draw.circle(screen, "yellow", [int(x) for x in ball_pos], ball_radius)

    # Handle window close
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    clock.tick(60)
    pg.display.flip()


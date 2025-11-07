import math
import random  # For generating random values used in asteroid shapes and positions

def accelerate(acceleration, velocity, FRICTION):
    # Apply friction and update velocity
    acceleration += velocity * FRICTION
    velocity += acceleration
    return (acceleration, velocity)

def xy_movefromangle(angle, speed, app):
    # Calculate movement in x and y directions based on angle and speed
    i = int(angle) % 360
    x_movement = app.SIN[i] * speed
    y_movement = app.COS[i] * speed
    return x_movement, y_movement

def change_vertices(matrix, x, y):
    # Shift all vertices of a polygon by (x, y)
    return [(vx + x, vy + y) for vx, vy in matrix]

def create_asteroid_poly():
    # Generate a random, irregular asteroid polygon shape
    radius = random.randint(2, 5)
    corners = random.randint(7, 10)

    # Create slightly varied radii for irregular edges
    radii = [radius + random.uniform(-1.0, 1.0) for _ in range(corners)]

    # Evenly space corners around a circle
    angles = [2 * math.pi * i / corners for i in range(corners)]

    # Convert polar coordinates to (x, y) points, scaled up for visibility
    points = []
    for angle, r in zip(angles, radii):
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x * 10, y * 10))

    return points

def parallax_movement(a, b, factor):
    # Simulate depth by scaling movement speed using a parallax factor
    return (a / (1 + b) ** factor) / 20

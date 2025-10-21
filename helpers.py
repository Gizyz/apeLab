import math
import random

def accelerate(acceleration, velocity, FRICTION):
    acceleration += velocity * FRICTION
    velocity += acceleration
    return (acceleration, velocity)

def xy_movefromangle(angle, speed, app):
    i = int(angle) % 360
    x_movement = app.SIN[i] * speed
    y_movement = app.COS[i] * speed
    return x_movement, y_movement

def change_vertices(matrix, x, y):
    return [(vx + x, vy + y) for vx, vy in matrix]

def create_asteroid_poly():
    radius = random.randint(2, 5)
    corners = random.randint(7, 10)

    radii = [radius + random.uniform(-1.0, 1.0) for _ in range(corners)]

    angles = [2* math.pi * i / corners for i in range(corners)]

    points = []
    for angle, r in zip(angles, radii):
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x *10, y * 10))

    return points

def parallax_movement(a, b, factor):
    return (a / (1+b) ** factor)/20


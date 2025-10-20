import math
import random

def accelerate(acceleration, velocity, FRICTION):
    acceleration += velocity * FRICTION
    velocity += acceleration
    return (acceleration, velocity)

def xy_movefromangle(angle, speed):
    x_movement = math.sin(math.radians(angle)) * speed
    y_movement = math.cos(math.radians(angle)) * speed
    return x_movement, y_movement

def change_vertices(matrix, x, y):
    new_pts = []
    for vx, vy in matrix:
        x -= vx
        y -= vy
        new_pts.append((x, y))
    return new_pts

def create_asteroid_poly():
    list=[]
    radius = random.randint(2, 5)
    corners = random.randint(7, 10)

    radii = [radius + random.uniform(-1.0, 1.0) for _ in range(corners)]


    C = 2*math.pi*radius
    step_size = C / corners
    angle = step_size/radius

    angles = [2* math.pi * i / corners for i in range(corners)]

    points = []
    for angle, r in zip(angles, radii):
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x *10, y * 10))
    for i in range(corners):
        x = radius * math.cos(angle * i) + random.randint(-1, 1)
        y = radius * math.sin(angle * i) + random.randint(-1, 1)
        list.append((x*10,y*10))

    return points
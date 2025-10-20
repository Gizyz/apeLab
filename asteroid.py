from helpers import change_vertices, xy_movefromangle
import random

class Asteroid:
    def __init__(self, app, poly_points, speed, angle):
        self.x = random.randint(0, app.width)
        self.y = 0
        self.points = change_vertices(poly_points, self.x, self.y)

        self.angle = angle
        self.speed = speed

    def move(self):
        x_movement, y_movement = xy_movefromangle(self.angle, self.speed)
        self.x -= x_movement
        self.y -= y_movement
        for i in range(len(self.points)):
            (x, y) = self.points[i]
            x -= x_movement
            y -= y_movement
            self.points[i] = (x, y)

    def draw(self, canvas):
        canvas.create_polygon(self.points, outline='black')
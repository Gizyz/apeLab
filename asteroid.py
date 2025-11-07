from helpers import change_vertices, xy_movefromangle  # Import helper functions for geometry and movement
import random  # Import random module for generating random positions

class Asteroid:
    def __init__(self, app, poly_points, speed, angle):
        # Set a random starting x position and start y position at the top of the screen
        self.x = random.randint(0, app.width)
        self.y = 0
        
        # Shift the asteroid's polygon points to the initial position
        self.points = change_vertices(poly_points, self.x, self.y)

        # Store references to app and motion properties
        self.app = app
        self.angle = angle
        self.speed = speed

    def move(self):
        # Calculate movement distance in x and y directions based on angle and speed
        x_movement, y_movement = xy_movefromangle(self.angle, self.speed, self.app)
        
        # Update asteroid’s central position
        self.x -= x_movement
        self.y -= y_movement
        
        # Update each vertex position of the asteroid’s polygon
        for i in range(len(self.points)):
            (x, y) = self.points[i]
            x -= x_movement
            y -= y_movement
            self.points[i] = (x, y)

    def draw(self, canvas):
        # Draw the asteroid shape on the canvas as a white-outlined polygon
        canvas.create_polygon(self.points, outline='white')

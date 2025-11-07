from helpers import parallax_movement  # Import helper for parallax depth effect
import random  # Used to randomize star positions and depth

class Star():
    def __init__(self, size, width, height):
        # Initialize a star with random position and distance
        self.orig_x = random.randint(0, width)
        self.orig_y = random.randint(0, height)

        self.x = self.orig_x
        self.y = self.orig_y
        
        self.width = width
        self.height = height
        self.size = size  # Visual size of the star (for drawing)

        # Position of the ship (used for parallax movement)
        self.ship_x = 0
        self.ship_y = 0

        # Random distance factor: farther stars move less
        self.dist = random.randint(0, 5)

    def offset_calc(self):
        # Calculate parallax offset based on ship position
        x_offset = self.ship_x - self.width / 2
        y_offset = self.ship_y - self.height / 2

        # Apply parallax effect using helper function
        self.x = self.orig_x + parallax_movement(x_offset, self.dist, 1.5)
        self.y = self.orig_y + parallax_movement(y_offset, self.dist, 1.5)

    def draw(self, canvas):
        # Update position and draw star as a small white square
        self.offset_calc()
        canvas.create_rectangle(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            fill='white'
        )

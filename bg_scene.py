from helpers import parallax_movement
import random

class Star():
    def __init__(self, size, width, height):
        self.orig_x = random.randint(0, width)
        self.orig_y = random.randint(0, height)

        self.x = self.orig_x
        self.y = self.orig_y
        
        self.width = width
        self.height = height
        
        self.size = size

        self.ship_x = 0
        self.ship_y = 0
        self.dist = random.randint(0,5)

    def offset_calc(self):
        x_offset = self.ship_x - self.width/2
        y_offset = self.ship_y - self.height/2

        self.x = self.orig_x + parallax_movement(x_offset, self.dist, 1.5)
        self.y = self.orig_y + parallax_movement(y_offset, self.dist, 1.5)

    def draw(self, canvas):
        self.offset_calc()

        canvas.create_rectangle(self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size, fill='white')





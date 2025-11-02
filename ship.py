from uib_inf100_graphics.helpers import scaled_image
from PIL import Image
from helpers import xy_movefromangle, accelerate


class Projectile:
    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.points = [(self.x-2, self.y-2), (self.x+2, self.y+2)]

        self.angle = angle
        self.speed = speed
        
    
    def move(self, app):
        x_movement, y_movement = xy_movefromangle(self.angle, self.speed, app)
        self.x -= x_movement
        self.y -= y_movement
        self.points = [(self.x-2, self.y-2), (self.x+2, self.y+2)]

    def draw(self, canvas):
        canvas.create_rectangle(self.x-2, self.y-2, self.x+2, self.y+2, fill='red')

class Ship:
    def __init__(self, x, y, speed, delay):
        self.img = scaled_image(Image.open("./ship2.png"), 2)

        self.x = x
        self.y = y
        self.speed = speed
        self.angle = 0
        self.direction = 0

        self.acceleration = 0
        self.velocity = 0
        self.FRICTION = -0.2

        self.rotacc = 0
        self.rot_left = 0
        self.rot_right = 0
        self.rotvel = 0

        self.shooting = False
        self.fire_delay = delay
        self.fire_timer = 0
        self.bullets=[]

        self.img_cache = {}
        for angle in range(361):
            self.img_cache[angle] = self.img.rotate(angle)

    def key_press(self, app):
        if "w" in app.key_presses:
            self.acceleration = app.ship.speed

        if "a" in app.key_presses:
            self.rot_left = 5

        if "d" in app.key_presses:
            self.rot_right = -5


        self.shooting = "space" in app.key_presses




    def shoot(self, app):
        if self.fire_timer <= 0:
            self.bullets.append(Projectile(self.x, self.y, app.bullet_speed, self.angle))
            self.fire_timer = self.fire_delay
            self.bullets = [ b for b in self.bullets 
                            if 0 <= b.x <= app.width and 0 <= b.y <= app.height]


    def turn(self):
        # Apply left and right rotation
        self.rotacc = self.rot_left + self.rot_right

        # Apply friction to rotation (may need some fine-tuning)
        (self.rotacc, self.rotvel) = accelerate(self.rotacc, self.rotvel, -0.2)
        self.rotacc = self.rotvel + self.rotacc * 0.5
        
        # Ensure the angle stays within bounds [0, 360)
        self.angle += self.rotacc
        self.angle %= 360

        self.rot_left = 0
        self.rot_right = 0
        self.rotacc = 0

    def move(self, app):
        self.turn()

        #print(f"Rotation (angle): {self.angle:.2f}, rotacc: {self.rotacc}")  # Debug line
        
        if self.shooting:
            self.shoot(app)

        if self.fire_timer > 0:
            self.fire_timer -= 1


        (self.acceleration, self.velocity) = accelerate(self.acceleration, self.velocity, self.FRICTION)
        self.acceleration = self.velocity + self.acceleration, 2 * 0.5

        if self.velocity > 0:
            x_movement, y_movement = xy_movefromangle(self.angle, self.velocity, app)
            self.x = self.x - x_movement
            self.y = self.y - y_movement

            #print((self.x, self.y))

    def draw(self, canvas):
        rotated_ship =  self.img_cache[int(self.angle) % 360]

        canvas.create_image(self.x, self.y, pil_image=rotated_ship)
        for bullet in self.bullets:
            bullet.draw(canvas)
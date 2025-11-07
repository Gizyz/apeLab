from uib_inf100_graphics.helpers import scaled_image  # Import image scaling helper
from PIL import Image  # Import Pillow for image handling
from helpers import xy_movefromangle, accelerate  # Import movement and acceleration helpers


class Projectile:
    def __init__(self, x, y, speed, angle):
        # Initialize projectile position and motion
        self.x = x
        self.y = y
        self.points = [(self.x-2, self.y-2), (self.x+2, self.y+2)]  # Small rectangle shape

        self.angle = angle
        self.speed = speed
        
    def move(self, app):
        # Update projectile position based on angle and speed
        x_movement, y_movement = xy_movefromangle(self.angle, self.speed, app)
        self.x -= x_movement
        self.y -= y_movement
        self.points = [(self.x-2, self.y-2), (self.x+2, self.y+2)]  # Update shape coordinates

    def draw(self, canvas):
        # Draw a small red square for the projectile
        canvas.create_rectangle(self.x-2, self.y-2, self.x+2, self.y+2, fill='red')


class Ship:
    def __init__(self, x, y, speed, delay):
        # Load and scale ship image
        self.img = scaled_image(Image.open("./ship2.png"), 2)

        # Ship position and motion parameters
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = 0
        self.direction = 0

        # Movement and friction settings
        self.acceleration = 0
        self.velocity = 0
        self.FRICTION = -0.2

        # Rotation-related attributes
        self.rotacc = 0
        self.rot_left = 0
        self.rot_right = 0
        self.rotvel = 0

        # Shooting control
        self.shooting = False
        self.fire_delay = delay
        self.fire_timer = 0
        self.bullets = []

        # Pre-rotate and cache all possible ship images for smoother rotation
        self.img_cache = {}
        for angle in range(361):
            self.img_cache[angle] = self.img.rotate(angle)

    def key_press(self, app):
        # Check pressed keys and adjust ship control accordingly
        if "w" in app.key_presses:
            self.acceleration = app.ship.speed

        if "a" in app.key_presses:
            self.rot_left = 5

        if "d" in app.key_presses:
            self.rot_right = -5

        # Enable shooting when space is pressed
        self.shooting = "space" in app.key_presses

    def shoot(self, app):
        # Fire a bullet if delay timer allows
        if self.fire_timer <= 0:
            self.bullets.append(Projectile(self.x, self.y, app.bullet_speed, self.angle))
            self.fire_timer = self.fire_delay
            # Remove bullets that go off-screen
            self.bullets = [b for b in self.bullets if 0 <= b.x <= app.width and 0 <= b.y <= app.height]

    def turn(self):
        # Combine left/right rotation input
        self.rotacc = self.rot_left + self.rot_right

        # Apply acceleration and friction to rotation
        (self.rotacc, self.rotvel) = accelerate(self.rotacc, self.rotvel, -0.2)
        self.rotacc = self.rotvel + self.rotacc * 0.5
        
        # Keep ship angle between 0–359 degrees
        self.angle += self.rotacc
        self.angle %= 360

        # Reset rotation values each frame
        self.rot_left = 0
        self.rot_right = 0
        self.rotacc = 0

    def move(self, app):
        # Handle rotation updates
        self.turn()

        # Fire bullets when shooting
        if self.shooting:
            self.shoot(app)

        # Reduce fire cooldown timer
        if self.fire_timer > 0:
            self.fire_timer -= 1

        # Update acceleration and velocity with friction applied
        (self.acceleration, self.velocity) = accelerate(self.acceleration, self.velocity, self.FRICTION)
        self.acceleration = self.velocity + self.acceleration, 2 * 0.5  # Apply simple motion formula

        # Move ship if velocity is positive
        if self.velocity > 0:
            x_movement, y_movement = xy_movefromangle(self.angle, self.velocity, app)
            self.x -= x_movement
            self.y -= y_movement

    def draw(self, canvas):
        # Retrieve pre-rotated image for current angle
        rotated_ship = self.img_cache[int(self.angle) % 360]

        # Draw ship image and its active bullets
        canvas.create_image(self.x, self.y, pil_image=rotated_ship)
        for bullet in self.bullets:
            bullet.draw(canvas)
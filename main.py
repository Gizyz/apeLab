def app_started(app):
    # app_started: kjøres én gang når programmet starter.
    # Her oppretter vi variabler i `app`` og gir dem initiell verdi.
    app.timer_delay = 16
    app.key_presses = set()
    app.ship = Ship(app.width/2, app.height/2, 4)
    app.projectile = []

def key_pressed(app, event):
    app.key_presses.add(event.key)

def key_released(app, event):
    app.key_presses.discard(event.key)

def redraw_all(app, canvas):
    app.ship.draw(canvas)

def timer_fired(app):
    app.ship.acceleration = 0
    app.ship.rotacc = 0

    app.ship.key_press(app)
    app.ship.move()


def accelerate(acceleration, velocity, FRICTION):
    acceleration += velocity * FRICTION
    velocity += acceleration
    return (acceleration, velocity)

def xy_movefromangle(angle, speed):
    x_movement = math.sin(math.radians(angle)) * speed
    y_movement = math.cos(math.radians(angle)) * speed
    return x_movement, y_movement

class Projectile:
    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
    
    def move(self):
        x_movement, y_movement = xy_movefromangle(self.angle, self.speed)
        self.x -= x_movement
        self.y -= y_movement

    def draw(self, canvas):
        self.move()
        canvas.create_rectangle(self.x-2, self.y-2, self.x+2, self.y+2, fill='black')

class Ship:
    def __init__(self, x, y, speed):
        self.img = scaled_image(Image.open("./ship.png"), 2)

        self.x = x
        self.y = y
        self.speed = speed
        self.angle = 0
        self.direction = 0

        self.acceleration = 0
        self.velocity = 0
        self.FRICTION = -0.2

        self.rotacc = 0
        self.rotvel = 0

        self.fire_delay = 2
        self.fire_timer = 0
        self.bullets=[]

    def key_press(self, app):
        if "Left" in app.key_presses:
            self.rotacc = 15
            self.rotvel = 0

        elif "Right" in app.key_presses:
            self.rotacc = -15
            self.rotvel = 0

        if "Up" in app.key_presses:
            self.acceleration = app.ship.speed
            self.direction = -1

        elif "Down" in app.key_presses:
            self.acceleration = app.ship.speed
            self.direction = 1

        if "Space" in app.key_presses and self.fire_timer <= 0:
            self.shoot()
            self.fire_timer = self.fire_delay

    def shoot(self):
        self.bullets.append(Projectile(self.x, self.y, 20, self.angle))

        if len(self.bullets) > 10:
             self.bullets.pop(0)


    def turn(self):
        (self.rotacc, self.rotvel) = accelerate(self.rotacc, self.rotvel, -0.2)
        self.rotacc = self.rotvel + round(self.rotacc, 2) * 0.5

        self.angle += self.rotacc
        self.angle %= 360

    def move(self):
        if self.fire_timer > 0:
            self.fire_timer -= 1
        self.turn()

        (self.acceleration, self.velocity) = accelerate(self.acceleration, self.velocity, self.FRICTION)
        self.acceleration = self.velocity + round(self.acceleration, 2) * 0.5

        if self.velocity > 0:
            x_movement, y_movement = xy_movefromangle(self.angle, self.velocity)
            self.x += round(x_movement, 2) * self.direction
            self.y += round(y_movement, 2) * self.direction


    def draw(self, canvas):
        rotated_ship = self.img.rotate(self.angle)

        canvas.create_image(self.x, self.y, pil_image=rotated_ship)
        for projectil in self.bullets:
            projectil.draw(canvas)


if __name__ == '__main__':
    import math
    import time
    from uib_inf100_graphics.event_app import run_app
    from uib_inf100_graphics.helpers import scaled_image
    from PIL import Image

    run_app(width=800, height=600)
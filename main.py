from uib_inf100_graphics.helpers import scaled_image


def app_started(app):
    # app_started: kjøres én gang når programmet starter.
    # Her oppretter vi variabler i `app`` og gir dem initiell verdi.
    app.timer_delay = 50
    app.key_presses = set()
    app.ship = Ship(app.width/2, app.height/2, 8)

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


class Ship:
    def __init__(self, x, y, speed):
        self.img = Image.open("./ship.png")

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
    def key_press(self, app):
        if "Left" in app.key_presses:
            app.ship.rotacc = 15
            app.ship.rotvel = 0

        elif "Right" in app.key_presses:
            app.ship.rotacc = -15
            app.ship.rotvel = 0

        if "Up" in app.key_presses:
            app.ship.acceleration = app.ship.speed
            app.ship.direction = -1

        elif "Down" in app.key_presses:
            app.ship.acceleration = app.ship.speed
            app.ship.direction = 1

    def turn(self):
        (self.rotacc, self.rotvel) = accelerate(self.rotacc, self.rotvel, -0.2)
        self.rotacc = self.rotvel + round(self.rotacc, 2) * 0.5

        self.angle += self.rotacc
        self.angle %= 360
        print(self.angle)

    def move(self):
        self.turn()

        (self.acceleration, self.velocity) = accelerate(self.acceleration, self.velocity, self.FRICTION)
        self.acceleration = self.velocity + round(self.acceleration, 2) * 0.5

        if self.velocity > 0:
            x_movement = math.sin(math.radians(self.angle)) * self.velocity
            y_movement = math.cos(math.radians(self.angle)) * self.velocity

            self.x += round(x_movement, 2) * self.direction
            self.y += round(y_movement, 2) * self.direction


    def draw(self, canvas):
        scaled_ship = scaled_image(self.img, 2)
        rotated_ship = scaled_ship.rotate(self.angle)

        canvas.create_image(self.x, self.y, pil_image=rotated_ship)


if __name__ == '__main__':
    import math
    from uib_inf100_graphics.event_app import run_app
    from uib_inf100_graphics.helpers import scaled_image
    from PIL import Image

    run_app(width=800, height=600)
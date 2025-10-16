def app_started(app):
    # app_started: kjøres én gang når programmet starter.
    # Her oppretter vi variabler i `app`` og gir dem initiell verdi.
    app.timer_delay = 16
    app.key_presses = set()
    app.ship = Ship(app.width/2, app.height/2, 4)
    app.asteroids = []

def key_pressed(app, event):
    app.key_presses.add(event.key.lower())

def key_released(app, event):
    app.key_presses.discard(event.key.lower())

def redraw_all(app, canvas):
    app.ship.draw(canvas)
    for asteroid in app.asteroids:
        asteroid.draw(canvas)

def timer_fired(app):
    import random
    app.ship.acceleration = 0
    app.ship.rotacc = 0

    app.ship.key_press(app)
    app.ship.move(app)

    if len(app.asteroids) < 10:
        app.asteroids.append(Asteroid(app, create_asteroid_poly(), random.randint(2,8), random.randint(180, 190)))

    offset = 0
    for i in range(len(app.asteroids)):
        index = i-offset
        app.asteroids[index].move()
        if app.asteroids[index].x < -100 or app.asteroids[index].x > 100+app.width or app.asteroids[index].y < -100 or app.asteroids[index].y > 100+app.height:
            app.asteroids.pop(index)
            offset += 1

    
def create_asteroid_poly():
    import random
    list=[]
    radius = random.randint(4, 7)
    corners = random.randint(5, 10)

    C = 2*math.pi*radius
    step_size = C / corners
    angle = step_size/radius

    for i in range(corners):
        x = radius * math.cos(angle * i) + random.randint(0, 1)
        y = radius * math.sin(angle * i) + random.randint(0, 1)
        list.append((x*10,y*10))

    return list

def accelerate(acceleration, velocity, FRICTION):
    acceleration += velocity * FRICTION
    velocity += acceleration
    return (acceleration, velocity)

def xy_movefromangle(angle, speed):
    x_movement = math.sin(math.radians(angle)) * speed
    y_movement = math.cos(math.radians(angle)) * speed
    return x_movement, y_movement

def change_vertices(matrix, x, y):
    for i in range(len(matrix)):
        x = x-matrix[i][0]
        y = y-matrix[i][1]
        matrix[i] = (x, y)
    return matrix

class Asteroid:
    def __init__(self, app, poly_points, speed, angle):
        import random
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
        canvas.create_rectangle(self.x-2, self.y-2, self.x+2, self.y+2, fill='black')

class Ship:
    def __init__(self, x, y, speed):
        self.img = scaled_image(Image.open("apeLab/ship.png"), 2)

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
        self.fire_delay = 2
        self.fire_timer = 0
        self.bullets=[]

        self.img_cache = {}
        for angle in range(361):
            self.img_cache[angle] = self.img.rotate(angle)

    def key_press(self, app):
        print(app.key_presses)
        if "w" in app.key_presses:
            self.acceleration = app.ship.speed

        if "a" in app.key_presses:
            self.rot_left = 5

        if "d" in app.key_presses:
            self.rot_right = -5


        self.shooting = "space" in app.key_presses




    def shoot(self, app):
        if self.fire_timer <= 0:
            self.bullets.append(Projectile(self.x, self.y, 30, self.angle))
            self.fire_timer = self.fire_delay
            for bullet in self.bullets:
                if bullet.x < 0 or bullet.x > app.width or bullet.y < 0 or bullet.y > app.height:
                    self.bullets.pop(0)


    def turn(self):
        # Apply left and right rotation
        self.rotacc = self.rot_left + self.rot_right

        # Apply friction to rotation (may need some fine-tuning)
        (self.rotacc, self.rotvel) = accelerate(self.rotacc, self.rotvel, -0.2)
        self.rotacc = self.rotvel + round(self.rotacc, 2) * 0.5
        
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
        self.acceleration = self.velocity + round(self.acceleration, 2) * 0.5

        if self.velocity > 0:
            x_movement, y_movement = xy_movefromangle(self.angle, self.velocity)
            self.x -= round(x_movement, 2)
            self.y -= round(y_movement, 2)


    def draw(self, canvas):
        rotated_ship =  self.img_cache[int(self.angle) % 360]

        canvas.create_image(self.x, self.y, pil_image=rotated_ship)
        for bullet in self.bullets:
            bullet.move()
            bullet.draw(canvas)


if __name__ == '__main__':
    import math
    import time
    from uib_inf100_graphics.event_app import run_app
    from uib_inf100_graphics.helpers import scaled_image
    from PIL import Image

    run_app(width=800, height=600, title="ASTEROIDS!",)
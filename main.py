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

    if len(app.asteroids) < 20:
        app.asteroids.append(Asteroid(app, create_asteroid_poly(), random.randint(2,8), random.randint(180, 190)))

    for i in reversed(range(len(app.asteroids))):
        app.asteroids[i].move()
        if app.asteroids[i].x < -100 or app.asteroids[i].x > 100+app.width or app.asteroids[i].y < -100 or app.asteroids[i].y > 100+app.height:
            app.asteroids.pop(i)

        for j in reversed(range(len(app.ship.bullets))):
            if GJK(app.ship.bullets[j].points, app.asteroids[i].points):
                app.asteroids.pop(i)
                app.ship.bullets.pop(j)
                break



class Polygon:
    def __init__(self, vertices):
        self.vertex = vertices
        self.edges = []
        for i in range(len(vertices)):
            x = vertices[i][0] - vertices[i-1][0]
            y = vertices[i][1] - vertices[i-1][1]
            self.edges.append((x, y))

if __name__ == '__main__':
    import math
    import random

    from uib_inf100_graphics.event_app import run_app
    from uib_inf100_graphics.helpers import scaled_image
    from collision import GJK
    from ship import Ship
    from asteroid import Asteroid
    from helpers import create_asteroid_poly
    run_app(width=800, height=600, title="ASTEROIDS!")
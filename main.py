def app_started(app):
    # app_started: kjøres én gang når programmet starter.
    # Her oppretter vi variabler i `app`` og gir dem initiell verdi.
    app.mouse_x = 0
    app.mouse_y = 0
    
    #Upgradables
    app.cash = 90000
    app.bullet_speed = 2
    app.bullet_damage = 2
    app.fire_rate = 20
    app.health = 10
    app.asteroid_count = 1
    app.ship_speed = 1
    
    
    #var inits
    app.state = 'game'
    app.timer_delay = 16
    app.key_presses = set()
    app.ship = Ship(app.width/2, app.height/2, app.ship_speed, app.fire_rate)
    app.asteroids = []
    app.stars = []
    app.btns = create_menu()

    app.SIN = [math.sin(math.radians(a)) for a in range(360)]
    app.COS = [math.cos(math.radians(a)) for a in range(360)]

    for _ in range(20):
        app.stars.append(Star(2, app.width, app.height))

def size_changed(app):
    app.stars = []
    for _ in range(20):
        app.stars.append(Star(2, app.width, app.height))

def key_pressed(app, event):
    app.key_presses.add(event.key.lower())

def key_released(app, event):
    app.key_presses.discard(event.key.lower())
    
def mouse_moved(app, event):
    if app.state == 'menu':
        app.mouse_x = event.x
        app.mouse_y = event.y
        
def mouse_pressed(app, event):
    if app.state == 'menu':
        for btn in app.btns:
            btn.click(app, event.x, event.y)
    
def redraw_all(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill='black')
    for star in app.stars:
        if app.state == 'game':
            star.ship_x = app.ship.x
            star.ship_y = app.ship.y
        else:
            star.ship_x = app.mouse_x
            star.ship_y = app.mouse_y
        star.draw(canvas)
    
    if app.state == 'game':
        app.ship.draw(canvas)
        for asteroid in app.asteroids:
            asteroid.draw(canvas)
            
    elif app.state == 'menu':
        for btn in app.btns:
            btn.draw(canvas)  
        canvas.create_rectangle(app.width/2 - 50, 10, app.width/2 + 50, 50, fill='black', outline='white')
        canvas.create_text(app.width/2, 30, text=f'{app.cash}$', fill='white', font=('Courier new', 15, ''))   

def timer_fired(app):
    if app.state == 'game':
        game_ticks(app)

def game_ticks(app):
    app.ship.acceleration = 0
    app.ship.rotacc = 0

    app.ship.key_press(app)
    app.ship.move(app)

    if len(app.asteroids) < app.asteroid_count:
        app.asteroids.append(Asteroid(app, create_asteroid_poly(), random.randint(2,8), random.randint(180, 190)))

    for bullet in app.ship.bullets:
        bullet.move(app)

    to_remove_asteroids = set()
    to_remove_bullets = set()
    for i in reversed(range(len(app.asteroids))):
        app.asteroids[i].move()
        ship_points = [(app.ship.x-5, app.ship.y-5), (app.ship.x+5, app.ship.y+5)]
        if GJK(ship_points, app.asteroids[i].points):
            app.state = 'menu'

        if app.asteroids[i].x < -100 or app.asteroids[i].x > 100+app.width or app.asteroids[i].y < -100 or app.asteroids[i].y > 100+app.height:
            to_remove_asteroids.add(i)

        for j in reversed(range(len(app.ship.bullets))):
            if abs(app.ship.bullets[j].x - app.asteroids[i].x) > 100 or abs(app.ship.bullets[j].y - app.asteroids[i].y) > 100:
                continue  # skip GJK

            if GJK(app.ship.bullets[j].points, app.asteroids[i].points):
                to_remove_asteroids.add(i)
                to_remove_bullets.add(j)
                
                app.cash += 10
                break
            


    app.asteroids = [a for k, a in enumerate(app.asteroids) if k not in to_remove_asteroids]
    app.ship.bullets = [a for k, a in enumerate(app.ship.bullets) if k not in to_remove_bullets]


if __name__ == '__main__':
    import math
    import random
    import sys

    from uib_inf100_graphics.event_app import run_app
    from uib_inf100_graphics.helpers import scaled_image
    from collision import GJK
    from ship import Ship
    from asteroid import Asteroid
    from bg_scene import Star
    from buttons import create_menu
    from helpers import create_asteroid_poly

    intervall = sys.getswitchinterval()
    sys.setswitchinterval(intervall*1000)
    run_app(width=800, height=600, title="ASTEROIDS!")
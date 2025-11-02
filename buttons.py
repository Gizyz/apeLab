from ship import Ship

class Button():
    def __init__(self, btn_json):
        self.pos_list = btn_json["positions"]
        self.name = btn_json["name"]
        self.event = btn_json["event"]
        self.cost = btn_json["cost"]
        self.max = btn_json["max"]

        self.bought = 0
        
    def click(self, app, mouse_x, mouse_y):
        (x1, y1, x2, y2) = self.pos_list
        #checks if mouse is within btn bounds
        if x1 < mouse_x < x2 and y1 < mouse_y < y2:
            #Checks if you have less than max upgrades
            if self.bought < self.max:
                if app.cash >= self.cost:
                    app.cash -= self.cost
                    self.bought += 1
                    eval(self.event)(app)
                        
            elif self.max == -1:
                eval(self.event)(app)

            
    def draw(self, canvas):
        if self.bought == self.max:
            color = 'orange'
        else:
            color = 'gray'
        
        (x1, y1, x2, y2) = self.pos_list
        txt_x = x1 + (x2-x1)/2
        txt_y = y1 + (y2-y1)/2
        
        if self.max >= 0:
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')
            canvas.create_text(txt_x, txt_y-10, text=f'Amount: {self.bought}', fill='blue')
            canvas.create_text(txt_x, txt_y, text=f'{self.name}', fill='blue')
            canvas.create_text(txt_x, txt_y+10, text=f'{self.cost}$', fill='blue')
        else:
            canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='white')
            canvas.create_text(txt_x, txt_y, text=self.name, fill='blue', font=('Courier new', 20, ''))
        
from pathlib import Path
import json
def create_menu():
    content = Path('btn_map.json').read_text(encoding='utf-8')
    data = json.loads(content)
    btns = []
    for btn in data:
        btns.append(Button(btn))
    return btns

def speed_increase(app):
    app.ship_speed += 0.1
def bullet_speed_increase(app):
    app.bullet_speed += 1
def rof_increase(app):
    app.fire_rate -= 1
    
def damage_increase(app):
    app.bullet_damage += 1
def asteroid_increase(app):
    app.asteroid_count += 1


def game_start(app):
    print('START')
    
    app.state = 'game'
    app.timer_delay = 16
    app.key_presses = set()
    app.ship = Ship(app.width/2, app.height/2, app.ship_speed, app.fire_rate)
    app.asteroids = []
    app.stars = []
        
if __name__ == '__main__':
    from uib_inf100_graphics.simple import canvas, display
    
    btns = create_menu()
    for btn in btns:
        btn.draw(canvas)
        eval(btn.event)()
        print(btn.cost)
    display(canvas)
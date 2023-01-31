from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, \
    ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint, choice
from kivy.core.window import Window


# TODO: FINISH BOOKLET'S CODE

'''
WIDGETS (DEFINED IN pong.kv)
'''

class PongPaddle(Widget):

    DEFAULT_LENGTH = 200

    score = NumericProperty(0)
    score_label = ObjectProperty(None)
    size_mods = NumericProperty(0)
    length = NumericProperty(DEFAULT_LENGTH)

class PongLengthUp(Widget):

    image = ObjectProperty(None)

    def collected(self, ball):
        if self.collide_widget(ball):
            self.pos = Vector(-100, -100)
            if ball.x_vel > 0:
                p1 = self.parent.p1
                p1.size_mods += 1
                if p1.size_mods == 0:
                    p1.length = PongPaddle.DEFAULT_LENGTH
                else:
                    p1.length += PongPaddle.DEFAULT_LENGTH / (3**(abs(p1.size_mods)))
            if ball.x_vel < 0:
                p2 = self.parent.p2
                p2.size_mods += 1
                if p2.size_mods == 0:
                    p2.length = PongPaddle.DEFAULT_LENGTH
                else:
                    p2.length += PongPaddle.DEFAULT_LENGTH / (3**(abs(p2.size_mods)))

class PongLengthDown(Widget):
    
    image = ObjectProperty(None)

    def collected(self, ball):
        if self.collide_widget(ball):
            self.pos = Vector(-100, -100)
            if ball.x_vel < 0:
                p1 = self.parent.p1
                p1.size_mods -= 1
                if p1.size_mods == 0:
                    p1.length = PongPaddle.DEFAULT_LENGTH
                else:
                    p1.length -= PongPaddle.DEFAULT_LENGTH / (3**(abs(p1.size_mods)))
            if ball.x_vel > 0:
                p2 = self.parent.p2
                p2.size_mods -= 1
                if p2.size_mods == 0:
                    p2.length = PongPaddle.DEFAULT_LENGTH
                else:
                    p2.length -= PongPaddle.DEFAULT_LENGTH / (3**(abs(p2.size_mods)))


class PongBall(Widget):

    x_vel = NumericProperty(0)
    y_vel = NumericProperty(0)
    vel = ReferenceListProperty(x_vel, y_vel)

    def move(self):
        self.pos = Vector(*self.vel) + self.pos


class PongGame(Widget):

    BALL_SPEED = 4
    BASE_BALL_SPEED_UP = 0.075
    PADDLE_MOVE = 5
    PAUSE_FLASH = 0.5
    POWERUP_SPAWN = 5

    powerups = ObjectProperty(None)
    ball = ObjectProperty(None)
    p1 = ObjectProperty(None)
    p2 = ObjectProperty(None)
    paused_text = StringProperty("")
    length_up_1 = ObjectProperty(None)
    length_down_1 = ObjectProperty(None)
    length_up_2 = ObjectProperty(None)
    length_down_2 = ObjectProperty(None)
    powerups = ReferenceListProperty(length_up_1, length_down_1, length_up_2, length_down_2)

    def initialise(self):

        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)

        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.on_key_up)

        self.p1_up = False
        self.p2_up = False
        self.p1_down = False
        self.p2_down = False
        self.paused = False
        self.pause_flash_countdown = 0
        self.powerup_counter = PongGame.POWERUP_SPAWN
    
    def update(self, delta):
        
        if not self.paused and Window.focus:

            self.paused_text = ""
            self.pause_flash_countdown = 0

            self.ball.move()

            if self.ball.y < 0 or self.ball.top > self.height:
                self.ball.y_vel *= -1
            if self.ball.x < 0:
                self.p2.score += 1
                self.reset_ball(0)
            if self.ball.x > self.width:
                self.p1.score += 1
                self.reset_ball(1)

            if self.p1.y < 0:
                self.p1.y = 0
            else:
                if self.p1_up:
                    self.p1.center_y += PongGame.PADDLE_MOVE

            if self.p1.y + self.p1.length > self.height:
                self.p1.y = self.height - self.p1.length
            else:
                if self.p1_down:
                    self.p1.center_y -= PongGame.PADDLE_MOVE
            
            if self.p2.y < 0:
                self.p2.y = 0
            else:
                if self.p2_up:
                    self.p2.center_y += PongGame.PADDLE_MOVE

            if self.p2.y + self.p2.length > self.height:
                self.p2.y = self.height - self.p2.length
            else:
                if self.p2_down:
                    self.p2.center_y -= PongGame.PADDLE_MOVE

            PongGame.bounce_ball(self.p1, self.ball)
            PongGame.bounce_ball(self.p2, self.ball)

            for powerup in self.powerups:
                powerup.collected(self.ball)

            self.powerup_counter -= delta

            if self.powerup_counter <= 0:
                self.powerup_counter = PongGame.POWERUP_SPAWN * randint(500,1500)/1000
                self.spawn_powerup()
        
        else:
            if self.pause_flash_countdown <= 0:
                self.pause_flash_countdown = PongGame.PAUSE_FLASH
                if self.paused_text == "":
                    self.paused_text = "PAUSED"
                else:
                    self.paused_text = ""
            else:
                self.pause_flash_countdown -= delta
    
    def spawn_powerup(self):
        temp_p = list(self.powerups)
        p = choice(temp_p)
        while len(temp_p) > 1 and p.pos != Vector(-100, -100):
            temp_p.remove(p)
            p = choice(temp_p)
        if p.pos == Vector(-100, -100):
            p.center = Vector(randint(50, self.parent.width-50), randint(50, self.parent.height-50))

    def keyboard_closed(self):
        print("Lost keyboard")
        self.keyboard.unbind(on_key_down=self.on_key_down)
    
    def on_key_down(self, _keyboard, keycode, _text, _modifiers):

        if keycode[1] == "w":
            self.p1_up = True
        if keycode[1] == "s":
            self.p1_down = True
        if keycode[1] == "up":
            self.p2_up = True
        if keycode[1] == "down":
            self.p2_down = True

        if keycode[1] == "p":
            self.paused = not self.paused

        return True

    def on_key_up(self, _keyboard, keycode):

        if keycode[1] == "w":
            self.p1_up = False
        if keycode[1] == "s":
            self.p1_down = False
        if keycode[1] == "up":
            self.p2_up = False
        if keycode[1] == "down":
            self.p2_down = False
        return True

    
    def reset_ball(self, x=None):
        if x is None:
            x = randint(0,1)
        self.ball.center = self.center
        rotation = randint(-45,45)
        rotation += 180 * x
        self.ball.vel = Vector(PongGame.BALL_SPEED, 0).rotate(rotation)
        self.p1.length = PongPaddle.DEFAULT_LENGTH
        self.p2.length = PongPaddle.DEFAULT_LENGTH
        self.p1.size_mods = 0
        self.p2.size_mods = 0
    

    def bounce_ball(paddle, ball):
        if paddle.collide_widget(ball):
            ball.vel[0] *= -1
            multiplier = randint(0, 2000) / 1000 * PongGame.BASE_BALL_SPEED_UP
            ball.vel = [x * (multiplier + 1) for x in ball.vel]
            ball.vel = Vector(*ball.vel).rotate(randint(-20, 20))

    # Currently disabled in favor of keyboard input

    #def on_touch_move(self, touch):
    #    if touch.x < self.width / 3:
    #        self.p1.center_y = touch.y
    #    if touch.x > self.width * 2 / 3:
    #        self.p2.center_y = touch.y
        

'''
APPLICATION
'''

class PongApp(App):
    def build(self):
        game = PongGame()
        game.initialise()
        game.reset_ball()
        Clock.schedule_interval(game.update, 1/60)
        return game


'''
MAIN
'''

if __name__ == "__main__":
    PongApp().run()
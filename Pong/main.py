from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, \
    ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window


# TODO: FINISH BOOKLET'S CODE

'''
WIDGETS (DEFINED IN pong.kv)
'''

class PongPaddle(Widget):

    score = NumericProperty(0)
    score_label = ObjectProperty(None)
    length = NumericProperty(25)


class PongBall(Widget):

    x_vel = NumericProperty(0)
    y_vel = NumericProperty(0)
    vel = ReferenceListProperty(x_vel, y_vel)

    def move(self, _delta):
        self.pos = Vector(*self.vel) + self.pos


class PongGame(Widget):

    BALL_SPEED = 4
    BASE_BALL_SPEED_UP = 0.075
    PADDLE_MOVE = 5

    ball = ObjectProperty(None)
    p1 = ObjectProperty(None)
    p2 = ObjectProperty(None)

    def initialise(self):

        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)

        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.on_key_up)

        self.p1_up = False
        self.p2_up = False
        self.p1_down = False
        self.p2_down = False
    
    def update(self, delta):

        self.ball.move(delta)

        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.y_vel *= -1
        if self.ball.x < 0:
            self.p2.score += 1
            self.reset_ball(0)
        if self.ball.x > self.width:
            self.p1.score += 1
            self.reset_ball(1)

        if self.p1_up:
            self.p1.center_y += PongGame.PADDLE_MOVE
        if self.p1_down:
            self.p1.center_y -= PongGame.PADDLE_MOVE
        if self.p2_up:
            self.p2.center_y += PongGame.PADDLE_MOVE
        if self.p2_down:
            self.p2.center_y -= PongGame.PADDLE_MOVE

        PongGame.bounce_ball(self.p1, self.ball)
        PongGame.bounce_ball(self.p2, self.ball)

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
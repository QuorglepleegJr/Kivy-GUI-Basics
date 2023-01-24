from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, \
    ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


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

    def move(self, delta):
        self.pos = Vector(*self.vel) * delta + self.pos


class PongGame(Widget):

    BALL_SPEED = 240
    BALL_SPEED_UP = 1.1

    ball = ObjectProperty(None)
    p1 = ObjectProperty(None)
    p2 = ObjectProperty(None)
    
    def update(self, delta):

        self.ball.move(delta)

        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.y_vel *= -1
        if self.ball.x < 0 or self.ball.right > self.width:
            self.ball.x_vel *= -1

        PongGame.bounce_ball(self.p1, self.ball)
        PongGame.bounce_ball(self.p2, self.ball)
    
    def reset_ball(self):
        self.ball.center = self.center
        rotation = randint(0,360)
        while rotation % 180 + 90 == 0:
            rotation = randint(0,360)
        self.ball.vel = Vector(PongGame.BALL_SPEED, 0).rotate(rotation)
    

    def bounce_ball(paddle, ball):
        if paddle.collide_widget(ball):
            ball.velocity[0] *= -1
            ball.velocity *= paddle.parent.BALL_SPEED_UP
        

'''
APPLICATION
'''

class PongApp(App):
    def build(self):
        game = PongGame()
        game.reset_ball()
        Clock.schedule_interval(game.update, 1/60)
        return game


'''
MAIN
'''

if __name__ == "__main__":
    PongApp().run()
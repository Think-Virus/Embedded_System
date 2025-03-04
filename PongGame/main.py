# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App
# A Widget is the base building block
# of GUI interfaces in Kivy.
# It provides a Canvas that
# can be used to draw widget on screen.
from kivy.uix.widget import Widget
#import kivy Properties below for numeric property, reference list property, and object property
#from kivy.properties import 
from kivy.vector import Vector
from random import randint
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

class PongPaddle(Widget):
    # define score as numeric property and initialize it to zero
    #score = 

    #define ball velocity when it hits a paddle
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset =  (ball.center_y - self.center_y )/(self.height /2)
            bounced = Vector(1*vx,vy) #a nagative value on x axis allows the ball travels in -x direction
            vel = bounced *1.1
            ball.velocity = vel.x, vel.y +offset

class PongBall(Widget):
    #define numeric property for velocity
    #velocity_x = 0
    #velocity_y = 0
    velocity  = ReferenceListProperty(velocity_x, velocity_y)


    def move(self):
        #self.pos =  Vector(*self.velocity)+self.pos
        #new position is determined from ball's current velocity+position
        self.pos =  Vector(self.velocity)+self.pos

# class in which we are creating the canvas
class PongGame(Widget):
    #define object: ball, player1 and player2 and initialize them as none
    #ball 
    #player1 
    #player2 

    # define an initial ball location whenn is served. 
    def serve_ball(self, vel = (4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        #self.ball.velocity = Vector(4,0).rotate(randint(0,360))

    #update ball location and also ball location when it hits paddle
    def update(self,dt):
        self.ball.move()

        #bounce ball of the paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        #set boundaries for ball
        if(self.ball.y = self.y) or (self.ball.top = self.top):
            self.ball.velocity_y *=-1


        #bounce ball top to bottom
        #if(self.ball.y < 0) or (self.ball.top > self.height):
            #self.ball.velocity_y *=-1

        #bounce ball left to right
        #if(self.ball.x < 0) or (self.ball.right > self.width):
            #self.ball.velocity_x *=-1

        #check if player scored
        if self.ball.x < self.x:
            self.player2.score = 1  #issue here
            self.serve_ball(vel = (4,0))
        if self.ball.x > self.width:
            self.player1.score =1   #issue here
            self.serve_ball(vel = (-4,0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y

# Create the App Class
class mainApp(App):
    def build(self):

        pong_game = PongGame()
        pong_game.serve_ball()
        Clock.schedule_interval(pong_game.update, 1.0/60.0)

        return pong_game



# run the App
if __name__ =='__main__':
    mainApp().run()

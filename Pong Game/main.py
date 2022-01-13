from turtle import Screen
from paddle import Paddle
from ball import Ball
from score import Score
import time


screen = Screen()
screen.setup(height=600, width=800)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)


paddle_right = Paddle((350,0))
paddle_left = Paddle((-350, 0))
ball = Ball()
score_left = Score(-100,200)
score_right = Score(100,200)
screen.listen()

is_game_on = True
while is_game_on:
    screen.update()
    time.sleep(ball.ball_speed)
    screen.onkey(paddle_right.go_up, "Up")
    screen.onkey(paddle_right.go_down, "Down")
    screen.onkey(paddle_left.go_up, "w")
    screen.onkey(paddle_left.go_down,"s")
    ball.move()

    #identifying the collision with the wall(top and bottom of the screen)
    if ball.ycor() < -280 or ball.ycor()>280:

        ball.bounce_y()

    #identifying the collision with the paddle
    if ball.distance(paddle_right) < 47 and ball.xcor() >320 or ball.distance(paddle_left) < 50 and ball.xcor() < -320:
        ball.bounce_x()
        print("this ran")


    #identifying whether the paddle missed the ball
    if ball.xcor() >340:
        score_left.increase()
        ball.reset_ball()
    elif ball.xcor() < -360:
        score_right.increase()
        ball.reset_ball()







screen.exitonclick()



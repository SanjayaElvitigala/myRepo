from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, STARTING_POS):
        super().__init__()
        self.shape("square")
        self.penup()
        self.color("white")
        self.shapesize(stretch_len=1,stretch_wid=5)
        self.goto(STARTING_POS)

    def go_up(self):
        self.sety(self.ycor() + 20.0)

    def go_down(self):
        self.sety(self.ycor() - 20.0)
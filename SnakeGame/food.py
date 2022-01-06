from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("green")
        self.speed("fastest")

        # it is -280 and 280 because our screen is 600 x 600 and needed to avoid the edge of the screen.
        # origin is at the middle of the screen
        rand_x, rand_y = random.randint(-280, 280), random.randint(-280, 280)
        self.goto((rand_x, rand_y))
        self.refresh()

    def refresh(self):
        rand_x, rand_y = random.randint(-280, 280), random.randint(-280, 280)
        self.goto((rand_x, rand_y))
from turtle import Turtle
ALIGN = "center"
FONT = ("Courier", 80, "normal")

class Score(Turtle):
    def __init__(self,x,y):
        super().__init__()
        self.score = 0
        self.penup()
        self.color("white")
        self.hideturtle()
        self.goto(x,y)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(self.score, align=ALIGN, font=FONT)
    def increase(self):
        self.score+=1
        self.clear()
        self.update_scoreboard()
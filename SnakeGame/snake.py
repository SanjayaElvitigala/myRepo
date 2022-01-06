from turtle import Turtle

STARTING_POSITIONS = [(0,0), (-20,0), (-40,0)]
MOVE_DISTANCE = 20
UP, DOWN, LEFT, RIGHT = 90, 270, 180, 0


class Snake:

    def __init__(self):
        self.snake_segments = []
        # code below creates the starting snake
        self.create_snake()
        self.head = self.snake_segments[0]

        # print(turtle_obj[0].pos()[0])
        # aligns the segments one after the other such that 3 squares(pieces) are in line with each other

        # .pos()[0] part extracts the x coordinate of the segment's position

        # self.snake_segments[1].setx(self.snake_segments[0].pos()[0] - 20.0)
        # self.snake_segments[2].setx(self.snake_segments[1].pos()[0] - 20.0)

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, postion):
            segment = Turtle(shape="square")
            segment.penup()
            segment.color("white")
            segment.goto(postion)
            self.snake_segments.append(segment)

    def extend(self):
        self.add_segment(self.snake_segments[-1].position())

    def move(self):
        """moves the snake"""
        # to avoid the separation of the segments when moving this for loop is used such that the pieces overlap
        for seg_num in range(len(self.snake_segments) - 1, 0, -1):
            # makes the pieces follow each other
            new_x = self.snake_segments[seg_num - 1].xcor()
            new_y = self.snake_segments[seg_num - 1].ycor()
            self.snake_segments[seg_num].goto(new_x, new_y)
        self.snake_segments[0].forward(MOVE_DISTANCE)

    def up(self):
        if not self.head.heading() == DOWN:
            self.head.setheading(UP)

    def down(self):
        if not self.head.heading() == UP:
            self.head.setheading(DOWN)

    def left(self):
        if not self.head.heading() == RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if not self.head.heading() == LEFT:
            self.head.setheading(RIGHT)




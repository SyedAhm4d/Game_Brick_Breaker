import turtle
from turtle import Turtle, Screen
import time,random,math
import winsound,threading,pygame

pygame.mixer.init()

def play_sound(filename):
    def _play():
        sound = pygame.mixer.Sound(filename)
        sound.play()
    threading.Thread(target=_play, daemon=True).start()

def start_sound():
    winsound.Beep(1000, 100)

pygame.init()
arcade = pygame.font.Font("ARCADE_N.TTF",) # Load the font


# Simple heart shape polygon
points = [
    (0, -2.5),
    (-2.5, 0),
    (-1, 2),
    (0, 1),
    (1, 2),
    (2.5, 0),
    (0, -2.5)
]

# Scale down the heart to fit turtle screen nicely
points_scaled = [(x * 5, y * 5) for x, y in points]

# Register heart shape
turtle.register_shape("heart", tuple(points_scaled))


STEP=150
LEFT_BOUNDARY=-750
RIGHT_BOUNDARY=750
UPPER_BOUNDARY=360
LOWER_BOUNDARY=-360

class Breakout(Turtle):
    def __init__(self):
        super().__init__()

        self.STEP_BALL_X = 5
        self.STEP_BALL_Y = -5
        self.last_location=0
        self.hearts_left=[None,None,None,None,None]

        self.screen_define()
        self.turtle_define()
        self.ball_define()
        self.boundary_define()

        self.sleep=0.01

        self.wall1=[]
        self.wall2=[]
        self.wall3=[]
        self.wall4=[]
        self.walls=[self.wall1,self.wall2,self.wall3,self.wall4]
        self.create_wall(color='green',y=0,wall=self.wall1)
        self.create_wall(color='orange',y=50,wall=self.wall2)
        self.create_wall(color='red',y=100,wall=self.wall3)
        self.create_wall(color='crimson',y=150,wall=self.wall4)
        self.create_hearts()

        self.screen.update()

        self.print_gamestart()
        self.start_game()
        self.screen.mainloop()

    def screen_define(self):
        self.screen = Screen()
        import tkinter
        root = tkinter.Tk()
        root.withdraw()  # Hide the small Tk window
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        # Set the turtle window size

        self.screen.setup(width=w, height=h)
        self.screen.bgcolor('black')
        self.screen.listen()
        self.screen.tracer(0)
        self.screen.onkeypress(self.move_left, "Left")
        self.screen.onkeypress(self.move_right, 'Right')

    def turtle_define(self):
        self.shape('square')
        self.shapesize(0.5, 14)
        self.color('blue')
        self.penup()
        self.goto(0, LOWER_BOUNDARY+20)

    def ball_define(self):
        self.ball=Turtle()
        self.ball.penup()
        self.ball.color('white')
        self.ball.shape('circle')
        self.ball.goto(0,-320)

    def create_hearts(self):
        for item in range(len(self.hearts_left)):
            heart=Turtle()
            heart.left(90)
            heart.color('red')
            heart.penup()
            heart.shape("heart")
            heart.shapesize(1,1)
            self.hearts_left[item]=heart
            if item==0:
                heart.goto(LEFT_BOUNDARY+40,UPPER_BOUNDARY-40)
            else:
                heart.goto(self.calc_distance(self.hearts_left[item-1],self.hearts_left[item]),UPPER_BOUNDARY-40)

    def boundary_define(self):
        t = Turtle()
        t.pensize(20)
        t.goto(LEFT_BOUNDARY, LOWER_BOUNDARY)
        t.speed(1000)
        t.pencolor('grey')
        t.setheading(90)

        for _ in range(2):
            t.forward(2 * UPPER_BOUNDARY)
            t.right(90)
            t.forward(2 * RIGHT_BOUNDARY)
            t.right(90)
        t.color('grey')

    def start_game(self):
        self.play_animation()

        while True:
            self.screen.update()
            self.ball_move()
            self.check_collision()
            time.sleep(self.sleep)

    def calc_distance(self, last_brick, current_brick):
        # Half-widths
        half_width_last = last_brick.shapesize()[1] * 10  # half of (stretch_len * 20)
        half_width_current = current_brick.shapesize()[1] * 10

        last_center_x = last_brick.pos()[0]

        # New brick center:
        next_center_x = last_center_x + half_width_last +5+ half_width_current

        return next_center_x

    def total_length(self,wall:list):
        total_length=0
        for item in wall:
            total_length+=item.shapesize()[1]*20

        total_length+=len(wall)*5
        return total_length

    def ball_move(self):
        self.ball.speed(10)
        self.ball.goto(self.ball.xcor()+self.STEP_BALL_X,self.ball.ycor()+self.STEP_BALL_Y)

    def create_wall(self,color:str,y:int,wall):
        for item in range(15):
            brick=Turtle()
            brick.color(color)
            brick.shape('square')
            brick.shapesize(2,random.randrange(4,7,1))
            brick.penup()
            wall.append(brick)
            self.locate_brick(brick,y,wall)

    def locate_brick(self,brick,y,wall):
        if len(wall) == 1:
            brick.goto((LEFT_BOUNDARY + 10 + brick.shapesize()[1] * 10) + 5, y)
        else:
            brick.goto(self.calc_distance(wall[-2], wall[-1]), y)
        if self.total_length(wall) > 1480:
            try:
                brick.shapesize(2, brick.shapesize()[1] - 0.5)
                self.locate_brick(brick,y,wall)
            except turtle.TurtleGraphicsError:
                wall.pop(wall.index(brick))
                brick.hideturtle()

    def break_wall(self,items,item):
        # item.hideturtle()
        # items.pop(items.index(item))
        # if items == self.wall1:
        #     self.sleep = 0.001
        # elif items == self.wall2:
        #     self.sleep = 0.000001
        # elif items == self.wall3:
        #     self.sleep = 0
        #
        # if len(self.wall1) == len(self.wall2) == len(self.wall3) == len(self.wall4) == 0:
        #     self.print_gamewin()
        for i,items in enumerate(self.walls):
            for item in items:
                if abs(self.ball.ycor() - item.ycor()) < 40 and abs(self.ball.xcor() - item.xcor()) < item.shapesize()[1] * 10+10:
                    item.hideturtle()
                    items.pop(items.index(item))
                    if i==0:
                        self.sleep=0.001
                    elif i==1:
                        self.sleep=0.000001
                    elif i==2:
                        self.sleep=0
                    self.screen.update()
                    if len(self.wall1)==len(self.wall2)==len(self.wall3)==len(self.wall4)==0:
                        self.print_gamewin()
                    play_sound('brick_break.mp3')

    def check_collision(self):
        if self.ball.ycor()-self.ycor()<20 and abs(self.ball.xcor()-self.xcor())<self.shapesize()[1]*10:
            self.STEP_BALL_Y=-1*self.STEP_BALL_Y
            if self.ball.xcor()<self.xcor():
                self.STEP_BALL_X=-1*random.randint(1,5)
            else:
                self.STEP_BALL_X=random.randint(1,5)

        if self.ball.ycor()>UPPER_BOUNDARY-20:
            self.STEP_BALL_Y=-1*self.STEP_BALL_Y
        if self.ball.ycor()<self.ycor():
            self.STEP_BALL_Y=-1*self.STEP_BALL_Y
            time.sleep(1)
            self.ball.hideturtle()
            self.hearts_left=[item.hideturtle() for item in self.hearts_left]
            self.hearts_left = [None for item in range(len(self.hearts_left)-1)]
            if len(self.hearts_left)==0:
                self.print_gameover()
            self.create_hearts()
            self.last_location=self.ball.xcor()
            self.ball_define()
            return
        if self.ball.xcor()<LEFT_BOUNDARY+20:
            self.STEP_BALL_X=-1*self.STEP_BALL_X
        if self.ball.xcor()>RIGHT_BOUNDARY-20:
            self.STEP_BALL_X=-1*self.STEP_BALL_X
        for items in self.walls:
            for item in items:
                if 30<abs(self.ball.ycor() - item.ycor()) < 40 and abs(self.ball.xcor() - item.xcor()) < item.shapesize()[1] * 10:
                    self.STEP_BALL_Y = -1 * self.STEP_BALL_Y
                    self.break_wall(items,item)
                if abs(self.ball.ycor() - item.ycor()) < 30 and abs(self.ball.xcor() - item.xcor()) < item.shapesize()[1] * 10+10:
                    self.STEP_BALL_X= -1 * self.STEP_BALL_X
                    self.break_wall(items,item)

    def move_left(self):
        if self.pos()[0] - STEP > LEFT_BOUNDARY:
            self.goto(self.pos()[0] - STEP, self.pos()[1])

    def move_right(self):
        if self.pos()[0] + STEP < RIGHT_BOUNDARY:
            self.goto(self.pos()[0] + STEP, self.pos()[1])

    def print_gamestart(self):
        writer = Turtle()
        writer.color('white')
        writer.penup()
        font = 101
        self.space_pressed=False
        self.screen.onkey(self.start,'space')
        while not self.space_pressed:
            writer.write("Game Start!", align="center", font=('Arcade Normal',font, "bold"))
            writer.goto(0,-100)
            writer.write("Press Space to Start Game", align="center", font=('Arcade Normal', 10, "bold"))
            writer.goto(0,0)
        writer.clear()
        writer.hideturtle()

    def start(self):
        self.screen.onkey(self.do_nothing, 'space')
        self.space_pressed=True
        return

    def play_animation(self):
        writer = Turtle()
        writer.color('white')
        writer.penup()
        font = 101
        threading.Thread(target=start_sound()).start()
        while font > 0:
            writer.clear()
            writer.write("Game Start!", align="center", font=('Arcade Normal', font, "bold"))
            # self.screen.update()
            time.sleep(0.03)
            font -= 5
        writer.clear()
        writer.hideturtle()

    def print_gameover(self):
        writer=Turtle()
        writer.color('white')
        writer.penup()
        font=16
        play_sound('end.mp3')
        while font<100:
            writer.clear()
            writer.write("Game Over!", align="center", font=('Arcade Normal', font, "bold"))
            font+=5
            time.sleep(0.03)
        time.sleep(2)
        exit()

    def print_gamewin(self):
        writer = Turtle()
        writer.color('white')
        writer.penup()
        font = 16
        play_sound('start.mp3')
        while font < 100:
            writer.clear()
            writer.write("Game Won!", align="center", font=('Arcade Normal', font, "bold"))
            font += 5
            time.sleep(0.03)
        time.sleep(2)
        exit()

    def do_nothing(self):
        pass


Breakout()
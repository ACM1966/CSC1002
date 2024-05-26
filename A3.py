import turtle
import random
from functools import partial

g_screen = None
g_snake = None
# g_monster = None
monster_list = [None, None, None, None]      # 4 monsters
g_snake_sz = 5
g_intro = None
g_keypressed = None
g_status = None

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"
FONT = ("Arial",16,"normal")

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
       "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_LEFT:180, KEY_RIGHT:0, KEY_UP:90, KEY_DOWN:270}


'''Below are self-designed variables'''
x_s, y_s = 0, 0 ; monster_pos = []
snake_pos = []
# keys_list = [ KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]
g_time = 0
g_timer = None
g_contact = 0
g_ccounter = None
# This list should work as a Queue using functions such as ._pop() ._append()
PAUSE = False
BOUNDED = [None, None, False, False]
# 0: for horizontal key if snake is on left/right bound; 1: for vertical key if snake is on up/down bound;
BODY = [[None, None, None, None], False]    # Left-Right-Up-Down
# Whether 4 direction are bounded (begin with unbounded)
# Since directions can be bounded at the same time, so us a list to deal with multi-bounded cases

END = False
# This shows game end or not

result_pen = turtle.Turtle()
result_pen.hideturtle()


def configurePlayArea():

    # motion border
    m = createTurtle(0,0,"","black")
    m.shapesize(25,25,5)
    m.goto(0,-40)  # shift down half the status

    # status border 
    s = createTurtle(0,0,"","black")
    s.shapesize(4,25,5)
    s.goto(0,250)  # shift up half the motion

    # introduction
    intro = createTurtle(-150,5)
    intro.hideturtle()
    intro.write("Click anywhere to start the game .....", font=("Arial",16,"normal"))
    
    # statuses
    status = createTurtle(0,0,"","black")
    status.hideturtle()
    status.goto(-200,s.ycor()) 

    # contact-counter, used to draw contact times in the game
    counter = createTurtle(-20,250)
    counter.hideturtle()
    counter.goto(-200,240)
    counter.write('Contact:0', font=('arial',15,'bold'))

    '''Below are pens added in imitation of the above doing similar jobs'''
    # timer, used to draw time in the game
    timer = createTurtle(150,250)
    timer.hideturtle()
    timer.goto(-30,240)
    timer.write('Time:0', font=('arial',15,'bold'))

    return intro, status, timer, counter

def configScreen():
    s = turtle.Screen()
    s.tracer(0)    # disable auto screen refresh, 0=disable, 1=enable
    # s.title("Snake")
    s.setup(500+120, 500+120+80)
    s.mode("standard")
    return s

# create turtle, red is head and body is black
def createTurtle(x, y, color="red", border="black"):
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x,y)
    return t

def updateStatus():
    global PAUSE

    g_status.clear()
    g_status.goto(100,240)
    if PAUSE:               
        g_status.write('Motion:Paused', font=('arial',15,'bold'))
    else:
        g_status.write('Motion:'+str(g_keypressed), font=('arial',15,'bold'))
    g_screen.update()

def setSnakeHeading(key):
    if key in HEADING_BY_KEY.keys():
        g_snake.setheading( HEADING_BY_KEY[key] )

def onArrowKeyPressed(key):
    global g_keypressed, PAUSE, BOUNDED
    # The game ends
    if END:
        return

    if key == KEY_SPACE:
        if PAUSE:
            PAUSE = False
        elif PAUSE is not True:
            PAUSE = True
    else:
        # if press the key that is bounded, skip it
        if (BOUNDED[2] == True) and (key == BOUNDED[0]):
            pass
        elif (BOUNDED[3] == True) and (key == BOUNDED[1]):
            pass
        else:
            if (key in BODY[0]):    # Means the direction of the key is bounded, skip it
                pass
            else:
                if PAUSE:   # all direction can unpause as long as not bounded
                    PAUSE = False
                g_keypressed = key
                setSnakeHeading(key)
    updateStatus()
    
def onTimerSnake():
    global PAUSE, BOUNDED, BODY, END, x_s, y_s, snake_pos, g_snake_sz, foodList#, g_keypressed # The snake could run without press at the very beginning
    
    # Game ends - Player win
    if checkFoodEaten():
        result_pen.pendown()
        result_pen.color("red")
        result_pen.write('Winner!!', font=('arial',20,'bold'))
        END = True
        g_screen.update()

    # The game ends
    if END:
        return

    if g_keypressed == None:
        # The snake could run without press at the very beginning with the code behind
        # g_keypressed = KEY_RIGHT
        g_screen.ontimer(onTimerSnake, 300)
        return
    
    if PAUSE == False:

        if (g_keypressed in BOUNDED) and (True in BOUNDED):     #
            pass 
        else:
            if g_keypressed in BODY[0] and (BODY[1]):
                pass
            else:

                # Clone the head as body
                g_snake.color(*COLOR_BODY)
                g_snake.stamp()
                g_snake.color(COLOR_HEAD)
                # Denote location of the snake
                if len(snake_pos) == g_snake_sz + 1:
                    snake_pos.pop()     # Can be considered as dequeue
                # Advance snake
                g_snake.forward(20)
                
                # Locate the head of the snake, noticing there exists slight errors
                # And add the location to a list, which is a Queue built on list
                snake_pos = [(round(g_snake.xcor()), round(g_snake.ycor()))] + snake_pos

                # Shifting or extending the tail.
                # Remove the last square on Shifting.
                if len(g_snake.stampItems) > g_snake_sz:
                    g_snake.clearstamps(1)

                # Game ends - Player lose
                
                for g_monster in monster_list:
                    x_m = round(g_monster.xcor())
                    y_m = round(g_monster.ycor())
                    if (abs(x_s-x_m) < 20) and (abs(y_s-y_m) < 20):
                        result_pen.pendown()
                        result_pen.color("red")
                        result_pen.write('Game Over!', font=('arial',20,'bold'))
                        END = True


        # Stop the Snake on boundary
        x_s, y_s = round(g_snake.xcor()), round(g_snake.ycor())

        # Bounded on edges
        '''Horizontal: (-240, 240)   Vertical:(-280, 200)'''
        if (x_s >= 240): 
            BOUNDED[0] = KEY_RIGHT
            if (g_keypressed == KEY_RIGHT):
                BOUNDED[2] = True
        elif (x_s <= -240):  
            BOUNDED[0] = KEY_LEFT
            if(g_keypressed == KEY_LEFT): 
                BOUNDED[2] = True
        else: BOUNDED[0] = None; BOUNDED[2] = False     # if not, then unbounded

        if (y_s >= 200): 
            BOUNDED[1] = KEY_UP
            if (g_keypressed == KEY_UP): 
                BOUNDED[3] = True
        elif (y_s <= -280): 
            BOUNDED[1] = KEY_DOWN
            if (g_keypressed == KEY_DOWN):
                BOUNDED[3] = True
        else: BOUNDED[1] = None; BOUNDED[3] = False     # unbounded

        
        # Eat

        for i in range(5):    
            if True in foodList[i][2:]:
                pass
            elif [x_s, y_s] in foodList[i]:     # eaten
                foodList[i][2] = True
                stamp_len = foodList[i][0]
                penList[i].clear()
                g_snake_sz += stamp_len
                # print("Eat", foodList[i][2])      only for checking

    g_screen.update()
    
    if len(g_snake.stampItems) > 4:
        if (len(g_snake.stampItems) < g_snake_sz):
            fre = 500
        else: fre = 300
    else: fre = 300
    g_screen.ontimer(onTimerSnake, fre)

def makeFood():
    global foodList

    '''Horizontal: (-240, 240)   Vertical:(-280, 200)'''
    foodList = []
    num = 0
    while len(foodList) < 5:
        x = 20*random.randint(0, 24) - 240
        y = 20*random.randint(0, 24) - 280

        if (x, y) != (0, 0) and (x, y) not in foodList:
            num += 1
            foodList.append([num, [x, y], False])    
            # (number, location,  eaten)
            
    return foodList

def setFood():
    global penList
    # food goes to the place
    copy = []
    for i in foodList:
        copy.append((i[1][0], i[1][1]-7))
    pen1 = turtle.Turtle() ; pen1.hideturtle() ; pen1.penup()
    pen2 = turtle.Turtle() ; pen2.hideturtle() ; pen2.penup()
    pen3 = turtle.Turtle() ; pen3.hideturtle() ; pen3.penup()
    pen4 = turtle.Turtle() ; pen4.hideturtle() ; pen4.penup()
    pen5 = turtle.Turtle() ; pen5.hideturtle() ; pen5.penup()
    pen1.goto(copy[0]) ; pen1.pendown() ; pen1.write(1, font=('arial',10,'bold'))
    pen2.goto(copy[1]) ; pen2.pendown() ; pen2.write(2, font=('arial',10,'bold'))
    pen3.goto(copy[2]) ; pen3.pendown() ; pen3.write(3, font=('arial',10,'bold'))
    pen4.goto(copy[3]) ; pen4.pendown() ; pen4.write(4, font=('arial',10,'bold'))
    pen5.goto(copy[4]) ; pen5.pendown() ; pen5.write(5, font=('arial',10,'bold'))
    penList = [pen1, pen2, pen3, pen4, pen5]
    

def checkFoodEaten():
    foodEaten = list(filter(lambda food: food[2] == True, foodList))
    if len(foodEaten) == 5:
        return True
    return False

def moveFood():
    global foodList
    if END:
        return

    i = 0
    for food in foodList:
        if not food[2]:
            num = food[0]

            new_x, new_y = dirFood(food[1][0], food[1][1])
            food[1][0] = new_x
            food[1][1] = new_y

            # # Randomly select a direction
             # dx, dy = random.choice([(0, 20), (0, -20), (20, 0), (-20, 0)])
             # #Move the position of food
             # new_x = round(food[1][0] + dx)
             # new_y = round(food[1][1] + dy)

             # # Check if the food exceeds the screen boundaries, if so adjust the position
             # if abs(new_x) <= 240 and abs(new_y) <= 280:
             # foodList[i][1][0] = new_x
             # foodList[i][1][1] = new_y
             #else:
             # # Food exceeds the screen boundaries and randomly resets its position
             # foodList[i][1][0] = random.randint(-240, 240)
             # foodList[i][1][1] = random.randint(-280, 200)
            penList[num-1].clear()
            penList[num-1].penup()
            penList[num-1].goto(foodList[i][1][0], foodList[i][1][1])
            penList[num-1].pendown()
            penList[num-1].write(num, font=('arial',10,'bold'))
            g_screen.update()
        
        i += 1

    g_screen.ontimer(moveFood, 5000)

def dirFood(x, y):
    ### bond: x:(-240, 240), y:(-280, 200)
    dx_list = [0, 20, 40, 80, -20, -40, -80]
    dy_list = [0, 20, 40, 80, -20, -40, -80]

    x_new = y_new = -1000       # initialize

    while ((not -240<=x_new<=240) or (not -280<=y_new<=200)):
        x_new = round(x + random.choice(dx_list))
        y_new = round(y + random.choice(dy_list))

        for food in foodList:
            if (x_new==food[1][0]) and (y_new==food[1][1]):     # avoid overlapping
                x_new = y_new = -1000
    return x_new, y_new

def setMonster():
    global monster_list
    # Set the moster in a fair distance with the snake
    # Whatever, it's far enough and random
    # Ensured not cross the boundary
    pos = []
    for g_monster in monster_list:      # Or just use a list to assign coordinates one by one
        if (2 * random.random() - 1) >= 0: p = 1
        else: p = -1

        x = 10
        while (x == 10) or (x == -10):
            x = 20 * random.randint(-10, 10) + 10 * p

        y = (220 - abs(x)) * p
        g_monster.goto(x, y)

        pos.append([x, y])       

    return pos      # The initial coordinates of each monster


def dirMonster(g_monster):
    # direct moster in the direction towards the snake
    global x_s, y_s
    x, y = g_monster.pos()
    x_m, y_m = round(x), round(y)
    if (x_s or y_s) == None:
        return 0
    
    hor = x_s - x_m ; ver = y_s - y_m

    # Adjust to locations after each move
    if abs(hor) > abs(ver):
        if hor > 0:
            x_m += 20
            return 0
        else: 
            x_m -= 20
            return 180
    else:
        if ver < 0: 
            y_m -= 20
            return 270
        else:           
            y_m += 20
            return 90

'''check the surrounding of the monster'''
def checkContact():
    global g_contact
    for g_monster in monster_list:
        x_m = round(g_monster.xcor())
        y_m = round(g_monster.ycor())
        for i in [(x_m+10, y_m+10), (x_m+10, y_m-10), (x_m-10, y_m+10), (x_m-10, y_m-10)]:
            if i in snake_pos[1:]:  # Locations of the snake excluding the head
                g_contact += 1
                return True
    return False


def onTimerMonster():
    global END
    
    # The game ends
    if END:
        return
    
    # For every monster
    for g_monster in monster_list:
        x_m = round(g_monster.xcor())
        y_m = round(g_monster.ycor())

        g_monster.setheading(dirMonster(g_monster))
        g_monster.forward(20)

        if checkContact():
            g_ccounter.clear()
            g_ccounter.write('Contact:' + str(g_contact), font=('arial',15,'bold'))

        if (abs(x_s-x_m) < 20) and (abs(y_s-y_m) < 20):
            result_pen.pendown()
            result_pen.color("red")
            result_pen.write('Game Over!', font=('arial',20,'bold'))
            END = True
        
    g_screen.update()
        
    # The game ends
    if END:
        return
    
    # Below is regarding the speed(refreshing rate) of moster
    
    g_screen.ontimer(onTimerMonster, 10 * random.randint(55,120))

'''Just denote and write time of game.'''
def onTimerTimer():
    global g_time

    # The game ends
    if END:
        return

    g_timer.clear()
    g_timer.write('Time:'+ str(g_time), font=('arial',15,'bold'))
    g_time += 1
    g_screen.ontimer(onTimerTimer, 1000)

def startGame(x,y):
    g_screen.onscreenclick(None)
    g_intro.clear()

    makeFood()
    setFood()

    g_screen.onkey(partial(onArrowKeyPressed,KEY_UP), KEY_UP)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_DOWN), KEY_DOWN)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_LEFT), KEY_LEFT)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_RIGHT), KEY_RIGHT)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_SPACE), KEY_SPACE)

    g_screen.ontimer(onTimerSnake, 300)
    g_screen.ontimer(onTimerMonster, 1000)
    g_screen.ontimer(onTimerTimer, 1000)
    # g_screen.ontimer(onTimerMonster2, 1000)
    # g_screen.ontimer(onTimerMonster3, 1000)
    # g_screen.ontimer(onTimerMonster4, 1000)


    g_screen.ontimer(moveFood, 5000)

def centerText(turtle, text):
    # Calculate the width and height of text
    width = turtle.window_width()
    height = turtle.window_height()
    turtle.penup()
    turtle.goto(0, 0)
    turtle.write(text, align="center", font=FONT)
    # Calculate the width and height of text
    text_width = turtle.window_width() - width
    text_height = turtle.window_height() - height
    # Move the text to the center of the game area
    turtle.goto(-text_width / 2, -text_height / 2)

def onGameEnd(message):
    end_text = createTurtle(0, 0)
    end_text.hideturtle()
    end_text.color("black")
    centerText(end_text, message)

if __name__ == "__main__":
    g_screen = configScreen()
    g_intro, g_status, g_timer, g_ccounter = configurePlayArea()
    
    updateStatus()

    monster_list[0] = createTurtle(-110,-110,"purple", "black")
    monster_list[1] = createTurtle(-110,110,"purple", "black")
    monster_list[2] = createTurtle(110,-110,"purple", "black")
    monster_list[3] = createTurtle(110,110,"purple", "black")

    result_pen.penup()
    result_pen.hideturtle()
    result_pen.back(50)

    g_snake = createTurtle(0,0,"red", "black")
    monster_pos = setMonster()

    g_screen.onscreenclick(startGame)

    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()
import turtle
import random
import numpy as np

def create_solvable_puzzle(size):
    """Generates a solvable puzzle of a given size."""
    puzzle = np.arange(size**2)
    np.random.shuffle(puzzle)
    while not is_solvable(puzzle, size):
        np.random.shuffle(puzzle)
    puzzle = puzzle.reshape((size, size))
    return puzzle

def is_solvable(puzzle, size):
    """Checks if a puzzle is solvable."""
    inv_count = 0
    flat_puzzle = puzzle.flatten()
    for i in range(size**2 - 1):
        for j in range(i + 1, size**2):
            if flat_puzzle[i] > flat_puzzle[j] != 0:
                inv_count += 1
    return inv_count % 2 == 0

def draw_puzzle(puzzle, size):
    """Draws the puzzle on the screen."""
    t.clear()
    for i in range(size):
        for j in range(size):
            if puzzle[i, j] != 0:
                draw_tile(i, j, puzzle[i, j], size)

def slicing_tile(rowf, colf, rowt, colt):
    ## 把puzzle信息转成坐标信息
    x1 = colf * 80 - (size * 80) / 2 + 40
    y1 = (size * 80) / 2 - rowf* 80 - 40
    x2 = colt * 80 - (size * 80) / 2 + 40
    y2 = (size * 80) / 2 - rowt* 80 - 40

    ## 确认起终点
    xfrom = x1 #- 40
    yfrom = y1 #- 50
    xto = x2 #- 40
    yto = y2 #- 50

    ## reset the graph such that the one to be moved is cleared
    p = puzzle.copy()
    p[rowf][colf] = 0
    p[rowt][colt] = 0
    draw_puzzle(p, size)
    
    pen = turtle.Turtle()
    pen.hideturtle()
    screen.tracer(0)
    pen.penup()
    pen.goto(xfrom, yfrom)
    pen.setheading(pen.towards(xto, yto))
    pen.pendown()
    
    arrived = False
    while arrived==False:
        screen.ontimer(litteMove(pen, xto, yto), 1)
        if (round(pen.pos()[0]) == xto) and (round(pen.pos()[1]) == yto):
            arrived = True
    pen.clear()

def litteMove(pen, xto, yto):
    pen.hideturtle()
    if (round(pen.pos()[0]) == xto) and (round(pen.pos()[1]) == yto):
        return

    pen.clear()
    x_pen, y_pen = pen.pos()
    pen.goto(x_pen-40, y_pen+50)
    pen.color('lightgreen')
    pen.setheading(0)       # look right
    pen.begin_fill()
    for _ in range(4):
        pen.forward(80 - 2)
        pen.right(90)
    pen.end_fill()

    pen.goto(x_pen, y_pen)
    pen.setheading(pen.towards(xto, yto))
    pen.forward(2)      ## 一点点挪

    screen.tracer(1)
    screen.update()
    screen.tracer(0)


def draw_tile(row, col, number, size, color='lightgreen'):

    """Draws a single tile with a light green block behind the number."""
    
    x = col * 80 - (size * 80) / 2 + 40
    y = (size * 80) / 2 - row * 80 - 40
    t.penup()
    
    # Draw light green block
    t.goto(x-40, y+50)
    t.color(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(80 - 2)
        t.right(90)
    t.end_fill()
    
    # Draw number with adjusted position
    t.goto(x, y )
    t.color('blue')
    t.write(number, align="center", font=("Arial", 18, "normal"))
    
    screen.tracer(1)
    screen.update()
    screen.tracer(0)



def onclick(x, y):
    """Handles tile click events."""
    global puzzle, size
    row = int((size * 80) / 2 - y) // 80
    col = int(x + (size * 80) / 2) // 80
    if row < 0 or col < 0 or row >= size or col >= size:
        return
    move_tile(row, col)
    draw_puzzle(puzzle, size)
    cmp=np.arange(1,size**2+1)
    cmp[-1]=0
    if np.array_equal(puzzle.flatten(), cmp):
        celebrate()

def move_tile(row, col):
    """Moves the clicked tile if adjacent to the empty space."""
    global puzzle, size
    zero_row, zero_col = np.where(puzzle == 0)
    zero_row, zero_col = int(zero_row), int(zero_col)
    
    # Check if the clicked tile is adjacent to the empty space
    if (abs(zero_row - row) == 1 and zero_col == col) or (abs(zero_col - col) == 1 and zero_row == row):
        puzzle[zero_row, zero_col], puzzle[row, col] = puzzle[row, col], puzzle[zero_row, zero_col]

        screen.onclick(None)
        screen.tracer(0)
        slicing_tile(row, col, zero_row, zero_col)
        screen.onclick(onclick)


def celebrate():
    """Changes the background color of all tiles to red when the puzzle is solved."""
    screen.tracer(0)  # 禁用屏幕更新
    for i in range(size):
        for j in range(size):
            if i == j == size - 1:
                break
            else:
                draw_tile(i, j, puzzle[i, j], size, "red")
                t.color('red')

    screen.tracer(1)
    screen.update()
    screen.onclick(None)



def main():
    global puzzle, size, t, screen
    t = turtle.Turtle()
    t.hideturtle()
    turtle.hideturtle()
    screen = turtle.getscreen()
    screen.title("Sliding Puzzle Game")
    size = int(screen.numinput("Puzzle Size", "Enter the size of the game (3, 4, 5):", 3, minval=3, maxval=5))
    puzzle = create_solvable_puzzle(size)
    t.speed("fastest")
    t.hideturtle()
    draw_puzzle(puzzle, size)
    screen.onclick(onclick)
    screen.mainloop()

if __name__ == "__main__":
    main()



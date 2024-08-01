import turtle
import time
import copy
import random

# Create a Turtle object
t = turtle.Turtle()
t.speed(25)

status = [0, 0, 0, 0, 0, 0, 0]
board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

player = "yellow"
computer = "red"

player_start = True
search_depth = 4

eval_score = [1, 4, 9]
win = 512
lose = -512
inf = 1024


def invert_board(curr_board, in_place: bool = True):
    if not in_place:
        curr_board = copy.deepcopy(curr_board)
    for r in range(6):
        for c in range(7):
            curr_board[r][c] = -1 * curr_board[r][c]
    return curr_board


def make_move(curr_board, stat, pos, val, in_place: bool = True):
    if not in_place:
        curr_board = copy.deepcopy(curr_board)
    if stat[pos] < 6:
        curr_board[stat[pos]][pos] = val
        stat[pos] += 1
    return curr_board


def evaluate(curr_board):
    result = 0

    for r in range(6):
        pos_count = 0
        neg_count = 0

        for c in range(7):
            if curr_board[r][c] == 1:
                pos_count += 1
            elif curr_board[r][c] == -1:
                neg_count += 1

            if c >= 4:
                if curr_board[r][c - 4] == 1:
                    pos_count -= 1
                elif curr_board[r][c - 4] == -1:
                    neg_count -= 1

            if c >= 3:
                if pos_count == 4:
                    return win
                elif neg_count == 4:
                    return lose
                elif neg_count == 0 and pos_count > 0:
                    result += eval_score[pos_count - 1]
                elif pos_count == 0 and neg_count > 0:
                    result -= eval_score[neg_count - 1]

    for c in range(7):
        pos_count = 0
        neg_count = 0

        for r in range(6):
            if curr_board[r][c] == 1:
                pos_count += 1
            elif curr_board[r][c] == -1:
                neg_count += 1

            if r >= 4:
                if curr_board[r - 4][c] == 1:
                    pos_count -= 1
                elif curr_board[r - 4][c] == -1:
                    neg_count -= 1

            if r >= 3:
                if pos_count == 4:
                    return win
                elif neg_count == 4:
                    return lose
                elif neg_count == 0 and pos_count > 0:
                    result += eval_score[pos_count - 1]
                elif pos_count == 0 and neg_count > 0:
                    result -= eval_score[neg_count - 1]

    for r in range(3):
        for c in range(4):
            pos_count_left = 0
            neg_count_left = 0
            pos_count_right = 0
            neg_count_right = 0

            for k in range(4):
                if curr_board[r + k][c + k] == 1:
                    pos_count_left += 1
                elif curr_board[r + k][c + k] == -1:
                    neg_count_left += 1

            for k in range(4):
                if curr_board[r + k][6 - c - k] == 1:
                    pos_count_right += 1
                elif curr_board[r + k][6 - c - k] == -1:
                    neg_count_right += 1

            if pos_count_left == 4 or pos_count_right == 4:
                return win
            elif neg_count_left == 4 or neg_count_right == 4:
                return lose

            if neg_count_left == 0 and pos_count_left > 0:
                result += eval_score[pos_count_left - 1]
            elif pos_count_left == 0 and neg_count_left > 0:
                result -= eval_score[neg_count_left - 1]

            if neg_count_right == 0 and pos_count_right > 0:
                result += eval_score[pos_count_right - 1]
            elif pos_count_right == 0 and neg_count_right > 0:
                result -= eval_score[neg_count_right - 1]

    return result


def negamax(curr_board, stat, depth, max_depth, alpha, beta):
    if evaluate(curr_board) == win or evaluate(curr_board) == lose:
        return (lose, None)

    if depth == max_depth:
        return (evaluate(curr_board), None)

    eval = alpha
    best_move = []
    move_sequence = [i for i in range(7)]
    random.shuffle(move_sequence)
    for move in move_sequence:
        if stat[move] >= 6:
            continue
        stat_copy = copy.deepcopy(stat)
        new_board = invert_board(make_move(curr_board, stat_copy, move, 1, False), True)
        next_move = negamax(new_board, stat_copy, depth + 1, max_depth, -beta, -eval)
        if -next_move[0] >= beta:
            return (-next_move[0], move)
        if -next_move[0] > eval:
            eval = -next_move[0]
            best_move = move
    return (eval, best_move)


def place(x, col):
    y = status[x]
    t.penup()
    t.goto(x * 100 - 300, y * 100 - 250)
    t.pendown()
    t.pencolor(col)
    t.dot(80)


def write(text, start_pos):
    t.penup()
    t.goto(start_pos, 0)
    t.pendown()
    t.pencolor("black")
    t.write(text, font=("Arial", 32, "normal"))


# Define a function to handle mouse clicks
def get_mouse_click(x, y):
    index = -1
    if (x > -350) and (x < -250) and status[0] < 6:
        index = 0
    if (x > -250) and (x < -150) and status[1] < 6:
        index = 1
    if (x > -150) and (x < -50) and status[2] < 6:
        index = 2
    if (x > -50) and (x < 50) and status[3] < 6:
        index = 3
    if (x > 50) and (x < 150) and status[4] < 6:
        index = 4
    if (x > 150) and (x < 250) and status[5] < 6:
        index = 5
    if (x > 250) and (x < 350) and status[6] < 6:
        index = 6

    if index != -1:
        place(index, player)
        make_move(board, status, index, 1)
        if evaluate(board) == win:
            print(board)
            write("Congrats, You Won!", -125)
            return
        score, move = negamax(invert_board(board, False), status, 0, search_depth, -inf, inf)
        if move == None:
            print(board)
            write("Well Done, You Tied!", -125)
            return
        place(move, computer)
        print("The computered played at position {}.".format(move))
        make_move(board, status, move, -1)
        if evaluate(board) == lose:
            print(board)
            write("Oh No... You Lost!", -125)
            return
        time.sleep(1)


def draw_grid():
    t.penup()
    t.goto(-350, -300)
    t.pendown()
    t.left(90)
    t.forward(600)
    t.right(90)
    t.forward(700)
    t.right(90)
    t.forward(600)
    t.right(90)
    t.forward(700)
    t.right(90)

    for i in range(6):
        t.penup()
        t.goto(-250 + i * 100, -300)
        t.pendown()
        t.forward(600)

    t.right(90)

    for i in range(5):
        t.penup()
        t.goto(-350, -200 + i * 100)
        t.pendown()
        t.forward(700)


draw_grid()

if not player_start:
    place(3, computer)
    print("The computered played at position {}.".format(3))
    make_move(board, status, 3, -1)

# Bind the mouse click event to the function
turtle.onscreenclick(get_mouse_click)

# Keep the window open
turtle.mainloop()
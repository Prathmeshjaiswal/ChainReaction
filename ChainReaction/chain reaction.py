# code by:prathmesh
# PVP Chain reaction game developed using tkinter

import tkinter as t
import tkinter.font


# resets up the board for new game
def resetBoard():
    turn.set(0)

    # reset notification button
    turnNote.set("It's player " + str(turn.get() + 1) + "'s turn!")

    for x in range(rowSize):
        for y in range(colSize):
            value = 0
            val[x][y] = t.StringVar()
            btn[x][y] = t.Button(frame, textvariable=val[x][y], command=lambda x=x, y=y: add(x, y))
            btn[x][y]["width"] = 6
            btn[x][y]["height"] = 3
            btn[x][y]["bg"] = "black"
            btn[x][y]["fg"] = "white"
            btn[x][y]["activebackground"] = "white"
            btn[x][y]["activeforeground"] = "white"
            btn[x][y]["font"] = helv10
            val[x][y].set(value)
            btn[x][y].grid(row=x, column=y)

        # checks the max size a block can hold


def maxSize(x, y):
    size = 4
    if x == rowSize - 1 or x == 0:
        size = size - 1
    if y == colSize - 1 or y == 0:
        size = size - 1
    return size


# recursive function to expand the blocks of a player based on no of collisions
def expand(x, y):
    if x - 1 >= 0:
        addAtom(x - 1, y)
    if x + 1 <= rowSize - 1:
        addAtom(x + 1, y)
    if y - 1 >= 0:
        addAtom(x, y - 1)
    if y + 1 <= colSize - 1:
        addAtom(x, y + 1)
    return;


# check whether the player can play or not
def canPlay():
    # preliminary test
    if turn.get() < playersCount:
        return True

    for x in range(rowSize):
        for y in range(colSize):
            if btn[x][y]["bg"] == color[turn.get() % playersCount]:
                return True

    return False


# Wrapper function for addAtom which first checks whether the user selected
# valid button and passes the turn to next player after adding atom
def add(x, y):
    # invalid selection by user
    if btn[x][y]["bg"] != color[(turn.get()) % playersCount] and btn[x][y]["bg"] != "black":
        return;

    try:
        addAtom(x, y)

    # if unending recursion occurs
    except RuntimeError:
        print("NOTE: GAME OVER.")

        for a in range(rowSize):
            for b in range(colSize):
                val[a][b].set(maxSize(a, b))
                btn[a][b]["bg"] = color[turn.get() % playersCount]

            declareWinner()
        return;

    passTurn()


# adds an atom if the selection is valid
def addAtom(x, y):
    value = 1 + int(val[x][y].get())
    # termination condition
    if value > maxSize(x, y):
        return;

    # change according to user color
    btn[x][y]["bg"] = color[turn.get() % playersCount]

    if value == maxSize(x, y):
        # need to set before expanding
        btn[x][y]["bg"] = "black"
        val[x][y].set(0)
        expand(x, y)
    else:
        val[x][y].set(value)


# used to pass the turn to next player
def passTurn():
    # increment move if a valid one is made to give chance to next player
    turn.set(turn.get() + 1)
    # keep count of number of passes
    passes = 0

    # pass the turn if player can't play
    while not canPlay():
        passes = passes + 1
        turn.set(turn.get() + 1)

    # if no other player can play
    if passes == playersCount - 1:
        declareWinner()
        return;

    # else modify turn
    nextTurn = (turn.get() % playersCount) + 1
    turnNote.set("It's player " + str(nextTurn) + "'s turn!")


# set notification message to win status
def declareWinner():
    turnNote.set("Player " + str((turn.get() % playersCount) + 1) + " WON!")


# UI design
window = t.Tk()

# required font style
helv10 = tkinter.font.Font(family='Helvetica', size=10, weight='bold')

# variable to toggle turns
turn = t.IntVar()

# Button to reset game
reset = t.Button(window, text="RESET", command=resetBoard).pack()

# String variable to notify which player's turn
turnNote = t.StringVar()
# Label to show turnNote
notify = t.Label(window, font=helv10, textvariable=turnNote).pack()

# frame to organize elements
frame = t.Frame(window)
frame.pack()

# set the dimensions of the board
rowSize = 8
colSize = 6

# set the number of players and assign colors to each one of them(max: seven)
# you can more colors and change player count to grater than seven
playersCount = 2
color = ["red", "indigo", "blue", "lime", "brown", "orange", "violet"]

btn = [[0 for y in range(colSize)] for x in range(rowSize)]
val = [[0 for y in range(colSize)] for x in range(rowSize)]

resetBoard()

window.mainloop()
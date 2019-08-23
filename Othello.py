import numpy as np
import random
import time
import collections
import math
import sys
import pygame
from copy import deepcopy

SIZE = 6

# Class created by Jalen Jackson    
class Stone:
    def __init__(self, row, col, state):
        self.state = state
        self.row = row
        self.col = col

        # Initalize as a dictionary
        self.neighbors = collections.defaultdict(lambda: None)

    # Prints the type of stone
    def __repr__(self):
        return str(self.state)


# Class created by Jalen Jackson
class Board:

    # Initializes the board with two black and two white stones on the middle of the board with size N
    def __init__(self, size):
        self.size = SIZE
        self.stones = [[None] * size for i in range(0, size)]

        for j in range(SIZE):
            for i in range(SIZE):
                self.insert(Stone(i, j, "-"))

        middleLeft = int((self.size / 2) - 1)
        middleRight = int(self.size / 2)

        blackStoneOne = Stone(middleLeft, middleLeft, "B")
        blackStoneTwo = Stone(middleRight, middleRight, "B")
        self.insert(blackStoneOne)
        self.insert(blackStoneTwo)

        whiteStoneOne = Stone(middleLeft, middleRight, "W")
        whiteStoneTwo = Stone(middleRight, middleLeft, "W")
        self.insert(whiteStoneOne)
        self.insert(whiteStoneTwo)

    def count(self, state):
        count = 0
        for j in range(SIZE):
            for i in range(SIZE):
                stone = self.get_stone_at(i, j)
                if stone.state == state:
                    count += 1
        return count

    # Inserts the stone on the board at a specific row & column set in the stone's constructor
    def insert(self, stone):
        self.stones[stone.row][stone.col] = stone

    # Gets the stone at the row and column specified in the function
    def get_stone_at(self, row, col):
        return self.stones[int(row)][int(col)]

    # Returns a dictionary of stones adjacent to the stone specified in the paramter.
    # Key: Returns the direction between the stone and the neighbor
    # Value: Returns the neighbor
    def neighbors_of(self, stone):
        if stone is None:
            return None

        if stone.row - 1 >= 0:
            stone.neighbors.update({"NORTH": self.stones[stone.row - 1][stone.col]})

        if stone.row + 1 < self.size:
            stone.neighbors.update({"SOUTH": self.stones[stone.row + 1][stone.col]})

        if stone.col - 1 >= 0:
            stone.neighbors.update({"WEST": self.stones[stone.row][stone.col - 1]})

        if stone.col + 1 < self.size:
            stone.neighbors.update({"EAST": self.stones[stone.row][stone.col + 1]})

        if stone.row - 1 >= 0 and stone.col - 1 >= 0:
            stone.neighbors.update(
                {"NORTHWEST": self.stones[stone.row - 1][stone.col - 1]}
            )

        if stone.row - 1 >= 0 and stone.col + 1 < self.size:
            stone.neighbors.update(
                {"NORTHEAST": self.stones[stone.row - 1][stone.col + 1]}
            )

        if stone.row + 1 < self.size and stone.col - 1 >= 0:
            stone.neighbors.update(
                {"SOUTHWEST": self.stones[stone.row + 1][stone.col - 1]}
            )

        if stone.row + 1 < self.size and stone.col + 1 < self.size:
            stone.neighbors.update(
                {"SOUTHEAST": self.stones[stone.row + 1][stone.col + 1]}
            )

        return stone.neighbors

    # Prints the board
    def __repr__(self):
        board = "\n\t  Column\nRow\t"
        r = 0

        for c in range(0, self.size):
            board += str(c) + " "
        board += "\n"

        for col in np.array(self.stones):
            board += str(r) + "\t"
            for stone in col:
                board += str(stone) + " "
            board += "\n"
            r += 1
        return board


# Created By Felicia based on algorithm psuedocode
# Input: stone object, int depth, bool maxPlayer
# Output: hueristic value assignments to legal moves for current play
def mini_max(board, depth=2, alpha=-math.inf, beta=math.inf, maxPlayer=True):
    if maxPlayer == True:
        moves = legal_moves(board, "W")
    else:
        moves = legal_moves(board, "B")

    if depth == 0 or moves == None:
        return set_heuristic_value(board)
    elif maxPlayer:
        value = -math.inf
        for move in moves:
            futureBoard = deepcopy(board)
            apply_move(move.row, move.col, "W", futureBoard)

            value = max(value, mini_max(futureBoard, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value
    else:  # minPlayer
        value = math.inf
        for move in moves:
            futureBoard = deepcopy(board)
            apply_move(move.row, move.col, "B", futureBoard)

            value = min(value, mini_max(futureBoard, depth - 1, alpha, beta, True))
            beta = min(beta, value)

            if alpha >= beta:
                break

        return value


def get_user_postion():
    row = int(input("Please Enter a row: "))
    col = int(input("Please Enter a column: "))

    return row, col


# created by Felicia
# Modified by Jalen
def legal_moves(board, player):
    movesList = []
    enemyPieces = []
    if player == "W":
        enemy = "B"
    else:
        enemy = "W"

    # get a list of all of the opponents pieces
    for i in range(SIZE):
        for j in range(SIZE):
            stone = board.get_stone_at(i, j)
            if stone.state == enemy:
                enemyPieces.append(stone)

        # Helper function for my modifications to find the directions of the flank

    def check_directions(neighbors, directionOne, directionTwo):
        if directionOne not in neighbors:
            return

        if directionTwo not in neighbors:
            return

        if neighbors[directionOne].state == player:
            if (
                neighbors[directionTwo].state == "-"
                and neighbors[directionTwo] not in movesList
            ):
                movesList.append(neighbors[directionTwo])
                return
            else:
                while neighbors[directionTwo].state == enemy:
                    moveNeighbors = board.neighbors_of(neighbors[directionTwo])
                    if directionTwo not in moveNeighbors:
                        return

                    if (
                        moveNeighbors[directionTwo].state == "-"
                        and moveNeighbors[directionTwo] not in movesList
                    ):
                        movesList.append(moveNeighbors[directionTwo])
                        return

                    neighbors.update({directionTwo: moveNeighbors[directionTwo]})

        if neighbors[directionTwo].state == player:
            if (
                neighbors[directionOne].state == "-"
                and neighbors[directionOne] not in movesList
            ):
                movesList.append(neighbors[directionOne])
                return
            else:
                while neighbors[directionOne].state == enemy:
                    moveNeighbors = board.neighbors_of(neighbors[directionOne])
                    if directionOne not in moveNeighbors:
                        return

                    if (
                        moveNeighbors[directionOne].state == "-"
                        and moveNeighbors[directionOne] not in movesList
                    ):
                        movesList.append(moveNeighbors[directionOne])
                        return

                    neighbors.update({directionOne: moveNeighbors[directionOne]})

    for stone in enemyPieces:
        check_directions(board.neighbors_of(stone), "NORTH", "SOUTH")
        check_directions(board.neighbors_of(stone), "EAST", "WEST")
        check_directions(board.neighbors_of(stone), "NORTHEAST", "SOUTHWEST")
        check_directions(board.neighbors_of(stone), "NORTHWEST", "SOUTHEAST")

    movesList.sort(key=lambda stone: (stone.row, stone.col))
    return movesList


# Created By James
# Function that places a stone
def place_stone(row, col, board, player):
    newStone = Stone(row, col, player)
    board.insert(newStone)


# Created by Rahin
# Function to check who won
# Jalen fixed error 'board.b[i][j]
def winner(board):
    whites = 0
    blacks = 0
    empty = 0

    for j in range(SIZE):
        for i in range(SIZE):
            if board.get_stone_at(i, j).state == "W":
                whites += 1
            elif board.get_stone_at(i, j).state == "B":
                blacks += 1
            else:
                empty += 1
    if blacks > whites:
        return "Black"
    elif whites > blacks:
        return "White"
    else:
        return "Tie"


# Modified by Felicia
def convert_line(startStone, board):
    enemy = None
    if startStone.state is "B":
        enemy = "W"
    elif startStone.state is "W":
        enemy = "B"

    neighbors = board.neighbors_of(startStone)
    flankStack = list(
        filter(
            lambda stone: stone is not None and stone[1].state == enemy,
            neighbors.items(),
        )
    )
    while len(flankStack) > 0:
        # grab off stack
        flipList = []
        currentFlank = flankStack.pop(0)
        # get the direction
        flankDirection = currentFlank[0]
        # move in that direction
        flankStone = currentFlank[1]

        # change the stone?
        while flankStone.state == enemy:
            flipList.append(flankStone)
            flankStone = flankStone.neighbors.get(flankDirection)

            # Jalen added this in order to check if there is no stone being checked
            if flankStone is None:
                return

        if flankStone.state == startStone.state:
            while flipList:
                currentStone = flipList.pop()
                apply_move(currentStone.row, currentStone.col, startStone.state, board)


def valid(row, col):
    if row >= 0 and row < SIZE and col < SIZE and col >= 0:
        return True
    else:
        return False


def apply_move(row, col, player, board):
    stone = board.get_stone_at(row, col)
    stone.state = player
    board.insert(stone)
    convert_line(stone, board)


# Function created by Felicia
# Finished by Jalen
def set_heuristic_value(board):
    score = 0
    # Evaluate disc count
    score += board.count("W") / 100
    score -= board.count("B") / 100

    # Legal Moves Count
    score += len(legal_moves(board, "W"))
    score -= len(legal_moves(board, "B"))

    # Corners Captured
    topLeftCorner = board.get_stone_at(0, 0)
    topRightCorner = board.get_stone_at(0, SIZE - 1)
    botLeftCorner = board.get_stone_at(SIZE - 1, 0)
    botRightCorner = board.get_stone_at(SIZE - 1, SIZE - 1)

    whiteCornersCaptured = 0
    blackCornersCaptured = 0

    if topLeftCorner.state == "W":
        whiteCornersCaptured += 1
    elif topLeftCorner.state == "B":
        blackCornersCaptured += 1

    if botLeftCorner.state == "W":
        whiteCornersCaptured += 1
    elif botLeftCorner.state == "B":
        blackCornersCaptured += 1

    if topRightCorner.state == "W":
        whiteCornersCaptured += 1
    elif topRightCorner.state == "B":
        blackCornersCaptured += 1

    if botRightCorner.state == "W":
        whiteCornersCaptured += 1
    elif botRightCorner.state == "B":
        blackCornersCaptured += 1

    score += 10 * whiteCornersCaptured
    score -= 10 * blackCornersCaptured

    return score


# TODO
def pick_best_move(moves, board):
    bestMove = random.choice(moves)
    bestValue = -math.inf

    for move in moves:
        futureBoard = deepcopy(board)
        apply_move(move.row, move.col, "W", futureBoard)

        value = mini_max(futureBoard)
        if bestValue > value:
            bestMove = move
            value = bestValue

    return bestMove


    
# Created By Felicia
# input: None
# Controls the game flow
def play_game():
    sys.setrecursionlimit(1000)
    #pygame Added
    pygame.init()
    size = width,height = 800, 600
    green = 46,139,87
    white = 255,255,255
    gray = 192,192,192
    black = 0,0,0
    widthLines = (width)//SIZE
    heightLines = height//SIZE
    square = int(np.sqrt(width*height//(SIZE*SIZE))) #size of each square
    rad = square//4
    shiftR = int(square/2* width/height)
    shiftD = int(square/2* height/width)
    screen= pygame.display.set_mode(size)
    #end of pygame
    
    board = Board(SIZE)
    for i in range(SIZE):
        for j in range(SIZE):
            board.neighbors_of(board.get_stone_at(i, j))
    gameInPlay = True
    # assume Player1 is 'B' stones
    player1 = True
    passedTurn = False

    while gameInPlay:
        #pygame stuff
        screen.fill(green)
        for i in range(SIZE):
            j = i +1
            pygame.draw.line(screen, gray,(widthLines*j, height), (widthLines*j, 0),1 )
        for i in range(SIZE):
            j = i +1
            pygame.draw.line(screen, gray,(width, heightLines*j), (0, heightLines*j),1 )
        
        for i in range(SIZE):
            for j in range(SIZE):
               stone = (board.get_stone_at(i, j))
               if stone.state == 'W':
                   pygame.draw.circle(screen, white, [i*widthLines+shiftR, j*heightLines+shiftD], rad)
               elif stone.state == 'B':
                   pygame.draw.circle(screen, black, [i*widthLines+shiftR, j*heightLines+shiftD], rad)
                       
        pygame.display.flip()
        
        #end of pygame
        print(board)

        moves = []

        print("Black Stones: " + str(board.count("B")))
        print("White Stones: " + str(board.count("W")))

        # players turn
        if player1 == True:
            moves = legal_moves(board, "B")
            for i in moves:
                print(i.row, i.col)
            # no legal moves means player forfeits turn
            if not moves:
                player1 = False
                # if the opposing player was unable to make a move the game is over
                if passedTurn == True:
                    break
                else:
                    passedTurn = True
            # otherwise get input from player
            else:
                position = False
                passedTurn = False
                while position == False:
                    # row, col = get_user_postion()  # return x,y
                    move = random.choice(moves)
                    row = move.row
                    col = move.col

                    time.sleep(2)

                    if valid(row, col):
                        playerMove = board.get_stone_at(row, col)

                        if playerMove in moves:  # if it's a legal move
                            apply_move(playerMove.row, playerMove.col, "B", board)
                            position = True  # next turn
                            player1 = False

        # The Computers turn
        else:
            moves = legal_moves(board, "W")
            for i in moves:
                print(i.row, i.col)
            if not moves:
                if passedTurn == True:
                    break
                else:
                    passedTurn = True
                    player1 = True
            else:
                passedTurn = False

                # pick the highest value
                compMove = pick_best_move(moves, board)

                # TODO need to validate move

                time.sleep(2)

                if valid(compMove.row, compMove.col):
                    apply_move(compMove.row, compMove.col, "W", board)

                    player1 = True

    whoWon = winner(board)
    if whoWon == "Black" or whoWon == "White":
        print(whoWon + " Won")
    else:
        print(whoWon)

    time.sleep(10)

    # TODO do something


if __name__ == "__main__":
    play_game()

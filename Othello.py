import numpy as np
import random
import time
import collections

SIZE = 6
#Class created by Jalen Jackson
class Stone:
    def __init__(self, row, col, state):
        self.state = state
        self.row = row
        self.col = col

    #Initalize as a dictionary
        self.neighbors = collections.defaultdict(lambda : None)

    #Prints the type of stone
    def __repr__(self):
        return str(self.state)

#Class created by Jalen Jackson
class Board:

    #Initializes the board with two black and two white stones on the middle of the board with size N
    def __init__(self, size):
        self.size = SIZE
        self.stones = [[None] * size for i in range(0, size)]

        for j in range(SIZE):
            for i in range(SIZE):
                self.insert(Stone(i, j, '-'))

        middleLeft = int((self.size / 2) - 1)
        middleRight = int(self.size / 2)

        blackStoneOne = Stone(middleLeft, middleLeft, 'B')
        blackStoneTwo = Stone(middleRight, middleRight, 'B')
        self.insert(blackStoneOne)
        self.insert(blackStoneTwo)

        whiteStoneOne = Stone(middleLeft, middleRight, 'W')
        whiteStoneTwo = Stone(middleRight, middleLeft, 'W')
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


    #Inserts the stone on the board at a specific row & column set in the stone's constructor
    def insert(self, stone):
        self.stones[stone.row][stone.col] = stone

    #Gets the stone at the row and column specified in the function
    def get_stone_at(self, row, col):
       return self.stones[int(row)][int(col)]

    #Returns a dictionary of stones adjacent to the stone specified in the paramter.
    #Key: Returns the direction between the stone and the neighbor
    #Value: Returns the neighbor
    def neighbors_of(self, stone):
        if stone is None:
            return None

        if stone.row - 1 >= 0:
            stone.neighbors.update({"NORTH" : self.stones[stone.row - 1][stone.col]})

        if stone.row + 1 < self.size:
            stone.neighbors.update({"SOUTH" : self.stones[stone.row + 1][stone.col]})

        if stone.col - 1 >= 0:
            stone.neighbors.update({"WEST" : self.stones[stone.row][stone.col - 1]})

        if stone.col + 1 < self.size:
            stone.neighbors.update({"EAST" : self.stones[stone.row][stone.col + 1]})

        if stone.row - 1 >= 0 and stone.col - 1 >= 0:
            stone.neighbors.update({"NORTHWEST" : self.stones[stone.row - 1][stone.col - 1]})

        if stone.row - 1 >= 0 and stone.col + 1 < self.size:
            stone.neighbors.update({"NORTHEAST" : self.stones[stone.row - 1][stone.col + 1]})

        if stone.row + 1 < self.size and stone.col - 1 >= 0:
            stone.neighbors.update({"SOUTHWEST" : self.stones[stone.row + 1][stone.col - 1]})

        if stone.row + 1 < self.size and stone.col + 1 < self.size:
            stone.neighbors.update({"SOUTHEAST" : self.stones[stone.row + 1][stone.col + 1]})

        return stone.neighbors

    #Prints the board
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

#Created By Felicia based on algorithm psuedocode
#Input: stone object, int depth, bool maxPlayer
#Output: hueristic value assignments to legal moves for current play
def mini_max(board, piece, depth, maxPlayer):
  if maxPlayer == False:
    moves = legal_moves(board, 'B')
  else:
    moves = legal_moves(board, 'W')

  if depth == 0 or moves == None:
    return set_hueristic_value(piece)
  elif maxPlayer:
    value = -10000
    for i in moves:
      tempVal = mini_max(board, i, depth-1, False)
      if value < tempVal:
        value = tempVal
    return value
  else: #minPlayer
    value = 65
    for i in moves:
      tempVal = mini_max(board, i, depth-1, True)
      if value < tempVal:
        value = tempVal
    return value




def get_user_postion():
  row = int(input("Please Enter a row: "))
  col = int(input("Please Enter a column: "))

  return row, col


#created by Felicia
#Modified by Jalen
def legal_moves(board, player):
  movesList = []
  enemyPieces = []
  if player == 'W':
    enemy ='B'
  else:
    enemy = 'W'


  #get a list of all of the opponents pieces
  for i in range(SIZE):
    for j in range(SIZE):
      stone = board.get_stone_at(i, j)
      if stone.state == enemy:
        enemyPieces.append(stone)

    #Helper function for my modifications to find the directions of the flank
  def check_directions(neighbors, directionOne, directionTwo):
    if directionOne not in neighbors:
        return

    if directionTwo not in neighbors:
        return

    if neighbors[directionOne].state == player:
        if neighbors[directionTwo].state == "-" and neighbors[directionTwo] not in movesList:
            movesList.append(neighbors[directionTwo])
            return
        else:
            while neighbors[directionTwo].state == enemy:
                moveNeighbors = board.neighbors_of(neighbors[directionTwo])
                if directionTwo not in moveNeighbors:
                    return

                if moveNeighbors[directionTwo].state == "-" and moveNeighbors[directionTwo] not in movesList:
                    movesList.append(moveNeighbors[directionTwo])
                    return

                neighbors.update({directionTwo : moveNeighbors[directionTwo]})

  for stone in enemyPieces:
    check_directions(board.neighbors_of(stone), "SOUTH", "NORTH")
    check_directions(board.neighbors_of(stone), "NORTH", "SOUTH")
    check_directions(board.neighbors_of(stone), "EAST", "WEST")
    check_directions(board.neighbors_of(stone), "WEST", "EAST")
    check_directions(board.neighbors_of(stone), "NORTHEAST", "SOUTHWEST")
    check_directions(board.neighbors_of(stone), "SOUTHWEST", "NORTHEAST")
    check_directions(board.neighbors_of(stone), "NORTHWEST", "SOUTHEAST")
    check_directions(board.neighbors_of(stone), "SOUTHEAST", "NORTHWEST")

  return movesList

#created by Felicia Helper Function for legal_moves
''' Not Required Anymore
def get_direction(direction, row, col):
  headTo = ""
  if direction == 'NORTHEAST':
    headTo = 'SOUTHWEST'
    row = row + 1
    col = col - 1
  elif direction == 'SOUTHWEST':
    headTo = 'NORTHEAST'
    row = row - 1
    col = col + 1
  elif direction == 'SOUTH':
    headTo = 'NORTH'
    row = row - 1
  elif direction == 'NORTH':
    headTo = 'SOUTH'
    row = row + 1
  elif direction == 'EAST':
    headTo = 'WEST'
    col = col - 1
  elif direction == 'WEST':
    headTo = 'EAST'
    col = col + 1
  elif direction == 'SOUTHEAST':
    headTo = 'NORTHWEST'
    row = row - 1
    col = col - 1
  elif direction == 'NORTHWEST':
    headTo = 'SOUTHEAST'
    row = row + 1
    col = col + 1
  return headTo, row, col
'''

#Created By James
#Function that places a stone
def place_stone(row, col, board, player):
    newStone = Stone(row, col, player)
    board.insert(newStone)



#Created by Rahin
#Function to check who won
#Jalen fixed error 'board.b[i][j]
def winner(board):
  whites = 0
  blacks = 0
  empty = 0

  for j in range(SIZE):
    for i in range(SIZE):
      if board.get_stone_at(i, j).state == 'W':
          whites += 1
      elif board.get_stone_at(i, j).state == 'B':
          blacks += 1
      else:
          empty += 1
  if blacks > whites:
    return "Black"
  elif whites > blacks:
    return "White"
  else:
    return "Tie"

#Modified by Felicia
def convert_line(startStone, board):
    enemy = None
    if startStone.state is 'B':
        enemy = 'W'
    elif startStone.state is 'W':
        enemy = 'B'

    neighbors = board.neighbors_of(startStone)
    flankStack = list(filter(lambda stone : stone is not None and stone[1].state == enemy, neighbors.items()))
    while len(flankStack) > 0:
        #grab off stack
        flipList = []
        currentFlank = flankStack.pop(0)
        #get the direction
        flankDirection = currentFlank[0]
        #move in that direction
        flankStone = currentFlank[1]

        #change the stone?
        while flankStone.state == enemy:
          flipList.append(flankStone)
          flankStone = flankStone.neighbors.get(flankDirection)

          #Jalen added this in order to check if there is no stone being checked
          if flankStone is None:
            return


        if flankStone.state == startStone.state:
          while flipList:
            currentStone = flipList.pop()
            apply_move(currentStone, startStone.state, board)

        #nextFlank = list(filter(lambda stone : stone[0] == flankDirection and stone[1].state == enemy, board.neighbors_of(flankStone).items()))
        #flankStack = nextFlank


def valid(row,col):

  if row >= 0 and row < SIZE and col < SIZE and col >= 0:
    return True
  else:
    return False

#TODO
def check_for_win(board):
  pass
#TODO

def apply_move(currentStone, player, board):
    stone = board.get_stone_at(currentStone.row, currentStone.col)
    stone.state = player
    board.insert(stone)

#TODO
def set_hueristic_value(currentStone):
  return 1

#TODO
def pick_best_move(moves):
    move = random.choice(moves)
    return move
#TODO a function to determine who goes 1st
#now - human is always black and comp is white <- hardcoded in for testing ATM

#Created By Felicia
#input: None
#Controls the game flow
def play_game():

  board = Board(SIZE)
  for i in range(SIZE):
      for j in range(SIZE):
        board.neighbors_of(board.get_stone_at(i,j))
  gameInPlay = True
  #assume Player1 is Human and moving 'B' the blackstones
  player1 = True
  passedTurn = False

  while gameInPlay:
    print(board)

    moves = []

    print("Black Stones: " + str(board.count('B')))
    print("White Stones: " + str(board.count('W')))

    #players turn
    if player1 == True:
      moves = legal_moves(board, 'B')
      for i in moves:
        print(i.row, i.col)
      #no legal moves means player forfeits turn
      if not moves:
        player1 = False
        #if the opposing player was unable to make a move the game is over
        if passedTurn == True:
          break
        else:
          passedTurn = True
    #otherwise get input from player
      else:
        position = False
        passedTurn = False
        while position == False:
          row,col = get_user_postion() #return x,y
          if valid(row,col):
            playerMove = board.get_stone_at(row, col)

            if playerMove in moves: #if it's a legal move
              apply_move(playerMove, 'B', board)
              convert_line(playerMove, board)
              position = True #next turn
              player1 = False

    #The Computers turn
    else:
      moves = legal_moves(board, 'W')
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
        #asign hueristics
        for i in moves:
          newBoard = board
          #mini_max(newBoard, i, 3, True)


        #pick the highest value
        compMove = pick_best_move(moves)

        #TODO need to validate move

        time.sleep(2)

        if valid(compMove.row, compMove.col):
          apply_move(compMove, 'W', board)
          convert_line(compMove, board)

          player1 = True

  whoWon = winner(board)
  if whoWon == "Black" or whoWon == "White":
    print(whoWon + " Won")
  else:
    print(whoWon)


  #TODO do something

if __name__ == "__main__":
    play_game()

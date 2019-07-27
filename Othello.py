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

        self.flankDirection = ""

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
  #THE COMPUTER IS MAX
  if maxPlayer == False:
    player = 'B'
  else:
    player = 'W'
  #TAKES A DUMMY BOARD AND PLAYS THE NEXT POSSIBLE MOVES
  moves = legal_moves(board, player)
  apply_move(piece, player, board)
  #GETS THE NUMBER OF PIECES IN SAID MOVE and stores it in a variable
  tempValue = convert_line(piece, board)
  #END OF RECURSION (MOVE LIST IS EMPTY or we went as deep as we wanted ?? Only test a few moves)
  if depth == 0 or moves == None:
    return tempValue
    #The computer places a piece
  elif maxPlayer:
    value = tempValue
    for i in moves:
      tempVal = mini_max(board, i, depth-1, False)
      if value < tempVal:
        value = tempVal
    return value
  else: #minPlayer
    value = tempValue
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
    if neighbors[directionOne] is None or neighbors[directionTwo] is None:
        return

    if neighbors[directionOne].state is player:
        while neighbors[directionTwo] is not "-" and neighbors[directionTwo] is enemy:
            moveNeighbors = board.neighbors_of(neighbors[directionTwo])
            neighbors.update({directionTwo : moveNeighbors[directionTwo]})

        if neighbors[directionTwo] not in movesList:
            movesList.append(neighbors[directionTwo])

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


#Created By James
#Function that places a stone
def place_stone(row, col, board, player):
    newStone = Stone(row, col, player)
    board.insert(newStone)



#Created by Rahin
#Function to check who won
def winner(board):
  whites = 0
  blacks = 0
  empty = 0

  for i in range(SIZE):
    for j in range(SIZE):
      if board.b[i][j] == 'W':
          whites += 1
      elif board.b[i][j] == 'B':
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
#Created by Jalen
def convert_line(startStone, board):
    enemy = None
    if startStone.state is 'B':
        enemy = 'W'
    elif startStone.state is 'W':
        enemy = 'B'
    #Counts the number of stones flipped for hueristic
    count = 0
    neighbors = board.neighbors_of(startStone)
    flankStack = list(filter(lambda stone : stone is not None and stone[1] is not None and stone[1].state == enemy, neighbors.items()))
    while len(flankStack) > 0:
        #grab off stack
        flipList = []
        currentFlank = flankStack.pop(0)
        #get the direction
        flankDirection = currentFlank[0]
        #move in that direction
        flankStone = currentFlank[1]

        while(flankStone is not None and flankStone.state == enemy):
          flipList.append(flankStone)
          flankStone = flankStone.neighbors.get(flankDirection)
        if flankStone is not None and flankStone.state == startStone.state:
          while flipList:
            currentStone = flipList.pop()
            apply_move(currentStone, startStone.state, board)
            count = count + 1
    return count

    


def valid(row,col):

  if row >= 0 and row < SIZE and col < SIZE and col >= 0:
    return True
  else:
    return False



#Modified by Felicia
#Create by James
def apply_move(currentStone, player, board):
    stone = board.get_stone_at(currentStone.row, currentStone.col)
    stone.state = player
    board.insert(stone)


def pick_best_move(values, moves):
    #move = random.choice(moves)
    tempVal = 0
    for i in range(len(values)):
      if values[i] > tempVal:
        tempVal = values[i]
        move = moves[i]
    return move


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
              dummy = convert_line(playerMove, board)
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
        movesValues = []
        
        for i in moves:
          #Create dummy boards to perserve original board state
          newBoard = Board(SIZE)
          for x in range(SIZE):
            for y in range(SIZE):
              dummyPiece = board.get_stone_at(x,y)
              newBoard.get_stone_at(x,y).state = dummyPiece.state
          val = mini_max(newBoard, i, 3, True)
          movesValues.append(val)
          print("Hueristic Value ", val, i.row, i.col, )


        #pick the highest value
        compMove = pick_best_move(movesValues, moves)
        print("Choosen Position", compMove.row, compMove.col)

        if valid(compMove.row, compMove.col):
          apply_move(compMove, 'W', board)
          dummy = convert_line(compMove, board)

          player1 = True

  theWinner = winner(board)

  '''
  TODO
  Testing
  Remove Test print
  Display helper Test i.e When outputing the possible moves let user know? W/e
  Display Winner
  '''

if __name__ == "__main__":
    play_game()

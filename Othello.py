import numpy as np

#Class created by Jalen Jackson
class Stone:
    def __init__(self, row, col, state):
        self.state = state
        self.row = row
        self.col = col

	#Initalize as a dictionary
        self.neighbors = {}

    #Prints the type of stone
    def __repr__(self):
        return str(self.state)

#Class created by Jalen Jackson
class Board:

    #Initializes the board with two black and two white stones on the middle of the board with size N
    def __init__(self, size):
        self.size = size
        self.stones = [[None] * size for i in range(0, size)]
        
        for j in range(size):
            for i in range(size):
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
            
    #Inserts the stone on the board at a specific row & column set in the stone's constructor
    def insert(self, stone):
        self.stones[stone.row][stone.col] = stone

    #Gets the stone at the row and column specified in the function
    def get_stone_at(self, row, col):
       return self.stones[int(row)][int(col)]

    #Returns a dictionary of stones adjacent to the stone specified in the paramter.
    #Key: Returns the direction between the stone and the neighbor
    #Value: Returns the neighbor
    #Felicia NORTH AND SOUTH MIXED
    def neighbors_of(self, stone):
        if stone.row - 1 >= 0:
            stone.neighbors.update({"SOUTH" : self.stones[stone.row - 1][stone.col]})

        if stone.row + 1 < self.size:
            stone.neighbors.update({"NORTH" : self.stones[stone.row + 1][stone.col]})

        if stone.col - 1 >= 0:
            stone.neighbors.update({"WEST" : self.stones[stone.row][stone.col - 1]})

        if stone.col + 1 < self.size:
            stone.neighbors.update({"EAST" : self.stones[stone.row][stone.col + 1]})

        if stone.row - 1 >= 0 and stone.col - 1 >= 0:
            stone.neighbors.update({"SOUTHWEST" : self.stones[stone.row - 1][stone.col - 1]})

        if stone.row - 1 >= 0 and stone.col + 1 < self.size:
            stone.neighbors.update({"SOUTHEAST" : self.stones[stone.row - 1][stone.col + 1]})

        if stone.row + 1 < self.size and stone.col - 1 >= 0:
            stone.neighbors.update({"NORTHWEST" : self.stones[stone.row + 1][stone.col - 1]})

        if stone.row + 1 < self.size and stone.col + 1 < self.size:
            stone.neighbors.update({"NORTHEAST" : self.stones[stone.row + 1][stone.col + 1]})
        
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
  row = input("Please Enter a row: ")
  col = input("Please Enter a column: ")
  return row, col

#created by Felicia # TODO issue with edge of game
def legal_moves(board, player):
  movesList = []
  opPosition = []
  endList = []
  size = 6
  if player == 'W':
    oppPlayer ='B'
  else:
    oppPlayer = 'W'
    #get a list of all of the opponents pieces
  for i in range(size):
    for j in range(size):
      stone = board.get_stone_at(i, j)
      if stone.state == oppPlayer:
        opPosition.append(stone)
  #i is a tile with an opponents stone
  for i in opPosition:
    #a list of every direction 
    for pieceDir, pieceVal in i.neighbors.items():
      #indicates empty space next to opponents piece 
      if pieceVal.state == '-':
        #search for flank
        #set our current piece in position
        d, row, col = get_direction(pieceDir, i.row,i.col)
        temp = board.get_stone_at(row, col)
        
        if temp.state != '_':
          while temp.state == oppPlayer and temp.row < size and temp.col < size:
            d, row, col = get_direction(pieceDir, temp.row,temp.col)
            temp = board.get_stone_at(row, col)
          if temp.state == player:
            #appends the original move as valid
            movesList.append(pieceVal)
            #appends the ending position for flipping of pieces later
            endList.append(temp)
            

  return movesList, endList

#created by Felicia Helper Function for legal_moves
def get_direction(direction, row, col):
  headTo = ""
  if direction == 'SOUTHEAST':
    headTo = 'NORTHWEST'
    row = row + 1
    col = col - 1
  elif direction == 'NORTHWEST':
    headTo = 'SOUTHEAST'
    row = row - 1
    col = col + 1
  elif direction == 'NORTH':
    headTo = 'SOUTH'
    row = row - 1
  elif direction == 'SOUTH':
    headTo = 'NORTH'
    row = row + 1
  elif direction == 'EAST':
    headTo = 'WEST'
    col = col - 1
  elif direction == 'WEST':
    headTo = 'EAST'
    col = col + 1
  elif direction == 'NORTHEAST':
    headTo = 'SOUTHWEST'
    row = row - 1
    col = col - 1
  elif direction == 'SOUTHWEST':
    headTo = 'NORTHEAST'
    row = row + 1
    col = col + 1
  return headTo, row, col

#Created By James
#Function that places a stone
def place_stone(row, col, board, player):
    newStone = Stone(row, col, player)
    board.insert(newStone)

#Created By James
#Function that converts a row
#TODO: make it work for diagonals
def convert_line(begRow, begCol, endRow, endCol, board, player):
    print(begRow, begCol, endRow, endCol)
    if begRow is endRow:
        num = begCol + 1
        while (num != endCol):
            #newStone = Stone(begRow, num, player)
            #board.insert(newStone)
            piece = board.get_stone_at(begRow, num)
            piece.state = player
            num += 1
    if begCol is endCol:
        num = begRow + 1
        while (num != endRow):
            #newStone = Stone(num, begCol, player)
            #board.insert(newStone)
            piece = board.get_stone_at(num, begCol)
            piece.state = player
            num += 1

#Created by Rahin
#Function used to count the number of black and white stones
def count_stones(self):
  whites = 0
  blacks = 0
  empty = 0
  size = 6
  for i in range(size):
    for j in range(size):
      if self.board[i][j] == 'W':
          whites += 1
      elif self.board[i][j] == 'B':
          blacks += 1
      else:
          empty += 1
  return whites, blacks, empty

#TODO
def set_hueristic_value(currentStone):
  return 1

#TODO 
def pick_best_move(moves):
  return moves[0]
#TODO a function to determine who goes 1st 
#now - human is always black and comp is white <- hardcoded in for testing ATM

#Created By Felicia
#input: None
#Controls the game flow
def play_game():
  size = 6
  board = Board(size)
  for i in range(size):
    for j in range(size):
      board.neighbors_of(board.get_stone_at(i,j))
  gameInPlay = True
  #assume Player1 is Human and moving 'B' the blackstones
  player1 = False
  passedTurn = False
  
  while gameInPlay:
    print(board)
    moves = []
    #endpieces is a list of pieces that correspond with legal_moves    may not need
    endpieces = []
    #players turn
    if player1 == True:
      piece = board.get_stone_at(2,1)
      print(piece)
      moves, endpieces = legal_moves(board, 'B')
      for i in moves:
        print(i.row, i.col, i.state)
      print(moves)
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
          rowStr,colStr = get_user_postion() #return x,y
          row = rowStr
          col = colStr
          if row < size and col < size and row >=0 and col >=0: #if it's valid
            playerMove = board.get_stone_at(row, col)     
            if playerMove in moves: #if it's a legal move
              place_stone(row, col, board, 'B')
              indices = [i for i, x in enumerate(moves) if x == playerMove]
              #TODO the indices of moves matches those in endpieces this should get multiple directions
              for i in indices:
                endPiece = endpieces[i]
                convert_line(playerMove.row, playerMove.col, endPiece.row, endPiece.col, board, 'B')
              position = True #next turn
              player1 = False

    #The Computers turn      
    else:
      moves, endpieces = legal_moves(board, 'W')
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
          mini_max(newBoard, i, 3, True)


        #pick the highest value
        compMove = pick_best_move(moves)
        #TODO need to validate move 
        
        place_stone(compMove.row, compMove.col, board, 'W')
        indices = [i for i, x in enumerate(moves) if x == compMove]
        #TODO the indices of moves matches those in endpieces this should get multiple directions
        for i in indices:
          endPiece = endpieces[i]
          convert_line(compMove.row, compMove.col, endPiece.row, endPiece.col, board, 'W')
                
        player1 = True

  #white, black, blank = count_stones(board)
  #TODO do something 
      


if __name__ == "__main__":
    play_game()

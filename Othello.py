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
        return self.stones[row][col]

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
        board = "\t"
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
        
    
    '''
    #Activity 2.2
    def depth_first_search(self, hayState):
        openList = [self.startHay]
        closedList = []
        paths = [];

        while openList != []:
            currentHay = openList.pop(0)
            
            if currentHay.state is hayState:
                hay = currentHay
                path = [];
                while hay is not self.startHay:
                    path.append(hay)
                    hay = hay.previousHay
                path.append(self.startHay)
                path.reverse()
                paths.append(path)
            else:
                closedList.insert(0, currentHay)
                neighborsList = list(filter(lambda hay: hay is not None, self.neighbors_of(currentHay)))
                neighborsList = list(filter(lambda hay: hay not in openList, neighborsList))
                neighborsList = list(filter(lambda hay: hay not in closedList, neighborsList))
                for hay in neighborsList:
                    hay.previousHay = currentHay
                    openList.insert(0, hay)

        
        if paths is not []:
            direction = ""
            paths.sort(key=lambda path: len(path))
            shortestPath = paths[0]
            for i in range(0, len(shortestPath) - 1):
                currentHay = shortestPath[i]
                nextHay = shortestPath[i + 1]

                if currentHay.northHay is nextHay:
                    direction += 'N'
                elif currentHay.southHay is nextHay:
                    direction += 'S'
                elif currentHay.westHay is nextHay:
                    direction += 'W'
                elif currentHay.eastHay is nextHay:
                    direction += 'E'

            return direction
        else:
            return "CAN'T FIND " + hayState
    '''
                
if __name__ == "__main__":
    board = Board(6)
    print(board)

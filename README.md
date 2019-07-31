# Othello
Our Othello is a board game with two stones played inside a console on a 6 x 6 board. There are 18 **'B'** stones and 18 **'W'** stones that each player must take turns placing them on the board. For every turn, a player must put each stone in a position where it can flip their opponent's disc over. Once all 36 stones are used, a winner is determined based on the most amount of stones a player has placed on the board.

# Developers
1. **Jalen Jackson**
   1. Introduced the game to the team
   2. Created classes stone and board creation
   3. Implementation of mini_max and hueristics and finalized implementation 
2. **Felicia**
   1. Design and modularization of program functionality
   2. Initial implementation of Legal_Moves function and rough creation of AI
   3. Cooperative bug fixes and function implementation
3. **Rahin**
   1. Created initial implentation to determine winner
   1. Design contribution
   1. Testing and finding bugs and errors
4. **James**
   1. Initial implementation of apply_piece
   1. Design contribution and determined the hueristics values
   1. Testing and finding bugs and errors
   
# Technical implementation
Provide a general discussion on the data structures and algorithms that were used to achieve the goals of the project

Othello will use the **minimax alogrithm** for the AI in order to get the best move against the player.

The heuristics for the algorithm is going to be based on:
   1. How many pieces the AI has compared to the player?
   2. How many AI pieces can the player not flip?
   3. How much corners the AI has?
The leaf node will occur in the minimax algorithm when the player wins or loses. 

# Usage
Our game will requires python 3 and numpy to run.
for numpy install instruction, read documentation here https://www.scipy.org/install.html

**For Windows**
   1. open directory with Othello.py using the terminal.
   2. run "py Othello.py" in your terminal.
   2. Play the game :)
   
 **For Mac**
   1. open directory with Othello.py using the terminal.
   2. run "python3 Othello.py" in your terminal.
   2. Play the game :)

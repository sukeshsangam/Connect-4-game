import random
import os
import time
from minimax import Minimax

class Game(object):
    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    game_name = "Connecter 4"
    colors = ["x", "o"]
    
    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None
        os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        print("Welcome to {0}".format(self.game_name))
        print("Should Player 1 be a Human or a Computer?")
        while self.players[0] == None:
            choice = str(input("Type 'H' or 'C': "))
            if choice == "Human" or choice.lower() == "h":
                self.players[0] = Player("Human", self.colors[0])
            elif choice == "Computer" or choice.lower() == "c":
                diff = int(input("Enter difficulty for this AI (1 - 5) "))
                self.players[0] = AIPlayer("computer", self.colors[0], diff+1)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[0].name, self.colors[0]))
        while self.players[1] == None:
            if choice == "Computer" or choice.lower() == "c":
                self.players[1] = Player("Human", self.colors[1])
            elif choice == "human" or choice.lower() == "h":
                diff = int(input("Enter difficulty for this AI (1 - 5) "))
                self.players[1] = AIPlayer("computer", self.colors[1], diff+1)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[1].name, self.colors[1]))
        self.turn = self.players[0]
        
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')
    
    def newGame(self):
        self.round = 1
        self.finished = False
        self.winner = None
        self.turn = self.players[0]
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
        self.round += 1

    def nextMove(self):
        player = self.turn
        if self.round > 42:
            self.finished = True
            return
        move = player.move(self.board)

        for i in range(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFours()
                self.printState()
                return
        print("Invalid move (column is full)")
        return
    
    def checkForFours(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        print(slope)
                        self.finished = True
                        return
        
    def verticalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
    
        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
    
        return fourInARow
    
    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
        
        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow
    
    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1
            
        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope
    
    def findFours(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    if self.verticalCheck(i, j):
                        self.highlightFour(i, j, 'vertical')
                    if self.horizontalCheck(i, j):
                        self.highlightFour(i, j, 'horizontal')
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        self.highlightFour(i, j, 'diagonal', slope)
    
    def highlightFour(self, row, col, direction, slope=None):
        if direction == 'vertical':
            for i in range(4):
                self.board[row+i][col] = self.board[row+i][col].upper()
        
        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col+i] = self.board[row][col+i].upper()
        
        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row+i][col+i] = self.board[row+i][col+i].upper()
        
            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row-i][col+i] = self.board[row-i][col+i].upper()
        
        else:
            print("Error - Cannot enunciate four-of-a-kind")
    
    def printState(self):
        os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        print("".format(self.game_name))
        print("Round: " + str(self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")
                
class Player(object):
    type = None 
    name = None
    color = None
    def __init__(self, name, color):
        self.type = "Human"
        self.name = name
        self.color = color
    
    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        column = None
        while column == None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column


class AIPlayer(Player):   
    difficulty = None
    def __init__(self, name, color, difficulty=5):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        
    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        m = Minimax(state)
        best_move, value = m.bestMove(self.difficulty, state, self.color)
        return best_move





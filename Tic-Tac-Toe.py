board = [" " for x in range(10)]
# board is now: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
def insertLetter(letter, pos):
    #Adds the chosen letter to the chosen position
    board[pos] = letter

def spaceIsFree(pos):
    #returns true if the position on the board is empty and false if it isn't
    return board[pos] == " "
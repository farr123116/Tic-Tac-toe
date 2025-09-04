board = [" " for x in range(10)]
# board is now: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
def insertLetter(letter, pos):
    #adds the chosen letter to the chosen position
    board[pos] = letter

def spaceIsFree(pos):
    #returns true if the position on the board is empty and false if it isnt
    return board[pos] == " "
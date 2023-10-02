import cv2
import gameLogic
import pieceFinder
import computerMove
import display


def game():
    videoStream = cv2.VideoCapture(0)
    compOrder = display.displayMenu(videoStream)
    # indicates if one of the players is a computer, and whether they play first or second
    currentTurn = 1
    # 1 is player 1 turn, 2 is player 2 turn
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    # 1 is player 1
    # 2 is player 2
    # 0 is empty
    endgameWinner = 0
    while endgameWinner == 0:
        validMoves = gameLogic.getMoves(board, currentTurn)
        # displays the board then runs a turn
        display.displayBoard(board, validMoves, currentTurn, compOrder)
        runTurn(board, currentTurn, compOrder, videoStream, validMoves)
        # swaps the turns
        currentTurn = abs(currentTurn - 2) + 1
        endgameWinner = gameLogic.checkEndGame(board)
    display.displayBoard(board, [], currentTurn, compOrder)
    display.displayEndgame(endgameWinner)


def runTurn(board, currentTurn, compOrder, videoStream, validMoves):
    # checks whether the player whose turn it is has any valid moves to make
    if len(validMoves):
        print(validMoves)
        # gets the move for the computer if it is the computers turn, or the player if it is the player's turn
        if compOrder == currentTurn:
            moveToMake = computerMove.makeComputerTurn(board, currentTurn, validMoves)
        else:
            moveToMake = pieceFinder.makePlayerTurn(validMoves, videoStream)
        # alters the board file for the decided move
        gameLogic.flipTiles(board, currentTurn, moveToMake)


while True:
    game()

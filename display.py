from PIL import Image
import cv2
import gameLogic
import pieceFinder


def displayBoard(board, validMoves, currentTurn, compOrder):
    # creates variables for each image file
    screenImage = Image.open("assets/screenImage.png")
    blackTileImage = Image.open("assets/blackTile.png")
    whiteTileImage = Image.open("assets/whiteTile.png")
    blackPossibleTileImage = Image.open("assets/blackPossibleTile.png")
    whitePossibleTileImage = Image.open("assets/whitePossibleTile.png")
    scorePlayers = Image.open("assets/scoreboard2Player.png")
    scoreComputer1 = Image.open("assets/scoreboardComputer1.png")
    scoreComputer2 = Image.open("assets/scoreboardComputer2.png")
    # pastes the relevant scoreboard on the display
    scoreBoardPosition = (2080, 400)
    if compOrder == 0:
        screenImage.paste(scorePlayers, scoreBoardPosition, scorePlayers)
    elif compOrder == 1:
        screenImage.paste(scoreComputer1, scoreBoardPosition, scoreComputer1)
    elif compOrder == 2:
        screenImage.paste(scoreComputer2, scoreBoardPosition, scoreComputer2)
    # offset of tile positions, and distance between them
    yOffset = 88
    xOffset = 568
    width = 187
    # iterates through all 64 coordinates, adding tiles to the board
    for x in range(8):
        for y in range(8):
            counterPosition = (xOffset + x * width, yOffset + y * width)
            if board[y][x] == 1:
                screenImage.paste(whiteTileImage, counterPosition, whiteTileImage)
            elif board[y][x] == 2:
                screenImage.paste(blackTileImage, counterPosition, blackTileImage)
    # iterates through the list of possible moves, adds an indicator on those positions to the board
    for validMove in validMoves:
        counterPosition = (xOffset + validMove[0] * width, yOffset + validMove[1] * width)
        if currentTurn == 1:
            screenImage.paste(whitePossibleTileImage, counterPosition, whitePossibleTileImage)
        if currentTurn == 2:
            screenImage.paste(blackPossibleTileImage, counterPosition, blackPossibleTileImage)
    # paste the scores into the scoreboard on the image
    displayScore(board, 1, screenImage, scoreBoardPosition)
    displayScore(board, 2, screenImage, scoreBoardPosition)
    # displays the image
    screenImage.save("assets/currentDisplay.png")
    cv2Image = cv2.imread('assets/currentDisplay.png')
    cv2.imshow("Reversi", cv2Image)
    cv2.waitKey(1)


def displayScore(board, playerIndex, screenImage, scoreBoardPosition):
    # array containing the images for each number, in both colours
    numberImages = [
        # black numbers
        [Image.open('assets/w0.png'), Image.open('assets/w1.png'),
         Image.open('assets/w2.png'), Image.open('assets/w3.png'),
         Image.open('assets/w4.png'), Image.open('assets/w5.png'),
         Image.open('assets/w6.png'), Image.open('assets/w7.png'),
         Image.open('assets/w8.png'), Image.open('assets/w9.png'), ],
        # white numbers
        [Image.open('assets/b0.png'), Image.open('assets/b1.png'),
         Image.open('assets/b2.png'), Image.open('assets/b3.png'),
         Image.open('assets/b4.png'), Image.open('assets/b5.png'),
         Image.open('assets/b6.png'), Image.open('assets/b7.png'),
         Image.open('assets/b8.png'), Image.open('assets/b9.png'), ]

    ]
    # splits the score into digits
    score = str(gameLogic.checkScore(board, playerIndex))
    # variables for letter positioning
    xOffset = scoreBoardPosition[0] + 377
    yOffset = scoreBoardPosition[1] + 44
    height = 110
    digitDisplacement = 28
    # iterates through digits, to accommodate for single-digit and double-digit scores
    for digit in range(len(score)):
        digitToPaste = numberImages[playerIndex - 1][int(score[digit])]
        digitPosition = (xOffset + digit * digitDisplacement - (len(score) - 1) * 14, yOffset + (playerIndex - 1) * height)
        screenImage.paste(digitToPaste, digitPosition, digitToPaste)


def displayMenu(videoStream):
    # displays the menu screen image
    menuScreen = cv2.imread('assets/menuScreen.png')
    cv2.imshow("Reversi", menuScreen)
    cv2.waitKey(1)
    compOrder = pieceFinder.readMenu(videoStream)
    return compOrder


def displayEndgame(endgameWinner):

    blackWin = Image.open('assets/blackWin.png')
    whiteWin = Image.open('assets/whiteWin.png')
    tie = Image.open('assets/tie.png')
    currentDisplay = Image.open('assets/currentDisplay.png')
    # picks an image to paste in based on game outcome
    pasteWinner = tie
    if endgameWinner == 1:
        pasteWinner = whiteWin
    elif endgameWinner == 2:
        pasteWinner = blackWin
    currentDisplay.paste(pasteWinner, (2080, 700), pasteWinner)
    currentDisplay.save("assets/currentDisplay.png")
    # displays the image
    cv2Image = cv2.imread('assets/currentDisplay.png')
    cv2.imshow("Reversi", cv2Image)
    cv2.waitKey(10000)

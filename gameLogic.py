import copy


def checkScore(board, playerToCheck):
    # adds a point for every tile of the *
    count = 0
    for row in board:
        for tile in row:
            if tile == playerToCheck:
                count += 1

    return count


def checkEndGame(board):
    # function determines whether the game is over, and which player wins, or tie
    player1Score = checkScore(board, 1)
    player2Score = checkScore(board, 2)
    # endgame conditions, if the board is full or if neither player has available moves to make
    boardFull = True
    for row in board:
        if 0 in row:
            boardFull = False
    noMoves = not (getMoves(board, 1) or getMoves(board, 2))
    endGame = noMoves or boardFull
    endGameWinner = 0
    if endGame:
        if player1Score == player2Score:
            endGameWinner = 3
        elif player1Score > player2Score:
            endGameWinner = 1
        else:
            endGameWinner = 2
    # 0: continue
    # 1: player 1 win
    # 2: player 1 win
    # 3: tie

    return endGameWinner


def getMoves(board, currentTurn):
    # iterates all positions on the board and checks if it is a valid move
    validMoves = []
    for x in range(8):
        for y in range(8):
            if board[y][x] == 0 and checkValid(board, currentTurn, [x, y]):
                validMoves.append((x, y))
    return validMoves


def checkValid(board, currentTurn, movePosition):
    # creates 2 copies of the boards to alter
    controlBoard = copy.deepcopy(board)
    flippedBoard = copy.deepcopy(board)
    # checks if making a move there actually changes anything
    controlBoard[movePosition[1]][movePosition[0]] = currentTurn
    flipTiles(flippedBoard, currentTurn, movePosition)
    valid = controlBoard != flippedBoard
    return valid


def flipTiles(board, currentTurn, movePosition):
    board[movePosition[1]][movePosition[0]] = currentTurn
    # function flips tiles in each of the 8 directions
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                flipDirection(board, x, y, movePosition, currentTurn)


def flipDirection(board, xIncrement, yIncrement, movePosition, currentTurn):
    spacesInBoard = [0, 1, 2, 3, 4, 5, 6, 7]
    endReached = False
    xIteration = movePosition[0] + xIncrement
    yIteration = movePosition[1] + yIncrement
    # iterate in the direction
    count = 0
    while xIteration in spacesInBoard and yIteration in spacesInBoard and not endReached:
        if board[yIteration][xIteration] == 0:
            endReached = True
        elif board[yIteration][xIteration] == currentTurn:
            for back in range(count, 0, - 1):
                board[yIteration - yIncrement * back][xIteration - xIncrement * back] = currentTurn

            endReached = True
        else:
            xIteration += xIncrement
            yIteration += yIncrement
            count += 1

    board[movePosition[1]][movePosition[0]] = currentTurn

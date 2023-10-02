import copy
import random

import gameLogic


def makeComputerTurn(board, currentTurn, validMoves):
    # creates a test board based on each possible move
    rankedMoves = []
    for move in validMoves:
        testBoard = copy.deepcopy(board)
        gameLogic.flipTiles(testBoard, currentTurn, move)
        # evaluates the board's "value"
        testBoardValue = checkBoardValue(testBoard, currentTurn)
        rankedMoves.append((move, testBoardValue))
    # sort moves by value then returns the best one
    rankedMoves.sort(key=lambda x: x[1])
    return rankedMoves[len(rankedMoves) - 1][0]


def checkBoardValue(board, currentTurn):
    # returns a value for the "worth" of a full reversi board, for a given player
    oppTurn = abs(currentTurn - 2) + 1
    # call functions that give scores based on various factors of preferable situations
    counterDifferenceScore = checkCounterDifference(board, currentTurn, oppTurn)
    actualMobilityScore = checkActualMobilityScore(board, currentTurn, oppTurn)
    potentialMobilityScore = checkPotentialMobilityScore(board, oppTurn, currentTurn)
    stabilityScore = checkStabilityScore(board, currentTurn, oppTurn)
    cornerClosenessScore = checkCornerCloseness(board, currentTurn, oppTurn)
    cornerOccupationScore = checkCornerOccupancy(board, currentTurn, oppTurn)
    # weighting of each of these weightings to the final score
    boardValue = counterDifferenceScore * 8000 + actualMobilityScore * 5000 + stabilityScore * 6000 \
        + potentialMobilityScore * 2000 + cornerOccupationScore * 5000000 \
        + cornerClosenessScore * 100000 + random.random()
    return boardValue


def checkCounterDifference(board, currentTurn, oppTurn):
    # returns difference of score divided by the total number of placed tiles
    currentScore = gameLogic.checkScore(board, currentTurn)
    oppScore = gameLogic.checkScore(board, oppTurn)
    return (currentScore - oppScore) / (currentScore + oppScore)


def checkActualMobilityScore(board, currentTurn, oppTurn):
    # returns the difference of possible moves by each player divided by the total possible moves by either player
    opponentMobility = len(gameLogic.getMoves(board, oppTurn))
    currentMobility = len(gameLogic.getMoves(board, currentTurn))
    if opponentMobility + currentMobility != 0:
        return (currentMobility - opponentMobility)/(currentMobility + opponentMobility)
    else:
        return 0


def checkPotentialMobilityScore(board, oppTurn, currentTurn):
    # returns the total number of empty spaces next to unstable opponent tiles
    potentialMobility = 0
    spacesInBoard = [0, 1, 2, 3, 4, 5, 6, 7]
    # iterates all 64 coordinates, checks for blank
    for x in range(8):
        for y in range(8):
            if board[y][x] == 0:
                # checks each of the 8 directions
                for xDirection in range(-1, 2):
                    for yDirection in range(-1, 2):
                        xCheck = x + xDirection
                        yCheck = y + yDirection
                        if (xDirection != 0 or yDirection != 0) and yCheck in spacesInBoard and xCheck in spacesInBoard:
                            # checks for unstable opponent tiles
                            if board[yCheck][xCheck] == oppTurn \
                                    and not isStable(board, (xCheck, yCheck)):
                                potentialMobility += 1
                            elif board[yCheck][xCheck] == currentTurn \
                                    and not isStable(board, (xCheck, yCheck)):
                                potentialMobility -= 1
    return potentialMobility


def isStable(board, position):
    # function returns whether a
    cornerIndexes = [0, 7]
    spacesInBoard = [0, 1, 2, 3, 4, 5, 6, 7]
    tileSelected = board[position[1]][position[0]]
    oppTile = abs(tileSelected - 2) + 1
    if position[0] in range(1, 7) and position[1] in range(1, 7):
        return False
    elif position[0] in cornerIndexes and position[1] in cornerIndexes:
        return True
    else:
        xIncrement = 0
        yIncrement = 0
        if position[0] == 0 or position[0] == 7:
            yIncrement = 1
        else:
            xIncrement = 1
        xIteration = position[0]
        yIteration = position[1]
        for direction in [-1, 1]:
            seeking = True
            while xIteration in spacesInBoard and yIteration in spacesInBoard and seeking:
                if xIteration in cornerIndexes and yIteration in cornerIndexes \
                        and board[yIteration][xIteration] == tileSelected:
                    return True
                if board[yIteration][xIteration] == 0:
                    seeking = False
                if board[yIteration][xIteration] == oppTile:
                    seeking = False
                xIteration += xIncrement * direction
                yIteration += yIncrement * direction
        return False


def checkStabilityScore(board, currentTurn, oppTurn):
    # function returns value based on how "stable" your pieces on the board
    # board assigning values based on how stable each position in the board, higher numbers to more valuable positions
    stabilityBoard = [
        [20, -3, 11, 8, 8, 11, -3, 20],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [20, -3, 11, 8, 8, 11, -3, 20]
    ]
    stabilityScore = 0
    # iterates board, adds the score for each position owned, and subtracts the score for each of the opponent's pieces
    for x in range(8):
        for y in range(8):
            if board[y][x] == currentTurn:
                stabilityScore += stabilityBoard[y][x]
            elif board[y][x] == oppTurn:
                stabilityScore -= stabilityBoard[y][x]
    return stabilityScore


def checkCornerOccupancy(board, currentTurn, oppTurn):
    # function returns the number of corners owned minus the number of corners owned by the opponent
    for corner in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        cornerTile = board[corner[1]][corner[0]]
        oppositeCorners = currentCorners = 0
        if cornerTile == currentTurn:
            oppositeCorners += 1
        elif cornerTile == oppTurn:
            currentCorners += 1
    return currentCorners - oppositeCorners


def checkCornerCloseness(board, currentTurn, oppTurn):
    # function returns score based on how many corners each player is close to, with less being better
    currentCloseness = oppositeCloseness = 0
    # iterates through each corner, checking if it is empty
    for corner in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        if board[corner[1]][corner[0]] == 0:
            # these 3 variables give the directions to check, based on which corner is being selected
            horizontal = (corner[0] + int(1 - corner[0] * 2 / 7), corner[1])
            diagonal = (corner[0] + int(1 - corner[0] * 2 / 7), corner[1] + int(1 - corner[1] * 2 / 7))
            vertical = (corner[0], corner[1] + int(1 - corner[1] * 2 / 7))
            for direction in [horizontal, diagonal, vertical]:
                tileChecked = board[direction[1]][direction[0]]
                # checks if the piece is stable, and if not, adds a score to the player in that position
                if not isStable(board, [direction[0], direction[1]]):
                    if tileChecked == currentTurn:
                        currentCloseness += 1
                    elif tileChecked == oppTurn:
                        oppositeCloseness += 1
    return oppositeCloseness - currentCloseness

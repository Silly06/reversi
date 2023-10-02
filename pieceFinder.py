import cv2
import numpy as np
import random


def makePlayerTurn(validMoves, videoStream):
    # keeps a count of how many frames in a row that it identifies a piece is in a position
    validatingMove = -1
    count = 0
    while True:
        # Captures the live stream frame-by-frame
        _, frame = videoStream.read()
        frame = cv2.resize(frame, [320, 240], cv2.INTER_AREA)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow("camera", frame)
        # splits the main image into quadrants, and searches each quadrant for the blue corner
        tileCoordinates = findTile(hsv)
        if tileCoordinates:
            topLeft = frame[0:120, 0:160]
            topRight = frame[0:120, 160:320]
            bottomLeft = frame[120:240, 0:160]
            bottomRight = frame[120:240, 160:320]
            topLeftRelCoord = findCorner(topLeft)
            topRightRelCoord = findCorner(topRight)
            bottomLeftRelCoord = findCorner(bottomLeft)
            bottomRightRelCoord = findCorner(bottomRight)
            if topLeftRelCoord and topRightRelCoord and bottomLeftRelCoord and bottomRightRelCoord:
                # adjusts the coordinate to be relative to the entire board
                topLeftAbsCoord = [topLeftRelCoord[0], topLeftRelCoord[1]]
                topRightAbsCoord = [topLeftRelCoord[0] + 160, topRightRelCoord[1]]
                bottomLeftAbsCoord = [bottomLeftRelCoord[0], bottomLeftRelCoord[1] + 120]
                bottomRightAbsCoord = [bottomRightRelCoord[0] + 160, bottomLeftRelCoord[1] + 120]
                # finds the average position of each of the sides, using the corners
                top = (topRightAbsCoord[1] + topLeftAbsCoord[1])/2
                bottom = (bottomRightAbsCoord[1] + bottomLeftAbsCoord[1]) / 2
                left = (topLeftAbsCoord[0] + bottomLeftAbsCoord[0])/2
                right = (topRightAbsCoord[0] + bottomRightAbsCoord[0]) / 2
                # determines the relative position of the tile on the board
                relX = ((((tileCoordinates[0] - left) / (right - left)) * 10) - 0.2) / 1.5
                relY = ((((tileCoordinates[1] - top) / (bottom - top)) * 10) - 0.5) / 1.3
                relXInt = round(relX)
                relYInt = round(relY)
                # check if the tile is within the bounds of the board
                if relXInt in range(8) and relYInt in range(8):
                    # calculates which square in the board the tile is in, returns it, and ends the loop
                    movePosition = (relXInt, relYInt)
                    print(relX, relY)
                    # checks if the move is the one being validated, adds to the score, and if sufficiently high,
                    # returns it, otherwise sets the validating move to the currently observed one
                    if movePosition == validatingMove:
                        count += 1
                        if count >= 5:
                            return movePosition
                    elif movePosition in validMoves:
                        validatingMove = movePosition
                        count = 0
                    else:
                        count = 0


def findTile(image):
    # Bounds for red in hsv, for sets at the bottom and top since hue cycles
    lower_red1 = np.array([0, 179, 30])
    upper_red1 = np.array([20, 255, 255])
    lower_red2 = np.array([160, 179, 30])
    upper_red2 = np.array([180, 255, 255])
    # adds the masks of the top and bottom reds
    mask1 = cv2.inRange(image, lower_red1, upper_red1)
    mask2 = cv2.inRange(image, lower_red2, upper_red2)
    mask = mask1 + mask2
    # opens the image, i.e., erodes and dilates the image to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cv2.waitKey(1)
    # finds red points, and if there are enough, determines the average position
    if np.sum(opening) > 1000:
        points = cv2.findNonZero(opening)
        return np.mean(points, axis=0).tolist()[0]
    else:
        return False


def findCorner(image):
    # searches for blue pixels
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 80, 20])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    points = cv2.findNonZero(mask)
    # threshold of blue pixels
    if np.sum(opening) > 1000:
        return np.mean(points, axis=0).tolist()[0]
    else:
        return False


def readMenu(videoStream):
    # keeps a count of how many frames in a row that it identifies a piece is in a position
    validatingPosition = []
    count = 0
    while True:
        _, frame = videoStream.read()
        frame = cv2.resize(frame, [320, 240], cv2.INTER_AREA)
        # converts image to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow("camera", frame)
        # splits the main image into quadrants, and searches each quadrant for the blue corner
        tileCoordinates = findTile(hsv)
        if tileCoordinates:
            topLeft = frame[90:150, 0:160]
            topRight = frame[90:150, 160:320]
            bottomLeft = frame[150:240, 0:160]
            bottomRight = frame[150:240, 160:320]
            topLeftRelCoord = findCorner(topLeft)
            topRightRelCoord = findCorner(topRight)
            bottomLeftRelCoord = findCorner(bottomLeft)
            bottomRightRelCoord = findCorner(bottomRight)
            if topLeftRelCoord and topRightRelCoord and bottomLeftRelCoord and bottomRightRelCoord:
                # adjusts the coordinate to be relative to the entire board
                topLeftAbsCoord = [topLeftRelCoord[0], topLeftRelCoord[1] + 90]
                topRightAbsCoord = [topLeftRelCoord[0] + 160, topRightRelCoord[1] + 90]
                bottomLeftAbsCoord = [bottomLeftRelCoord[0], bottomLeftRelCoord[1] + 150]
                bottomRightAbsCoord = [bottomRightRelCoord[0] + 160, bottomLeftRelCoord[1] + 150]
                # finds the average position of each of the sides, using the corners
                top = (topRightAbsCoord[1] + topLeftAbsCoord[1])/2
                bottom = (bottomRightAbsCoord[1] + bottomLeftAbsCoord[1]) / 2
                left = (topLeftAbsCoord[0] + bottomLeftAbsCoord[0])/2
                right = (topRightAbsCoord[0] + bottomRightAbsCoord[0]) / 2
                # check if the tile is within the bounds of the board
                positionX = round(((tileCoordinates[0] - left) / (right - left) * 4) - 0.5)
                positionY = round(((tileCoordinates[1] - top) / (bottom - top) * 2) - 0.5)
                if positionX in range(8) and positionY in range(8):
                    # calculates which menu option the tile is in
                    print(positionX, positionY)
                    if positionY == 1:
                        # checks if the move is the one being validated, adds to the score, and if sufficiently high,
                        # returns it, otherwise sets the validating position to the currently observed one
                        if positionX == validatingPosition:
                            count += 1
                            if count >= 5:
                                if positionX == 0:
                                    return random.randint(1, 2)
                                elif positionX == 3:
                                    return 0
                        elif positionX == 0 or positionX == 3:
                            validatingPosition = positionX
                            count = 0
                        else:
                            count = 0

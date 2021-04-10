import sys, random, time
import numpy as np

history_game_boards = np.array([])
history_moves = np.array([])
history_scores = np.array([])

clean_game_board = np.array([   [9,9,9,9,9,9,9,9],
                                [9,0,0,0,0,0,0,9],
                                [9,0,0,0,0,0,0,9],
                                [9,0,0,0,0,0,0,9],
                                [9,0,0,0,0,0,0,9],
                                [9,0,0,0,0,0,0,9],
                                [9,0,0,0,0,0,0,9],
                                [9,9,9,9,9,9,9,9]])

game_board = np.array([ [9,9,9,9,9,9,9,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,9,9,9,9,9,9,9]])

open_location = {}

snake = np.array([[2,2]])
apple = np.array([[5,5]])

score = 0

def addSnake():
    first = True
    for pos in snake:
        x,y = pos
        if (x,y) in open_location:
            open_location.pop((x,y))
        if first:
            game_board[x][y] = 2
            first = False
        else:
            game_board[x][y] = 1

def addApple():
    x,y = apple[0]
    game_board[x][y] = 3
    if (x,y) in open_location:
        open_location.pop((x,y))

def spawnApple():
    pos = random.choice(list(open_location.items()))
    apple[0][0] = pos[0][0]
    apple[0][1] = pos[0][1]

def spawnSnake():
    pos = random.choice(list(open_location.items()))
    snake[0][0] = pos[0][0]
    snake[0][1] = pos[0][1]

def addLengthToSnake(move):
    global snake
    if move == 0:
        pos = np.copy(snake[-1])
        pos[1] = pos[1]+1
        snake = np.append(snake,[pos], axis=0)
    elif move == 1:
        pos = np.copy(snake[-1])
        pos[0] = pos[0]+1
        snake = np.append(snake,[pos], axis=0)
    elif move == 2:
        pos = np.copy(snake[-1])
        pos[1] = pos[1]-1
        snake = np.append(snake,[pos], axis=0)
    else:
        pos = np.copy(snake[-1])
        pos[0] = pos[0]-1
        snake = np.append(snake,[pos], axis = 0)

def resetBoard():
    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] != 9:
                game_board[i][j] = 0
                open_location[(i,j)] = True

def updateBoard():
    #global game_board
    #global clean_game_board
    #game_board = np.copy(clean_game_board)
    resetBoard()
                
    addSnake()
    addApple()
    # Make open locations array?


def checkMovement(move):
    # Left move
    if move == 0:
        pos = snake[0]
        if game_board[pos[0]][pos[1]-1] == 9 or game_board[pos[0]][pos[1]-1] == 1:
            return False
        else:
            return True
    # Up Move
    elif move == 1:
        pos = snake[0]
        if game_board[pos[0]-1][pos[1]] == 9 or game_board[pos[0]-1][pos[1]] == 1:
            return False
        else:
            return True
    # Right move
    elif move == 2:
        # Check gameboard
        pos = snake[0]
        if game_board[pos[0]][pos[1]+1] == 9 or game_board[pos[0]][pos[1]+1] == 1:
            return False
        else:
            return True
    elif move == 3:
        pos = snake[0]
        if game_board[pos[0]+1][pos[1]] == 9 or game_board[pos[0]+1][pos[1]] == 1:
            return False
        else:
            return True
    else:
        return False

def moveSnakeLeft():
    oldX = snake[0][0]
    oldY = snake[0][1]
    (snake[0])[1] = (snake[0])[1]-1

    for i in range(1, len(snake)):
        tempX = snake[i][0]
        tempY = snake[i][1]
        snake[i][0] = oldX
        snake[i][1] = oldY
        oldX = tempX
        oldY = tempY

def moveSnakeUp():
    oldX = snake[0][0]
    oldY = snake[0][1]
    (snake[0])[0] = (snake[0])[0]-1

    for i in range(1, len(snake)):
        tempX = snake[i][0]
        tempY = snake[i][1]
        snake[i][0] = oldX
        snake[i][1] = oldY
        oldX = tempX
        oldY = tempY

def moveSnakeRight():
    oldX = snake[0][0]
    oldY = snake[0][1]
    (snake[0])[1] = (snake[0])[1]+1

    for i in range(1, len(snake)):
        tempX = snake[i][0]
        tempY = snake[i][1]
        snake[i][0] = oldX
        snake[i][1] = oldY
        oldX = tempX
        oldY = tempY

def moveSnakeDown():
    oldX = snake[0][0]
    oldY = snake[0][1]
    (snake[0])[0] = (snake[0])[0]+1

    for i in range(1, len(snake)):
        tempX = snake[i][0]
        tempY = snake[i][1]
        snake[i][0] = oldX
        snake[i][1] = oldY
        oldX = tempX
        oldY = tempY

def checkSnakeAndApple():
    if (snake[0])[0] == (apple[0])[0] and (snake[0])[1] == (apple[0])[1]:
        return True
    else:
        return False


def greedyMove():
    # Check which way we cant move
    snPos = snake[0]
    appPos = apple[0]

    up = game_board[snPos[0]-1][snPos[1]]
    down = game_board[snPos[0]+1][snPos[1]]
    left = game_board[snPos[0]][snPos[1]-1]
    right = game_board[snPos[0]][snPos[1]+1]
    #print(up)
    #print(down)
    #print(left)
    #print(right)

    upPos = [snPos[0]-1, snPos[1]]
    downPos = [snPos[0]+1, snPos[1]]
    leftPos = [snPos[0], snPos[1]-1]
    rightPos = [snPos[0], snPos[1]+1]

    # Calculate shortest distance to apple for each
    # Euclidean distance
    upEc = np.linalg.norm(np.array(appPos) - np.array(upPos))
    downEc = np.linalg.norm(np.array(appPos) - np.array(downPos))
    leftEc = np.linalg.norm(np.array(appPos) - np.array(leftPos))
    rightEc = np.linalg.norm(np.array(appPos) - np.array(rightPos))

    # Rank distances from best to worst
    rank = [(0, left, leftPos, leftEc), (1, up, upPos, upEc), (2, right, rightPos, rightEc), (3, down, downPos, downEc)]
    rank_sort = sorted(rank, key=lambda tup: tup[3])

    # Check the move that is the closest that is not a 9 or 1
    for tup in rank_sort:
        #print(tup)
        if tup[1] != 1 and tup[1] != 9:
            return tup[0]
    
    return 0


def main():
    resetBoard()
    spawnApple()
    spawnSnake()
    while 1:
        print(chr(27) + "[2J")
        # Check if snake head is on apple
        if checkSnakeAndApple():
            # Respawn apple
            spawnApple()

            # Add length to snake
            addLengthToSnake(move)

            # Add to score
            global score
            score+=100

        updateBoard()
        print("Score: " + str(score))
        print(game_board)

        # Greedy algorithm decides where to move based on board
        move = greedyMove()
        print("move: " + str(move))

        np.append(history_game_boards, game_board)
        np.append(history_moves, move)
        np.append(history_scores, score)

        if checkMovement(move):
            print("Can move")
            if (move == 0):
                moveSnakeLeft()
            elif (move == 1):
                moveSnakeUp()
            elif (move == 2):
                moveSnakeRight()
            else:
                moveSnakeDown()
        else:
            # Game over
            print("Game over")
            x = 0
            while(1):
                x+=1
        updateBoard()
        time.sleep(.5)

main()
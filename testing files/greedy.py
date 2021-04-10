import numpy as np
import sys
#print(sys.getrecursionlimit())
#sys.setrecursionlimit(100000)

visited = {}

def greedy_moveSnakeLeft(snake):
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
    return snake

def greedy_moveSnakeUp(snake):
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
    return snake

def greedy_moveSnakeRight(snake):
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
    return snake

def greedy_moveSnakeDown(snake):
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
    return snake

def greedy_addSnake(game_board, snake):
    first = True
    for pos in snake:
        x,y = pos
        if first:
            game_board[x][y] = 2
            first = False
        else:
            game_board[x][y] = 1
    return game_board

def greedy_addApple(game_board, apple):
    x,y = apple[0]
    game_board[x][y] = 3
    return game_board

def greedy_resetBoard(game_board, snake, apple):
    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] != 9:
                game_board[i][j] = 0
    game_board = greedy_addSnake(game_board, snake)
    game_board = greedy_addApple(game_board, apple)
    return game_board

def greedyHelper(game_board, visited, snake, apple, move):
    global visited
    # Check if we can move in the direction given
    snPos = snake[0]
    # Left
    if move == 0:
        left = game_board[snPos[0]][snPos[1]-1]
        param_tuple = (snPos[0], snPos[1]-1)

        if left != 1 and left != 9 and param_tuple not in visited:
            snake = greedy_moveSnakeLeft(snake)
            game_board = greedy_resetBoard(game_board, snake, apple)
            visited[param_tuple] = True
            return (np.linalg.norm(np.array(apple[0]) - np.array(snake[0])) 
                    + greedyHelper(game_board, visited, snake, apple, 0))
        else:
            up_param = (snPos[0]-1, snPos[1])
            right_param = (snPos[0], snPos[1]+1)
            down_param = (snPos[0]+1, snPos[1])
            if up_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 1)
            if right_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 2)
            if down_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 3)
            return 0
    # Up
    if move == 1:
        up = game_board[snPos[0]-1][snPos[1]]
        param_tuple = (snPos[0]-1, snPos[1])

        if up != 1 and up != 9 and param_tuple not in visited:
            snake = greedy_moveSnakeUp(snake)
            game_board = greedy_resetBoard(game_board, snake, apple)
            visited[param_tuple] = True
            return (np.linalg.norm(np.array(apple[0]) - np.array(snake[0])) 
                    + greedyHelper(game_board, visited, snake, apple, 1))
        else:
            left_param = (snPos[0], snPos[1]-1)
            right_param = (snPos[0], snPos[1]+1)
            down_param = (snPos[0]+1, snPos[1])
            if left_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 0)
            if right_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 2)
            if down_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 3)
            return 0
    # Right
    if move == 2:
        right = game_board[snPos[0]][snPos[1]+1]
        param_tuple = (snPos[0], snPos[1]+1)

        if right != 1 and right != 9 and param_tuple not in visited:
            snake = greedy_moveSnakeRight(snake)
            game_board = greedy_resetBoard(game_board, snake, apple)
            visited[param_tuple] = True
            return (np.linalg.norm(np.array(apple[0]) - np.array(snake[0])) 
                    + greedyHelper(game_board, visited, snake, apple, 2))
        else:
            left_param = (snPos[0], snPos[1]-1)
            up_param = (snPos[0]-1, snPos[1])
            down_param = (snPos[0]+1, snPos[1])
            if left_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 0)
            if up_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 1)
            if down_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 3)
            return 0
    # Down
    if move == 3:
        down = game_board[snPos[0]+1][snPos[1]]
        param_tuple = (snPos[0]+1, snPos[1])

        if down != 1 and down != 9 and param_tuple not in visited:
            snake = greedy_moveSnakeDown(snake)
            game_board = greedy_resetBoard(game_board, snake, apple)
            visited[param_tuple] = True
            return (np.linalg.norm(np.array(apple[0]) - np.array(snake[0])) 
                    + greedyHelper(game_board, visited, snake, apple, 3))
        else:
            left_param = (snPos[0], snPos[1]-1)
            up_param = (snPos[0]-1, snPos[1])
            right_param = (snPos[0], snPos[1]+1)
            if left_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 0)
            if up_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 1)
            if right_param not in visited:
                return 0 + greedyHelper(game_board, visited, snake, apple, 2)
            return 0

    return 0


def greedyMove(game_board, snake, apple):
    global visited
    # Check which way we cant move
    #snPos = snake[0]
    #appPos = apple[0]

    #up = game_board[snPos[0]-1][snPos[1]]
    #down = game_board[snPos[0]+1][snPos[1]]
    #left = game_board[snPos[0]][snPos[1]-1]
    #right = game_board[snPos[0]][snPos[1]+1]

    #upPos = [snPos[0]-1, snPos[1]]
    #downPos = [snPos[0]+1, snPos[1]]
    #leftPos = [snPos[0], snPos[1]-1]
    #rightPos = [snPos[0], snPos[1]+1]

    # Calculate shortest distance to apple for each
    # Euclidean distance
    #upEc = np.linalg.norm(np.array(appPos) - np.array(upPos))
    #downEc = np.linalg.norm(np.array(appPos) - np.array(downPos))
    #leftEc = np.linalg.norm(np.array(appPos) - np.array(leftPos))
    #rightEc = np.linalg.norm(np.array(appPos) - np.array(rightPos))
    visited = {}
    leftEc = greedyHelper(game_board, visited, snake, apple, 0)
    visited = {}
    upEc = greedyHelper(game_board, visited, snake, apple, 1)
    visited = {}
    rightEc = greedyHelper(game_board, visited, snake, apple, 2)
    visited = {}
    downEc = greedyHelper(game_board, visited, snake, apple, 3)
    visited = {}
    #print(leftEc)
    #print(upEc)
    #print(rightEc)
    #print(downEc)

    # Rank distances from best to worst
    rank = [(0, leftEc), (1, upEc), (2, rightEc), (3, downEc)]
    rank_sort = sorted(rank, key=lambda tup: tup[1])

    for tup in rank_sort:
        print(str(tup[0]) + " : " + str(tup[1]))


    # Check the move that is the closest that is not a 9 or 1
    for tup in rank_sort:
        #print(tup)
        if tup[1] != 0:
            return tup[0]
    
    return 0
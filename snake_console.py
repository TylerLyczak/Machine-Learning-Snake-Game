import sys, random, pygame, time, os
import numpy as np
from knn import WeightedKNN

# Global lists to keep information about the game to store later
history_game_boards = []
history_moves = []
history_scores = []

# The gameboard
'''
    9 = Wall
    3 = Apple
    2 = Snake head
    1 = Snake body
    0 = Open location
'''
game_board = np.array([ [9,9,9,9,9,9,9,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,0,0,0,0,0,0,9],
                        [9,9,9,9,9,9,9,9]])

# Dictionary that stores all the open locaitons on the gameboard
# Used to find random locations to spawn the apple
open_location = {}

# Inital snake and apple locations, changes right as the game starts
snake = np.array([[2,2]])
apple = np.array([[5,5]])

# Global variable to store the score of the game
score = 0


'''
    def addSnake():
        Adds the snake array to the game_board
        snake head gets a value of 2
        snake body gets a value of 1
'''
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


'''
    def addApple():
        Adds the apple to the gameboard
        apple gets a value of 3
'''
def addApple():
    x,y = apple[0]
    game_board[x][y] = 3
    if (x,y) in open_location:
        open_location.pop((x,y))


'''
    def spawnApple():
        Gets a random location from all of the open locations dictionary
        Sets that location to the apple
'''
def spawnApple():
    pos = random.choice(list(open_location.items()))
    apple[0][0] = pos[0][0]
    apple[0][1] = pos[0][1]


'''
    def spawnSnake():
        Gets a random location from all of the open locations dictionary
        Sets that location to the snake
'''
def spawnSnake():
    pos = random.choice(list(open_location.items()))
    snake[0][0] = pos[0][0]
    snake[0][1] = pos[0][1]


'''
    def resetBoard():
        Resets the gameboard to its inital state
        Adds all the open locations to the dictionary
'''
def resetBoard():
    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] != 9:
                game_board[i][j] = 0
                open_location[(i,j)] = True


'''
    def updateBoard():
        Helper function that calls multiple functions
'''
def updateBoard():
    resetBoard()
                
    addSnake()
    addApple()


'''
    def checkMovement():
        Given a movement number, checks if the snake can move in that direction
        based on if there is a wall or its body is in the way
        Returns True is can move, returns False otherwise
'''
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


'''
    def moveSnake(addToSnake, move):
        Moves the snake array in the direction given
        If snake ate an apple, it adds another elem to its array
'''
def moveSnake(addToSnake, move):
    global snake
    oldX = snake[0][0]
    oldY = snake[0][1]
    if move == 0:
        (snake[0])[1] = (snake[0])[1]-1
    elif move == 1:
        (snake[0])[0] = (snake[0])[0]-1
    elif move == 2:
        (snake[0])[1] = (snake[0])[1]+1
    else:
        (snake[0])[0] = (snake[0])[0]+1

    
    if (addToSnake):
        snake = np.insert(snake, 1, [oldX, oldY], axis=0)
    else:
        for i in range(1, len(snake)):
            tempX = snake[i][0]
            tempY = snake[i][1]
            snake[i][0] = oldX
            snake[i][1] = oldY
            oldX = tempX
            oldY = tempY


'''
    def checkSnakeAndApple():
        Checks if the snake head is on the apple
        Returns True is it is, otherwise False
'''
def checkSnakeAndApple():
    if (snake[0])[0] == (apple[0])[0] and (snake[0])[1] == (apple[0])[1]:
        return True
    else:
        return False


'''
    def greedyMove():
        Calculates the Euclidean distance for each movement the snake can make
        Sorts it based on that distance, which determines its move
'''
def greedyMove():
    # Check which way we cant move
    snPos = snake[0]
    appPos = apple[0]

    up = game_board[snPos[0]-1][snPos[1]]
    down = game_board[snPos[0]+1][snPos[1]]
    left = game_board[snPos[0]][snPos[1]-1]
    right = game_board[snPos[0]][snPos[1]+1]

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


'''
    def restartGame():
        Adds all the of the game information into different files, used for training models
        Resets the game state to a fresh game
'''
def restartGame():
    global score
    global snake
    global apple
    global history_scores
    global history_game_boards
    global history_moves

    snake = np.array([[2,2]])
    apple = np.array([[5,5]])

    if score > 2400:

        for i in history_moves:
            #history_scores = np.append(history_scores, score)
            history_scores.append(score)

        file1 = open("board_history.txt", "a")
        file2 = open("move_history.txt", "a")
        file3 = open("score_history.txt", "a")

        
        for arr in history_game_boards:
            #print(arr)
            for i in range(len(arr)):
                #file1.writelines(str(arr[i]))
                file1.writelines("[")
                for j in range(len(arr[i])):
                    temp = str(arr[i][j])
                    file1.writelines(temp)
                    if j != len(arr[i])-1:
                        file1.writelines(";")
                file1.writelines("]")
                if i != len(arr)-1:
                    file1.writelines(",")
            file1.writelines("|\n")
        
        for row in history_moves:
            file2.writelines(str(row)+";\n")

        for row in history_scores:
            file3.writelines(str(row)+";\n")

        file1.close()
        file2.close()
        file3.close()

    score = 0
    history_game_boards = []
    history_moves = []
    history_scores = []

    resetBoard()


'''
    def main():
        Runs two different while 1 loops
        The inner while loop controls the game
            After the snake loses or wins, it breaks
        The outer while loop resets the game
'''
def main():
    global history_game_boards
    global history_moves

    while 1:
        # Reset the game state to a new state
        resetBoard()
        spawnApple()
        spawnSnake()
        weightedKNN = WeightedKNN(3)
        addToSnake = False

        # Runs the game until somebody wins or loses
        while 1:
            print(chr(27) + "[2J")

            # If there are no open locations, the snake won the game
            if not open_location:
                print("SNAKE WIN!")
                break
            
            # Check if the snake head and the apple are in the same location
            if checkSnakeAndApple():
                # Respawn apple
                spawnApple()

                # Add length to snake
                addToSnake = True

                # Add to score
                global score
                score+=100
            
            # Update the board and draw the game
            updateBoard()

            print("Score: " + str(score))
            print(game_board)

            # Use KNN to get the best move
            # If no move, use greedy
            move = weightedKNN.findMove(game_board)
            result = ""
            if (move == -1):
                move = greedyMove()
                result = "Greedy Move"
            else:
                result = "KNN Move"
            
            # Display what algorithm the game used
            print(result)

            # Append the game board and the move it choose
            history_game_boards.append(np.copy(game_board))
            history_moves.append(move)

            # Check if the snake can go in that direction
            # If it can, then move the snake
            # Else, it lost
            if checkMovement(move):
                moveSnake(addToSnake, move)
                addToSnake = False
            else:
                # Game over
                print("GAME OVER!")
                break

            # Update the board
            updateBoard()
            time.sleep(1)
        restartGame()
        time.sleep(5)

main()
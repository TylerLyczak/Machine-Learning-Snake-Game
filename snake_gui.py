import sys, random, pygame, time, os
import numpy as np
from knn import WeightedKNN

pygame.init()

# Global variables for the game size
SIZE_X = 800
SIZE_Y = 460

# Initialize the game screen
screen = pygame.display.set_mode((SIZE_X, SIZE_Y))

# Set the name of the window
pygame.display.set_caption('ML Snake Game')
fonts = pygame.font.get_fonts()

# Define some colors and make an array for the snake colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
COLORS = []

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

# Global variables to store locations for GUI
max_x = 0
y_score = 0
y_move = 150
y_result = 300


'''
    def drawGame():
        Draws the current game_board each tick
        Also draws the score
'''
def drawGame():
    global max_x
    x=0
    y=0
    w=50

    color_iter = 0
    row_iter = 0
    col_iter = 0

    screen.fill(BLACK)

    # Loop through the gameboard
    for row in game_board:
        for col in row:
            box = pygame.Rect(x, y, w, w)

            # Draws different colors depending on what the number represents
            if col == 9:
                pygame.draw.rect(screen, BLUE, box)
            elif col == 1:
                # get the index of where that cord is in the snake list
                res = snake.tolist().index([row_iter, col_iter])

                # Add colors is that index is out of range
                while res > len(COLORS)-1:
                    rand1 = np.random.randint(20, 235)
                    rand2 = np.random.randint(20, 235)
                    rand3 = np.random.randint(20, 235)
                    COLORS.append((rand1, rand2, rand3))
                pygame.draw.rect(screen, WHITE, box)
                box_color = pygame.Rect(x+10, y+10, w-20, w-20)
                pygame.draw.rect(screen, COLORS[res], box_color)

            elif col == 2:
                pygame.draw.rect(screen, WHITE, box)
                eye1 = pygame.Rect(x+2, y+2, 8, 16)
                eye2 = pygame.Rect(x+38, y+2, 8, 16)
                pygame.draw.rect(screen, RED, eye1)
                pygame.draw.rect(screen, RED, eye2)
            elif col == 3:
                pygame.draw.rect(screen, RED, box)
            else:
                pygame.draw.rect(screen, BLACK, box)
            
            x=x+w
            col_iter+=1
            max_x = x
        y=y+w
        x=0
        col_iter=0
        row_iter+=1
    y += 10
    max_x+=10

    # Draw the score
    font1 = pygame.font.SysFont('didot.ttc', 72)
    score_txt = "Score: " + str(score)
    img1 = font1.render(score_txt, True, WHITE)
    screen.blit(img1, (max_x,0))
    pygame.display.update()


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
    # Make open locations array?


'''
    def checkMovement():
        Given a movement number, checks if the snake can move in that direction
        based on if there is a wall or its body is in the way
        Returns True is can move, returns False otherwise
'''
def checkMovement(move):
    # Left move
    if move == 0:
        # Check gameboard
        pos = snake[0]
        if game_board[pos[0]][pos[1]-1] == 9 or game_board[pos[0]][pos[1]-1] == 1:
            return False
        else:
            return True
    # Up Move
    elif move == 1:
        # Check gameboard
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
    # Down move
    elif move == 3:
        # Check gameboard
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
    global COLORS

    snake = np.array([[2,2]])
    apple = np.array([[5,5]])

    # If we got a score worth keeping, then add it to the files
    if score > 2400:
        for i in history_moves:
            history_scores.append(score)

        file1 = open("board_history.txt", "a")
        file2 = open("move_history.txt", "a")
        file3 = open("score_history.txt", "a")

        
        for arr in history_game_boards:
            for i in range(len(arr)):
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
    COLORS = []

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
    CLOCK = pygame.time.Clock()

    while 1:
        # Reset the game state to a new state
        resetBoard()
        spawnApple()
        spawnSnake()
        weightedKNN = WeightedKNN(3)
        addToSnake = False

        # Runs the game until somebody wins or loses
        while 1:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # If there are no open locations, the snake won the game
            if not open_location:
                font1 = pygame.font.SysFont('didot.ttc', 72)
                game_over = "SNAKE WIN!"
                img1 = font1.render(game_over, True, RED)
                screen.blit(img1, (max_x,y_result))
                pygame.display.update()
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
            drawGame()

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
            font1 = pygame.font.SysFont('didot.ttc', 72)
            img1 = font1.render(result, True, WHITE)
            screen.blit(img1, (max_x,y_move))
            pygame.display.update()

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
                font1 = pygame.font.SysFont('didot.ttc', 72)
                game_over = "GAME OVER!"
                img1 = font1.render(game_over, True, RED)
                screen.blit(img1, (max_x, y_result))
                pygame.display.update()
                break

            # Update the board
            updateBoard()
            pygame.display.update()
            CLOCK.tick(20)
        restartGame()
        time.sleep(5)

main()
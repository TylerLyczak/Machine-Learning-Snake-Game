import math
import numpy as np
import math
import os.path
np.set_printoptions(threshold=np.inf)

class WeightedKNN():
    def __init__(self, k=3):
        self.board_history = np.empty((0,8,8), int)
        self.move_history = np.array([])
        self.score_history = np.array([])
        self.k = k

        if os.path.exists("board_history.txt") and os.path.exists("move_history.txt") and os.path.exists("score_history.txt"):

            file1 = open("board_history.txt", "r")
            lines1 = file1.readlines()
            for line in lines1:
                board = np.empty((0,8), int)
                line = line.replace('|', '')
                arrays = line.split(',')
                for arr in arrays:
                    arr = arr.replace('[', '')
                    arr = arr.replace(']', '')
                    nums = arr.split(';')
                    row = np.array([])
                    for num in nums:
                        row = np.append(row, int(num))
                    board = np.append(board, [row], axis=0)
                self.board_history = np.append(self.board_history, [board], axis=0)
            
            file1.close()

            file2 = open("move_history.txt", "r")
            lines2 = file2.readlines()
            for line in lines2:
                line = line.replace(';', '')
                self.move_history = np.append(self.move_history, int(line))
            file2.close()

            file3 = open("score_history.txt", "r")
            lines3 = file3.readlines()
            for line in lines3:
                line = line.replace(';', '')
                self.score_history = np.append(self.score_history, int(line))
            file3.close()

    def findMove(self, current_board):

        best_left_moves = []
        best_right_moves = []
        best_up_moves = []
        best_down_moves = []

        #it = np.nditer(board_history, flags=['f_index'])
        for i in range(len(self.board_history)):
            #print(board_history[i])
            if (self.board_history[i] == current_board).all():
                move = self.move_history[i]
                score = self.score_history[i]

                # Add the score to the correct move list
                if move == 0:
                    # Check if the score is big enough to add to array
                    if len(best_left_moves) < self.k:
                        best_left_moves.append(score)
                    else:
                        for i in range(len(best_left_moves)):
                            if score > best_left_moves[i]:
                                best_left_moves[i] = score
                                break
                elif move == 1:
                    # Check if the score is big enough to add to array
                    if len(best_up_moves) < self.k:
                        best_up_moves.append(score)
                    else:
                        for i in range(len(best_up_moves)):
                            if score > best_up_moves[i]:
                                best_up_moves[i] = score
                                break
                elif move == 2:
                    # Check if the score is big enough to add to array
                    if len(best_right_moves) < self.k:
                        best_right_moves.append(score)
                    else:
                        for i in range(len(best_right_moves)):
                            if score > best_right_moves[i]:
                                best_right_moves[i] = score
                                break
                else:
                    # Check if the score is big enough to add to array
                    if len(best_down_moves) < self.k:
                        best_down_moves.append(score)
                    else:
                        for i in range(len(best_down_moves)):
                            if score > best_down_moves[i]:
                                best_down_moves[i] = score
                                break
        
        # Compare arrays
        avg_left = np.average(np.array(best_left_moves))
        avg_up = np.average(np.array(best_up_moves))
        avg_right = np.average(np.array(best_right_moves))
        avg_down = np.average(np.array(best_down_moves))

        avg_ls = [(0, avg_left), (1, avg_up), (2, avg_right), (3, avg_down)]
        avg_ls.sort(key=lambda a:a[1])

        if (math.isnan(avg_ls[0][1])):
            return -1
        else:
            return avg_ls[0][0]
import numpy as np


def boards_generator(file):
    line_num = 0
    board = []
    for line in file:
        line_num += 1
        # read 5 numbers into curr_board
        board.append([int(x) for x in line.split(' ') if x.strip().isdigit()])
        if line_num % 5 == 0:
            yield board
            # empty line.
            file.readline()
            # will create a new board now.
            board = []


def is_win(bit_board):
    # check row sum
    for i in range(5):
        if(np.sum(bit_board[i,:]) == 5):
            return True
    # check col sum
    for j in range(5):
        if(np.sum(bit_board[:,j]) == 5):
            return True
    return False


def calculate_time_and_score(numbers, board, direction):
    # create hash map from number to position for board
    positions = {}
    for i in range(5):
        for j in range(5):
            positions[board[i][j]] = (i,j)

    # create binary matrix for checking win
    bit_board = np.zeros((5,5))
    sum = np.sum(board)

    for t in range(len(numbers)):
        curr_num = numbers[t]
        if curr_num in positions:
            p = positions[curr_num]
            bit_board[p[0], p[1]] = 1.0
            sum -= curr_num
            if is_win(bit_board):
                return t, sum*curr_num

    return direction*10000, 0


def F (direction = 1):
    with open('input.txt') as f:
        # read numbers.
        line = f.readline().strip()
        numbers = [int(x) for x in line.split(',')]
        # read empty line.
        f.readline()
        # board generator
        best_time, best_score = direction*10000, 0
        for board in boards_generator(f):
            curr_time, curr_score = calculate_time_and_score(numbers, board, direction)
            if direction*curr_time < direction*best_time:
                best_time = curr_time
                best_score = curr_score
        print("\tbest time : ", best_time)
        print("\tbest score: ", best_score)
            

print("Part 1:")
F(direction = 1)

print("Part 2:")
F(direction = -1)

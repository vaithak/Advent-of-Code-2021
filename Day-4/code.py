import numpy as np

def get_boards_and_numbers():
    with open('input.txt') as f:    # added an extra newline
        line = f.readline().strip()
        # read numbers into numbers
        numbers = [int(x) for x in line.split(',')]

        # empty line
        f.readline()

        line_num = 0
        boards_arr = []
        curr_board = []
        for line in f:
            line_num += 1
            if line_num % 6 == 0:
                boards_arr.append(curr_board)
                curr_board = []
                continue
            # read 5 numbers into curr_board
            curr_board.append([int(x) for x in line.split(' ') if x.strip().isdigit()])

    print(numbers)
    print(boards_arr[0])
    print(boards_arr[len(boards_arr)-1])
    return numbers, boards_arr


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


def calculate_time_and_score(numbers, board):
    # create hash map from number to position for board
    positions = {}
    for i in range(5):
        for j in range(5):
            positions[board[i,j]] = (i,j)

    # create binary matrix for checking win
    bit_board = np.zeros((5,5))

    for t in range(len(numbers)):
        curr_num = numbers[t]

    return 10000, 0


def F():
    numbers, boards_arr = get_boards_and_numbers()
    best_time, best_score = 10000, 0
    for board in boards_arr:
        curr_time, curr_score = calculate_time_and_score(numbers, board)
        if curr_time < best_time:
            best_time = curr_time
            best_score = curr_score
    print("\tbest time : ", best_time)
    print("\tbest score: ", best_score)
            

print("Part 1:")
F()

print("Part 2:")
F()

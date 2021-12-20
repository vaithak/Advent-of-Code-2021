import numpy as np

def get_binary_digit(ch):
    return 1 if ch == '#' else 0

def get_char(binary_digit):
    return '#' if binary_digit == 1 else '.'

def str_to_binary_arr(s):
    binary_arr = []
    for i in range(len(s)):
        binary_arr.append(get_binary_digit(s[i]))
    return binary_arr

def get_neighbors_arr(i, j, input_matrix, boundary_constant=0):
    m, n = input_matrix.shape
    c = boundary_constant
    neighbors = []
    # handle corners.
    if i==0 and j==0:
        neighbors = [c, c, c, c, input_matrix[i,j], input_matrix[i,j+1], c, input_matrix[i+1,j], input_matrix[i+1,j+1]]
    elif i==0 and j==n-1:
        neighbors = [c, c, c, input_matrix[i,j-1], input_matrix[i,j], c, input_matrix[i+1,j-1], input_matrix[i+1,j], c]
    elif i==m-1 and j==0:
        neighbors = [c, input_matrix[i-1,j], input_matrix[i-1,j+1], c, input_matrix[i,j], input_matrix[i,j+1], c, c, c]
    elif i==m-1 and j==n-1:
        neighbors = [input_matrix[i-1,j-1], input_matrix[i-1,j], c, input_matrix[i,j-1], input_matrix[i,j], c, c, c, c]
    # handle edges.
    elif i==0:
        neighbors = [c, c, c, input_matrix[i,j-1], input_matrix[i,j], input_matrix[i,j+1], input_matrix[i+1,j-1], input_matrix[i+1,j], input_matrix[i+1,j+1]]
    elif i==m-1:
        neighbors = [input_matrix[i-1,j-1], input_matrix[i-1,j], input_matrix[i-1,j+1], input_matrix[i,j-1], input_matrix[i,j], input_matrix[i,j+1], c, c, c]
    elif j==0:
        neighbors = [c, input_matrix[i-1,j], input_matrix[i-1,j+1], c, input_matrix[i,j], input_matrix[i,j+1], c, input_matrix[i+1,j], input_matrix[i+1,j+1]]
    elif j==n-1:
        neighbors = [input_matrix[i-1,j-1], input_matrix[i-1,j], c, input_matrix[i,j-1], input_matrix[i,j], c, input_matrix[i+1,j-1], input_matrix[i+1,j], c]
    # handle inside cases
    else:
        neighbors = [input_matrix[i-1,j-1], input_matrix[i-1,j], input_matrix[i-1,j+1], input_matrix[i,j-1], input_matrix[i,j], input_matrix[i,j+1], input_matrix[i+1,j-1], input_matrix[i+1,j], input_matrix[i+1,j+1]]
    return neighbors


def find_output_at_index(i, j, input_matrix, algorithm, boundary_constant):
    neighbors = get_neighbors_arr(i, j, input_matrix, boundary_constant)
    num = int("".join(str(x) for x in neighbors), 2)
    return algorithm[num]

def print_image(matrix):
    m, n = matrix.shape
    for i in range(m):
        for j in range(n):
            print(get_char(matrix[i, j]), end='')
        print()

def apply_enhancement(input_matrix, algorithm, times):
    boundary_constant = 0
    for _ in range(times):
        temp_matrix = np.zeros(input_matrix.shape, dtype=int)
        m, n = temp_matrix.shape
        for i in range(m):
            for j in range(n):
                temp_matrix[i, j] = find_output_at_index(i, j, input_matrix, algorithm, boundary_constant)
        if boundary_constant == 0:
            boundary_constant = algorithm[0]
        else:
            boundary_constant = algorithm[511]
        input_matrix = temp_matrix
    return input_matrix

def count_ones(image_matrix):
    res = 0
    for row in image_matrix:
        for elem in row:
            if elem == 1:
                res += 1
    return res

def main(times):
    with open("input.txt") as f:
        image_matrix = []
        algorithm = str_to_binary_arr(f.readline().strip())
        f.readline() # read empty line.
        for line in f:
            curr_row = str_to_binary_arr(line.strip())
            image_matrix.append(curr_row)
        image_matrix = np.array(image_matrix, dtype=int)
        image_matrix = np.pad(image_matrix, times, mode='constant')
        output_matrix = apply_enhancement(image_matrix, algorithm, times)
        # print_image(output_matrix)
        print(f"\tNumber of ones: {count_ones(output_matrix)}")

if __name__ == '__main__':
    print("Part 1:")
    main(2)
    print("Part 2:")
    main(50)

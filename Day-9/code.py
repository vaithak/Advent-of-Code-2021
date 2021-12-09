import numpy as np

# boundary = -1 means process first and middle row,
# boundary = 0  means process only middle row,
# boundary = 1  means process only bottom row.
def process_three_rows(curr_three_rows, start_idx, boundary):
    middle_idx, last_idx = (start_idx+1)%3, (start_idx+2)%3
    res = 0
    n = len(curr_three_rows[start_idx])
    if boundary == 1:
        for i in range(n):
            if i==0 and curr_three_rows[last_idx][i]<min(curr_three_rows[middle_idx][i], curr_three_rows[last_idx][i+1]):
                res += 1+int(curr_three_rows[last_idx][i])
            elif i==(n-1) and curr_three_rows[last_idx][i]<min(curr_three_rows[middle_idx][i], curr_three_rows[last_idx][i-1]):
                res += 1+int(curr_three_rows[last_idx][i])
            elif (i>0 and i<n-1) and curr_three_rows[last_idx][i]<min(curr_three_rows[middle_idx][i], curr_three_rows[last_idx][i-1], curr_three_rows[last_idx][i+1]):
                res += 1+int(curr_three_rows[last_idx][i])
        return res
    # process middle row if boundary = -1 or 0.
    for i in range(n):
        if curr_three_rows[middle_idx][i]<min(curr_three_rows[last_idx][i], curr_three_rows[start_idx][i]):
            if i==0 and curr_three_rows[middle_idx][i]<curr_three_rows[middle_idx][i+1]:
                res += 1+int(curr_three_rows[middle_idx][i])
            elif i==(n-1) and curr_three_rows[middle_idx][i]<curr_three_rows[middle_idx][i-1]:
                res += 1+int(curr_three_rows[middle_idx][i])
            elif (i>0 and i<n-1) and curr_three_rows[middle_idx][i]<min(curr_three_rows[middle_idx][i-1], curr_three_rows[middle_idx][i+1]):
                res += 1+int(curr_three_rows[middle_idx][i])
    # process top row if boundary = -1.
    if boundary == -1:
        for i in range(n):
            if curr_three_rows[start_idx][i]<curr_three_rows[middle_idx][i]:
                if i==0 and curr_three_rows[start_idx][i]<curr_three_rows[start_idx][i+1]:
                    res += 1+int(curr_three_rows[start_idx][i])
                elif i==(n-1) and curr_three_rows[start_idx][i]<curr_three_rows[start_idx][i-1]:
                    res += 1+int(curr_three_rows[start_idx][i])
                elif (i>0 and i<n-1) and curr_three_rows[start_idx][i]<min(curr_three_rows[start_idx][i-1], curr_three_rows[start_idx][i+1]):
                    res += 1+int(curr_three_rows[start_idx][i])
    return res


def F_1():
    curr_three_rows = []
    res = 0
    with open("input.txt") as f:
        for _ in range(3):
            curr_three_rows.append(f.readline().strip())
        start_idx = 0
        res += process_three_rows(curr_three_rows, start_idx, boundary=-1)
        for line in f:
            curr_three_rows[start_idx] = line.strip()
            start_idx = (start_idx+1)%3
            res += process_three_rows(curr_three_rows, start_idx, boundary=0)
        res += process_three_rows(curr_three_rows, start_idx, boundary=1)
        print("\tres: ", res)

print("Part 1:")
F_1()


### Part 2:
def is_lowpoint(matrix, p):
    i, j = p
    m, n = len(matrix), len(matrix[0])
    if i!=0 and matrix[i-1][j]<=matrix[i][j]:
        return False
    if i!=(m-1) and matrix[i+1][j]<=matrix[i][j]:
        return False
    if j!=0 and matrix[i][j-1]<=matrix[i][j]:
        return False
    if j!=(n-1) and matrix[i][j+1]<=matrix[i][j]:
        return False
    return True


def get_lowpoints(row, matrix):
    lowpoints = []
    for j in range(len(matrix[row])):
        if is_lowpoint(matrix, (row, j)):
            lowpoints.append((row, j))
    return lowpoints


def dfs(matrix, p, visited):
    i, j = p
    m, n = len(matrix), len(matrix[0])
    res = 1
    visited[i, j] = True
    if i!=0 and matrix[i-1][j]!='9' and matrix[i-1][j]>matrix[i][j] and not visited[i-1][j]:
        res += dfs(matrix, (i-1, j), visited)
    if i!=(m-1) and matrix[i+1][j]!='9' and matrix[i+1][j]>matrix[i][j] and not visited[i+1][j]:
        res += dfs(matrix, (i+1,j), visited)
    if j!=0 and matrix[i][j-1]!='9' and matrix[i][j-1]>matrix[i][j] and not visited[i][j-1]:
        res += dfs(matrix, (i,j-1), visited)
    if j!=(n-1) and matrix[i][j+1]!='9' and matrix[i][j+1]>matrix[i][j] and not visited[i][j+1]:
        res += dfs(matrix, (i,j+1), visited)
    return res


def F_2():
    matrix = []
    res = 0
    with open("input.txt") as f:
        for line in f:
            matrix.append(line.strip())
        lowpoints = []
        m, n = len(matrix), len(matrix[0])
        for row in range(m):
            lowpoints = lowpoints + get_lowpoints(row, matrix)
        basin_sizes = []
        visited = np.full((m, n), False, dtype=bool)
        for lowpoint in lowpoints:
            basin_sizes.append(dfs(matrix, lowpoint, visited))
        basin_sizes = sorted(basin_sizes, reverse=True)
        res = basin_sizes[0]*basin_sizes[1]*basin_sizes[2]
        print("\tres: ", res)

print("Part 2:")
F_2()

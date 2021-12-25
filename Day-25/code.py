def process_east_step(matrix):
    cnt = 0
    for row in matrix:
        first_elem = row[0]
        j, n = 0, len(row)
        while j < n:
            if row[j] == '>':
                if j == n-1:
                    if first_elem == '.':
                        row[j] = '.'
                        row[0] = '>'
                        cnt += 1
                elif row[j+1] == '.':
                    row[j] = '.'
                    row[j+1] = '>'
                    j += 1
                    cnt += 1
            j += 1
    return cnt

def process_south_step(matrix):
    m, n = len(matrix), len(matrix[0])
    cnt = 0
    for j in range(n):
        i = 0
        first_elem = matrix[0][j]
        while i < m:
            if matrix[i][j] == 'v':
                if i == m-1:
                    if first_elem == '.':
                        matrix[i][j] = '.'
                        matrix[0][j] = 'v'
                        cnt += 1
                elif matrix[i+1][j] == '.':
                    matrix[i][j] = '.'
                    matrix[i+1][j] = 'v'
                    i += 1
                    cnt += 1
            i += 1
    return cnt


def main():
    matrix = []
    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            matrix.append(list(line))

    continue_flag = True
    steps = 0
    while continue_flag:
        steps += 1
        moved_east_cnt = process_east_step(matrix)
        moved_down_cnt = process_south_step(matrix)
        continue_flag = (moved_east_cnt + moved_down_cnt != 0)
    print(f"\tSteps: {steps}")


if __name__ == "__main__":
    main()

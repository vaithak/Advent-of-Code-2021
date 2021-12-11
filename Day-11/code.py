def check_index(i, j, m, n):
    return (i>=0) and (j>=0) and (i<m) and (j<n)

def get_neighbors(p, m, n):
    neighbors = []
    i, j = p
    dxs = [-1, 0, 1]
    dys = [-1, 0, 1]
    for dx in dxs:
        for dy in dys:
            if dx == 0 and dy==0:
                continue
            else:
                if check_index(i+dx, j+dy, m, n):
                    neighbors.append((i+dx, j+dy))
    return neighbors

def process_step(matrix):
    m, n = len(matrix), len(matrix[0])
    # increment all by 1.
    flash_pts = []
    for i in range(m):
        for j in range(n):
            matrix[i][j] += 1
            if matrix[i][j] == 10:
                flash_pts.append((i, j))
    # flash all flash_pts.
    for pt in flash_pts:
        neighbors = get_neighbors(pt, m, n)
        for neighbor in neighbors:
            i, j = neighbor
            matrix[i][j] += 1
            if matrix[i][j] == 10:
                flash_pts.append((i, j))
    # mark all pts flashed = 0.
    for pt in flash_pts:
        matrix[pt[0]][pt[1]] = 0
    return len(flash_pts)

def F(max_steps):
    matrix = []
    flashes = 0
    with open("input.txt") as f:
        for line in f:
            matrix.append([int(x) for x in list(line.strip())])
        for i in range(max_steps):
            new_flashes = process_step(matrix)
            if new_flashes == len(matrix)*len(matrix[0]):
                print("\tAll flashed simultaneously at step:", i+1)
                break
            flashes += new_flashes
    print("\tflashes: ", flashes)

print("Part 1:")
F(max_steps = 100)

print("Part 2:")
F(max_steps = 300)

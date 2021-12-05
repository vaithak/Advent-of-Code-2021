import numpy as np


def line_generator(file):
    for line in file:
        # parse line
        start_pt, end_pt = [x.strip() for x in line.split("->")]
        start_pt = [int(x) for x in start_pt.split(',')]
        end_pt = [int(x) for x in end_pt.split(',')]
        yield start_pt, end_pt


def is_vertical(pt_1, pt_2):
    return pt_1[0] == pt_2[0]


def is_horizontal(pt_1, pt_2):
    return pt_1[1] == pt_2[1]


def sign(a):
    if a>0      : return 1
    elif a == 0 : return 0
    return -1


def F(consider_diagonal = False):
    with open('input.txt') as f:
        grid = np.zeros((1000, 1000))
        res = 0
        for start_pt, end_pt in line_generator(f):
            if is_vertical(start_pt, end_pt):
                # mark vertical points on grid.
                x = start_pt[0]
                y1, y2 = start_pt[1], end_pt[1]
                dy = sign(y2-y1)
                for y in range(y1, y2+dy, dy):
                    grid[y][x] += 1
                    if grid[y][x] == 2:
                        res += 1
            elif is_horizontal(start_pt, end_pt):
                # mark horizontal points on grid.
                y = start_pt[1]
                x1, x2 = start_pt[0], end_pt[0]
                dx = sign(x2-x1)
                for x in range(x1, x2+dx, dx):
                    grid[y][x] += 1
                    if grid[y][x] == 2:
                        res += 1
            elif consider_diagonal:
                # must be diagonal.
                x1, y1 = start_pt
                x2, y2 = end_pt
                dx = sign(x2-x1)
                dy = sign(y2-y1)
                for _ in range(abs(x1-x2)+1):
                    grid[y1][x1] += 1
                    if grid[y1][x1] == 2:
                        res += 1
                    y1 += dy
                    x1 += dx
    print("\tcount: ", res)


print("Part 1: ")
F()

print("Part 2: ")
F(consider_diagonal = True)

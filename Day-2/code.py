import numpy as np

def F_1():
    direction = {
                 # horz, depth
        "forward": np.array([1, 0]),
        "down"   : np.array([0, 1]),
        "up"     : np.array([0, -1]),
    }
    positions = np.array([0, 0])
    # read file.
    with open('input.txt') as f:
        for line in f:
            dir, mag = line.split()
            positions += direction[dir] * int(mag)
    print("\thorz    : ", positions[0])
    print("\tdepth   : ", positions[1])
    print("\tproduct : ", positions[0] * positions[1])


def F_2():
    direction = {
                 # horz, depth, aim
        "forward": np.array([1, 1, 0]),
        "down"   : np.array([0, 0, 1]),
        "up"     : np.array([0, 0, -1]),
    }
    positions = np.array([0, 0, 0])
    # read file.
    with open('input.txt') as f:
        for line in f:
            dir, mag = line.split()
            positions[0] = positions[0] + direction[dir][0]*int(mag)
            positions[1] = positions[1] + direction[dir][1]*positions[2]*int(mag)
            positions[2] = positions[2] + direction[dir][2]*int(mag)
    print("\thorz    : ", positions[0])
    print("\tdepth   : ", positions[1])
    print("\taim     : ", positions[2])
    print("\tproduct : ", positions[0] * positions[1])


print("Part 1:")
F_1()

print("Part 2:")
F_2()

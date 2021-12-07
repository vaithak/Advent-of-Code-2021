import numpy as np


def F_1():
    with open('input.txt') as f:
        numbers = f.readline().split(',')
        numbers = [int(num.strip()) for num in numbers]
        x = np.median(numbers)
        cost = np.sum([abs(x-num) for num in numbers])
        print("\tcost: ", cost)


def cost_2(numbers, x):
    return np.sum([((x-num)**2 + abs(x-num))/2 for num in numbers])


def F_2():
    with open('input.txt') as f:
        numbers = f.readline().split(',')
        numbers = [int(num.strip()) for num in numbers]
        x_1 = np.floor(np.mean(numbers))
        x_2 = np.ceil(np.mean(numbers))
        cost = min(cost_2(numbers, x_1), cost_2(numbers, x_1-1), cost_2(numbers, x_2), cost_2(numbers, x_2+1))
        print("\tcost: ", cost)


print("Part 1:")
F_1()

print("Part 2:")
F_2()

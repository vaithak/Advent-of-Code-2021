import numpy as np


def F(MAX):
    # dp[i] tells the number of fishes after 'i' days, if initially only 1 fish with timer = 0
    dp = np.zeros(MAX+1)
    dp[0] = 1
    dp[1] = 2; dp[2] = 2; dp[3] = 2; dp[4] = 2; dp[5] = 2; dp[6] = 2; dp[7] = 2; dp[8] = 3
    start = 9
    for t in range(start, MAX+1):
        dp[t] = dp[t-7] + dp[t-9]

    res = 0
    with open("input.txt") as f:
        fishes = f.readline().strip().split(',')
        fishes = [int(fish) for fish in fishes]
        for fish in fishes:
            res += dp[MAX-fish]
    print("\tres: ", res)


print("Part 1:")
F(80)

print("Part 2:")
F(256)


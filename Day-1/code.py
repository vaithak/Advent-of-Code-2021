def F(win_size):
    prev_arr = []
    prev_sum = 0
    win_start_idx = 0 # essentially prev_arr is a circular window.
    increased_cnt = 0
    with open('input.txt') as f:
        for x in f:
            x = int(x)
            if len(prev_arr) == win_size:
                diff_sum = (x - prev_arr[win_start_idx])
                increased_cnt += diff_sum > 0
                prev_sum += diff_sum
                prev_arr[win_start_idx] = x
                win_start_idx = (win_start_idx + 1)%win_size
            else:
                prev_arr.append(x)
                prev_sum += x
    print("\tlast number: ", x)
    print("\tcount      : ", increased_cnt)


print("Part 1:")
F(1)

print("Part 2:")
F(3)

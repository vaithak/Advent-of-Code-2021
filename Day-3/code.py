import numpy as np


def bit(x, rev=False):
    if (x>=0) ^ (rev): return 1
    return 0


def bin_arr_to_num(b):
    return b.dot(2**np.arange(b.size)[::-1])


def F_1():
    with open('input.txt') as f:
        # initialize using the first line.
        s = f.readline()
        cnt_arr = 2*np.array(list(map(int, s.strip()))) - 1 # add 1 if bit is 1 else -1.
        for s in f:
            cnt_arr += 2*np.array(list(map(int, s.strip()))) - 1 # add 1 if bit is 1 else -1.
        gamma_bin_arr   = np.array([bit(x) for x in cnt_arr])
        epsilon_bin_arr = np.array([bit(x, rev=True) for x in cnt_arr])
        gamma   = bin_arr_to_num(gamma_bin_arr)
        epsilon = bin_arr_to_num(epsilon_bin_arr)   # will be 1's complement of gamma.
    print("\tgamma   : ", gamma)
    print("\tepsilon : ", epsilon)
    print("\tproduct : ", gamma*epsilon)


print("Part 1:")
F_1()


########## Part 2:

def find_winner_bit(diff, o2):
    if o2:  return int(diff >= 0)
    return int(diff < 0)


def find_remaining_candidate(lines, o2 = True):
    candidates = list(range(len(lines)))
    bit_pos = 0
    while len(candidates) > 1:
        curr_cnt = 0
        for candidate in candidates:
            curr_cnt += 2*int(lines[candidate][bit_pos]) - 1
        winner_bit = find_winner_bit(curr_cnt, o2)
        new_candidates = []
        for candidate in candidates:
            if int(lines[candidate][bit_pos]) == winner_bit:
                new_candidates.append(candidate)
        candidates = new_candidates
        bit_pos += 1
    return lines[candidates[0]]


def F_2():
    with open('input.txt') as f:
        # read num of lines.
        lines = []
        for line in f:
            lines.append(line.strip())
        o2_str  = find_remaining_candidate(lines, True)
        co2_str = find_remaining_candidate(lines, False)
        o2  = int(o2_str , 2)
        co2 = int(co2_str, 2)
    print("\to2      : ", o2)
    print("\tco2     : ", co2)
    print("\tproduct : ", o2*co2)


print("Part 2:")
F_2()

# both parts can be simply done using Ctrl+F in the editor using regex search.

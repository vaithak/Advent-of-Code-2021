import math

INF = 1000
TARGET = {
    'x': [79, 137],
    'y': [-176, -117],
}

def triangular(n):
    return (n*(n+1))//2

"""
 Assumptions:
 * Target x's are always positive.
 * Target y's are always negative.
"""

################################ Part 1: #################################
max_vy = abs(TARGET['y'][0])-1
print("Part 1:")
print(f"\tMax Vy: {max_vy}, Max Dy: {triangular(max_vy)}")


################################ Part 2: ################################
def calculate_dist_x_from_target (Vx, t):
    dist =  Vx*t - triangular(t-1)
    if dist < TARGET['x'][0]  :   return -1
    elif dist > TARGET['x'][1]:   return 1
    return 0

def calculate_dist_y_from_target (Vy, t):
    dist =  Vy*t - triangular(t-1)
    if dist > TARGET['y'][1]  :   return -1
    elif dist < TARGET['y'][0]:   return 1
    return 0

# find any index where f(x)=0, if not exists return -1.
def binary_search_find(start, end, f):
    while start <= end:
        mid = (start + end)//2
        if f(mid) == 0:     return mid
        elif f(mid) < 0:    start = mid+1
        else:               end = mid-1
    return -1

# find lowest index where f(x)=0. It is guaranteed that f(end)=0.
def binary_search_lowest(start, end, f):
    while start <= end:
        mid = (start + end)//2
        if f(mid) == 0:     end = mid-1
        else:               start = mid+1
    return end+1

# find highest index where f(x)=0. It is guaranteed that f(start)=0.
def binary_search_highest(start, end, f):
    while start <= end:
        mid = (start + end)//2
        if f(mid) == 0:     start = mid+1
        else:               end = mid-1
    return start-1

# find the lowest, highest x for which f(x) = 0. Return -1, -1 if nowhere 0.
def binary_search_range(start, end, f):
    # find a 0.
    pos_0 = binary_search_find(start, end, f)
    # no 0 exists
    if pos_0 == -1:
        return -1, -1
    # else find the range.
    return binary_search_lowest(start, pos_0, f), binary_search_highest(pos_0, end, f)


# Given Vx, compute [T1, T2] in which the point will remain inside target.
def compute_X_target_duration (Vx):
    if triangular(Vx) < TARGET['x'][0] or Vx > TARGET['x'][1]:
        return -1, -1
    largest_T = Vx
    T1, T2 = binary_search_range(1, largest_T, lambda t: calculate_dist_x_from_target(Vx, t))
    if T2 == Vx:
        T2 = INF
    return T1, T2

# Given Vy, compute [T1, T2] in which the point will remain inside target.
def compute_Y_target_duration (Vy):
    T_add = 0
    if Vy >= 0:
        T_add = 2*Vy + 1
        Vy = -Vy - 1
    
    # now Vy is < 0.
    largest_T = int(math.sqrt(2*abs(TARGET['y'][0])))+1
    T1, T2 = binary_search_range(1, largest_T, lambda t: calculate_dist_y_from_target(Vy, t))
    if T1 == -1:
        return -1, -1
    return T1+T_add, T2+T_add
    
def check_intersection(T_pair_1, T_pair_2):
    if T_pair_1[1] < T_pair_2[0] or T_pair_2[1] < T_pair_1[0]:
        return False
    return True

# check each (Vx, Vy).
Vx_range = (int(math.sqrt(2*abs(TARGET['x'][0])))-1, TARGET['x'][1])
Vy_range = (TARGET['y'][0], max_vy)
res = []
for vx in range(Vx_range[0], Vx_range[1]+1):
    T_pair_1 = compute_X_target_duration(vx)
    if T_pair_1[0] == -1:
        continue
    for vy in range(Vy_range[0], Vy_range[1]+1):
        T_pair_2 = compute_Y_target_duration(vy)
        if T_pair_2[0] == -1 or (not check_intersection(T_pair_1, T_pair_2)):
            continue
        res.append((vx, vy))

print("Part 2:")
print(f"\tcount = {len(res)}")

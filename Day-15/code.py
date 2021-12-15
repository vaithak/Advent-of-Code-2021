import heapq

def find_increased_element(matrix, index):
    m, n = len(matrix), len(matrix[0])
    i, j = index
    quot_m, quot_n = i//m, j//n
    res = matrix[i%m][j%n] + quot_n + quot_m
    if res > 9: 
        res = res - 9
    return res

def read_matrix():
    matrix = []
    with open("input.txt") as f:
        for line in f:
            matrix.append([int(x) for x in list(line.strip())])
    return matrix

def get_neighbors(index, m, n, visited):
    neighbors = []
    i, j = index
    if i!=0 and (i-1, j) not in visited:      neighbors.append((i-1, j))
    if j!=0 and (i, j-1) not in visited:      neighbors.append((i, j-1))
    if i!=m-1 and (i+1, j) not in visited:    neighbors.append((i+1, j))
    if j!=n-1 and (i, j+1) not in visited:    neighbors.append((i, j+1))
    return neighbors

def reached_target(index, m, n, mult_factor):
    return index == (mult_factor*m-1, mult_factor*n-1)

# Apply Djikstra's algorithm.
def F(mult_factor=1):
    matrix = read_matrix()
    m, n = len(matrix), len(matrix[0])
    heap = []
    heapq.heappush(heap, (0, (0, 0)))
    visited = {}
    while len(heap) > 0:
        cost, index = heapq.heappop(heap)
        neighbors = get_neighbors(index, m*mult_factor, n*mult_factor, visited)
        for neighbor in neighbors:
            neighbor_cost = find_increased_element(matrix, neighbor)
            if reached_target(neighbor, m, n, mult_factor):
                print(f"\tShortest path length: {cost+neighbor_cost}")
                return
            visited[neighbor] = True
            heapq.heappush(heap, (cost+neighbor_cost, neighbor))

print("Part 1:")
F(mult_factor=1)

print("Part 2:")
F(mult_factor=5)

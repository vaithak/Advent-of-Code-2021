def dfs_routes(adjList, start_node, end_node, visited, small_twice_node=None):
    if start_node[0].islower():
        visited[start_node] += 1
    res = 0
    for neighbor in adjList[start_node]:
        if neighbor == end_node:
            res += 1
        elif visited[neighbor] != 1:
            res += dfs_routes(adjList, neighbor, end_node, visited)
    if start_node.islower():
        visited[start_node] -= 1
    return res

def form_adj_list():
    adjList = {}
    with open("input.txt") as f:
        for line in f:
            # form adjacency list
            a, b = line.strip().split("-") # edge a-b
            if a in adjList:    adjList[a].append(b)
            else:               adjList[a] = [b]
            if b in adjList:    adjList[b].append(a)
            else:               adjList[b] = [a]
    return adjList
   
def F_1():
    adjList = form_adj_list()
    visited = {}
    for node in adjList.keys():
        visited[node] = 0
    print("\t", dfs_routes(adjList, "start", "end", visited))

print("Part 1:")
F_1()


### Part 2:
def F_2():
    adjList = form_adj_list()
    visited = {}
    for node in adjList.keys():
        visited[node] = 0
    initial_res = dfs_routes(adjList, "start", "end", visited)
    res = initial_res
    for node in adjList.keys():
        if node.islower() and node not in ["start", "end"]:
            visited[node] = -1
            res += dfs_routes(adjList, "start", "end", visited) - initial_res
            visited[node] = 0
    print("\t", res)
    
print("Part 2:")
F_2()

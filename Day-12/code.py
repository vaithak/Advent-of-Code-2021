def dfs_routes(adjList, start_node, end_node, visited):
    if start_node[0].islower():
        visited[start_node] = True
    res = 0
    for neighbor in adjList[start_node]:
        if neighbor == end_node:
            res += 1
        elif visited[neighbor] == False:
            res += dfs_routes(adjList, neighbor, end_node, visited)
    visited[start_node] = False
    return res


adjList = {}
with open("input.txt") as f:
    for line in f:
        # form adjacency list
        a, b = line.strip().split("-") # edge a-b
        if a in adjList:    adjList[a].append(b)
        else:               adjList[a] = [b]
        if b in adjList:    adjList[b].append(a)
        else:               adjList[b] = [a]
    visited = {}
    for node in adjList.keys():
        visited[node] = False
    print(adjList)
    print(dfs_routes(adjList, "start", "end", visited))

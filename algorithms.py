from collections import deque

def BFS(start, goal, maze):
    
    queue = deque([start])
    came_from = {start: None}
    
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        y, x = current
        for dy, dx in [(0,1),(1,0),(0,-1),(-1,0)]:
            neighbor = (y+dy, x+dx)
            if neighbor in maze and maze[neighbor]==0 and neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
    
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    
    return path[::-1]
#2-the seconde algorithm is DFS
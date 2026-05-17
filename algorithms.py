from collections import deque

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def _is_walkable(maze, cell):
    return cell in maze and maze[cell] == 0


def _reconstruct_path(came_from, goal):
    if goal not in came_from:
        return []
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]


def _expand_neighbors(current, maze, came_from, add_neighbor):
    y, x = current
    for dy, dx in DIRECTIONS:
        neighbor = (y + dy, x + dx)
        if _is_walkable(maze, neighbor) and neighbor not in came_from:
            came_from[neighbor] = current
            add_neighbor(neighbor)


def BFS(start, goal, maze):
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            return _reconstruct_path(came_from, goal)
        _expand_neighbors(current, maze, came_from, queue.append)

    return []


def DFS(start, goal, maze):
    stack = [start]
    came_from = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            return _reconstruct_path(came_from, goal)
        _expand_neighbors(current, maze, came_from, stack.append)

    return []

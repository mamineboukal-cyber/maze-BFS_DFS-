from collections import deque

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def _search(start, goal, maze, dfs=False):
    frontier = [start] if dfs else deque([start])
    came = {start: None}
    while frontier:
        cur = frontier.pop() if dfs else frontier.popleft()
        if cur == goal:
            path, cell = [], cur
            while cell is not None:
                path.append(cell)
                cell = came[cell]
            return path[::-1]
        y, x = cur
        for dy, dx in DIRS:
            n = (y + dy, x + dx)
            if n in maze and maze[n] == 0 and n not in came:
                came[n] = cur
                frontier.append(n)
    return []


def reachable(start, goal, maze):
    return bool(_search(start, goal, maze))


BFS = lambda start, goal, maze: _search(start, goal, maze)
DFS = lambda start, goal, maze: _search(start, goal, maze, True)
